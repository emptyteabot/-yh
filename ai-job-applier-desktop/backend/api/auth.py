"""
认证相关 API
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from automation.boss_applier import BossApplier
from automation.config import AutoApplyConfig

router = APIRouter(prefix="/api/auth", tags=["认证"])
logger = logging.getLogger(__name__)

# 全局 applier 实例
_applier: Optional[BossApplier] = None


class LoginRequest(BaseModel):
    phone: str
    headless: bool = False


class LoginResponse(BaseModel):
    success: bool
    message: str
    session_saved: bool = False


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    登录 Boss直聘
    使用手机号验证码登录
    """
    global _applier

    try:
        # 创建配置
        config = AutoApplyConfig(
            phone=request.phone,
            headless=request.headless,
            platform="boss"
        ).to_dict()

        # 创建 applier
        _applier = BossApplier(config)

        # 初始化浏览器
        await _applier._init_browser()

        # 执行登录
        logger.info(f"开始登录 Boss直聘，手机号: {request.phone}")
        success = await _applier._async_login(request.phone)

        if success:
            # 保存会话
            await _applier.session_manager.save_session(
                _applier.context,
                {"phone": request.phone}
            )

            return LoginResponse(
                success=True,
                message="登录成功",
                session_saved=True
            )
        else:
            return LoginResponse(
                success=False,
                message="登录失败，请检查验证码是否正确"
            )

    except Exception as e:
        logger.error(f"登录失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/logout")
async def logout():
    """登出并清理会话"""
    global _applier

    try:
        if _applier:
            await _applier.close()
            _applier = None

        return {"success": True, "message": "登出成功"}
    except Exception as e:
        logger.error(f"登出失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_status():
    """获取登录状态"""
    global _applier

    is_logged_in = _applier is not None and _applier.page is not None

    return {
        "logged_in": is_logged_in,
        "platform": "boss" if is_logged_in else None
    }


def get_applier() -> Optional[BossApplier]:
    """获取当前 applier 实例"""
    return _applier
