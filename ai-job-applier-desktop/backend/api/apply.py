"""
自动投递 API
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
import asyncio

from api.auth import get_applier
from ai.llm_client import get_async_llm_client, get_llm_settings

router = APIRouter(prefix="/api/apply", tags=["投递"])
logger = logging.getLogger(__name__)


class ApplyRequest(BaseModel):
    job_ids: List[str]
    resume_text: str
    use_ai_cover_letter: bool = True


async def generate_cover_letter(job: Dict[str, Any], resume: str) -> str:
    """
    使用 AI 生成求职信
    """
    try:
        llm_client = get_async_llm_client()
        settings = get_llm_settings()

        prompt = f"""你是一个专业的求职顾问。请根据以下信息生成一封简洁的求职信（100-150字）：

岗位信息：
- 职位：{job.get('title', '')}
- 公司：{job.get('company', '')}
- 要求：{job.get('description', '')}

我的简历：
{resume}

要求：
1. 突出匹配度
2. 表达求职意愿
3. 简洁专业
4. 不要使用"尊敬的"等客套话
5. 直接开始正文

求职信："""

        response = await llm_client.chat.completions.create(
            model=settings["chat_model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )

        cover_letter = response.choices[0].message.content.strip()
        logger.info(f"生成求职信成功: {job.get('title')}")
        return cover_letter

    except Exception as e:
        logger.error(f"生成求职信失败: {e}")
        return "您好，我对这个岗位很感兴趣，希望能有机会加入贵公司。"


@router.websocket("/ws/apply")
async def websocket_apply(websocket: WebSocket):
    """
    WebSocket 批量投递接口
    """
    await websocket.accept()

    try:
        # 接收投递任务
        data = await websocket.receive_json()
        job_ids = data.get('job_ids', [])
        resume_text = data.get('resume_text', '')
        use_ai = data.get('use_ai_cover_letter', True)

        logger.info(f"收到投递任务: {len(job_ids)} 个岗位")

        applier = get_applier()
        if not applier:
            await websocket.send_json({
                'error': True,
                'message': '请先登录 Boss直聘'
            })
            await websocket.close()
            return

        if not applier.page:
            await websocket.send_json({
                'error': True,
                'message': '浏览器未初始化，请重新登录'
            })
            await websocket.close()
            return

        logger.info(f"开始批量投递，共 {len(job_ids)} 个岗位")

        # 批量投递
        success_count = 0
        failed_count = 0

        for i, job_id in enumerate(job_ids):
            try:
                # 生成求职信
                cover_letter = ""
                if use_ai and resume_text:
                    # 这里简化处理，实际应该获取岗位详情
                    job_info = {
                        'title': '岗位',
                        'company': '公司',
                        'description': ''
                    }
                    cover_letter = await generate_cover_letter(job_info, resume_text)
                else:
                    cover_letter = "您好，我对这个岗位很感兴趣，希望能有机会加入贵公司。"

                # 投递
                success = await applier.apply_to_job(
                    job_id=job_id,
                    greeting=cover_letter
                )

                if success:
                    success_count += 1
                else:
                    failed_count += 1

                # 推送进度
                await websocket.send_json({
                    'progress': (i + 1) / len(job_ids),
                    'current': i + 1,
                    'total': len(job_ids),
                    'job': f'岗位 {job_id}',
                    'company': '公司',
                    'success': success,
                    'message': '投递成功' if success else '投递失败'
                })

                # 随机延迟（3-6秒，避免被限流）
                await asyncio.sleep(3 + (i % 3))

            except Exception as e:
                failed_count += 1
                logger.error(f"投递失败 {job_id}: {e}")
                await websocket.send_json({
                    'progress': (i + 1) / len(job_ids),
                    'current': i + 1,
                    'total': len(job_ids),
                    'job': f'岗位 {job_id}',
                    'company': '公司',
                    'success': False,
                    'message': f'投递失败: {str(e)}'
                })

        # 完成
        await websocket.send_json({
            'completed': True,
            'message': f'批量投递完成！成功 {success_count} 个，失败 {failed_count} 个'
        })

    except WebSocketDisconnect:
        logger.info("WebSocket 连接断开")
    except Exception as e:
        logger.error(f"批量投递失败: {e}")
        try:
            await websocket.send_json({
                'error': True,
                'message': str(e)
            })
        except:
            pass
    finally:
        try:
            await websocket.close()
        except:
            pass


@router.post("/single")
async def apply_single_job(job_id: str, greeting: str = ""):
    """
    单个岗位投递
    """
    applier = get_applier()

    if not applier:
        raise HTTPException(status_code=401, detail="请先登录")

    try:
        success = await applier.apply_to_job(job_id=job_id, greeting=greeting)

        return {
            "success": success,
            "message": "投递成功" if success else "投递失败"
        }
    except Exception as e:
        logger.error(f"投递失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
