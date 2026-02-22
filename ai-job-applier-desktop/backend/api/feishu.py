"""
飞书通知 API
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

router = APIRouter(prefix="/api/feishu", tags=["飞书通知"])
logger = logging.getLogger(__name__)


class FeishuMessageRequest(BaseModel):
    message: str
    message_type: str = "text"  # text, card, interactive
    webhook_url: Optional[str] = None


class FeishuMessageResponse(BaseModel):
    success: bool
    message: str


@router.post("/send", response_model=FeishuMessageResponse)
async def send_feishu_message(request: FeishuMessageRequest):
    """
    发送飞书消息
    """
    try:
        from ai.feishu_bot import FeishuBot

        logger.info(f"发送飞书消息: {request.message[:50]}...")

        bot = FeishuBot(webhook_url=request.webhook_url)

        if request.message_type == "text":
            result = await bot.send_text(request.message)
        elif request.message_type == "card":
            result = await bot.send_card(request.message)
        else:
            result = await bot.send_text(request.message)

        if result:
            return FeishuMessageResponse(
                success=True,
                message="消息发送成功"
            )
        else:
            return FeishuMessageResponse(
                success=False,
                message="消息发送失败"
            )

    except Exception as e:
        logger.error(f"发送飞书消息失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/notify-application")
async def notify_application(
    job_title: str,
    company: str,
    status: str,
    webhook_url: Optional[str] = None
):
    """
    发送投递通知
    """
    try:
        from ai.feishu_bot import FeishuBot

        bot = FeishuBot(webhook_url=webhook_url)

        message = f"""
📮 投递通知

岗位：{job_title}
公司：{company}
状态：{status}
时间：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        result = await bot.send_text(message)

        return {
            "success": result,
            "message": "通知发送成功" if result else "通知发送失败"
        }

    except Exception as e:
        logger.error(f"发送投递通知失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
async def test_feishu_webhook(webhook_url: str):
    """
    测试飞书 Webhook
    """
    try:
        from ai.feishu_bot import FeishuBot

        bot = FeishuBot(webhook_url=webhook_url)
        result = await bot.send_text("🎉 飞书 Webhook 测试成功！")

        return {
            "success": result,
            "message": "测试成功" if result else "测试失败"
        }

    except Exception as e:
        logger.error(f"测试飞书 Webhook 失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
