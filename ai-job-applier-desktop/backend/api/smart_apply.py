"""
智能投递 API - 集成 smart_apply 和 auto_apply_engine
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import asyncio

router = APIRouter(prefix="/api/smart-apply", tags=["智能投递"])
logger = logging.getLogger(__name__)


class SmartApplyRequest(BaseModel):
    resume_text: str
    target_positions: List[str]
    target_locations: List[str]
    salary_min: Optional[int] = None
    auto_generate_cover_letter: bool = True
    max_applications: int = 50


class SmartApplyResponse(BaseModel):
    success: bool
    message: str
    job_count: int = 0


@router.post("/start", response_model=SmartApplyResponse)
async def start_smart_apply(request: SmartApplyRequest):
    """
    启动智能投递
    """
    try:
        from ai.smart_apply import SmartApplyEngine

        logger.info(f"启动智能投递: {request.target_positions}")

        engine = SmartApplyEngine()

        # 配置投递参数
        config = {
            "resume_text": request.resume_text,
            "target_positions": request.target_positions,
            "target_locations": request.target_locations,
            "salary_min": request.salary_min,
            "auto_generate_cover_letter": request.auto_generate_cover_letter,
            "max_applications": request.max_applications
        }

        # 启动投递（异步）
        asyncio.create_task(engine.start(config))

        return SmartApplyResponse(
            success=True,
            message="智能投递已启动",
            job_count=0
        )

    except Exception as e:
        logger.error(f"启动智能投递失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/ws/smart-apply")
async def websocket_smart_apply(websocket: WebSocket):
    """
    WebSocket 智能投递接口 - 实时推送进度
    """
    await websocket.accept()

    try:
        # 接收配置
        data = await websocket.receive_json()
        resume_text = data.get('resume_text', '')
        target_positions = data.get('target_positions', [])
        target_locations = data.get('target_locations', [])
        salary_min = data.get('salary_min')
        max_applications = data.get('max_applications', 50)

        from ai.smart_apply import SmartApplyEngine
        from ai.auto_apply_engine import AutoApplyEngine

        logger.info(f"WebSocket 智能投递: {target_positions}")

        # 创建引擎
        smart_engine = SmartApplyEngine()
        auto_engine = AutoApplyEngine()

        # 步骤 1: 搜索岗位
        await websocket.send_json({
            'stage': 'searching',
            'message': '正在搜索匹配岗位...',
            'progress': 0.1
        })

        jobs = await smart_engine.search_matching_jobs(
            positions=target_positions,
            locations=target_locations,
            salary_min=salary_min,
            limit=max_applications
        )

        await websocket.send_json({
            'stage': 'found',
            'message': f'找到 {len(jobs)} 个匹配岗位',
            'progress': 0.3,
            'job_count': len(jobs)
        })

        # 步骤 2: 分析简历
        await websocket.send_json({
            'stage': 'analyzing',
            'message': '正在分析简历...',
            'progress': 0.4
        })

        resume_analysis = await auto_engine.analyze_resume(resume_text)

        # 步骤 3: 批量投递
        await websocket.send_json({
            'stage': 'applying',
            'message': '开始批量投递...',
            'progress': 0.5
        })

        success_count = 0
        failed_count = 0

        for i, job in enumerate(jobs):
            try:
                # 生成求职信
                cover_letter = await auto_engine.generate_cover_letter(
                    job=job,
                    resume=resume_text,
                    analysis=resume_analysis
                )

                # 投递
                result = await auto_engine.apply_job(
                    job_id=job.get('job_id'),
                    cover_letter=cover_letter
                )

                if result:
                    success_count += 1
                else:
                    failed_count += 1

                # 推送进度
                progress = 0.5 + (i + 1) / len(jobs) * 0.5
                await websocket.send_json({
                    'stage': 'applying',
                    'current': i + 1,
                    'total': len(jobs),
                    'progress': progress,
                    'job': job.get('title', ''),
                    'company': job.get('company', ''),
                    'success': result,
                    'success_count': success_count,
                    'failed_count': failed_count
                })

                # 延迟（避免频繁请求）
                await asyncio.sleep(3)

            except Exception as e:
                logger.error(f"投递失败 {job.get('title')}: {e}")
                failed_count += 1

        # 完成
        await websocket.send_json({
            'stage': 'completed',
            'message': f'投递完成！成功 {success_count} 个，失败 {failed_count} 个',
            'progress': 1.0,
            'success_count': success_count,
            'failed_count': failed_count
        })

    except WebSocketDisconnect:
        logger.info("WebSocket 连接断开")
    except Exception as e:
        logger.error(f"智能投递失败: {e}")
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


@router.get("/status")
async def get_smart_apply_status():
    """
    获取智能投递状态
    """
    try:
        # TODO: 实现状态查询
        return {
            "running": False,
            "progress": 0,
            "message": "未运行"
        }

    except Exception as e:
        logger.error(f"获取状态失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
