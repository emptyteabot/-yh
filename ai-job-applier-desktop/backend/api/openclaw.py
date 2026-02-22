"""
岗位搜索 API - 集成 OpenClaw 真实数据
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging

router = APIRouter(prefix="/api/openclaw", tags=["OpenClaw岗位搜索"])
logger = logging.getLogger(__name__)


class OpenClawSearchRequest(BaseModel):
    keywords: str
    location: str = "全国"
    experience: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    limit: int = 50


class JobDetail(BaseModel):
    job_id: str
    title: str
    company: str
    salary: str
    location: str
    experience: str
    education: str
    description: str
    skills: List[str] = []
    welfare: List[str] = []
    boss_name: Optional[str] = None
    boss_title: Optional[str] = None
    url: str


class OpenClawSearchResponse(BaseModel):
    success: bool
    jobs: List[JobDetail]
    total: int
    source: str  # "openclaw" or "mock"
    message: str = ""


@router.post("/search", response_model=OpenClawSearchResponse)
async def search_jobs_openclaw(request: OpenClawSearchRequest):
    """
    使用 OpenClaw 搜索真实岗位
    如果 OpenClaw 不可用，返回模拟数据
    """
    try:
        from ai.local_openclaw_client import LocalOpenClawClient

        logger.info(f"OpenClaw 搜索: {request.keywords} @ {request.location}")

        client = LocalOpenClawClient()

        # 检查 OpenClaw 是否可用
        if not client.is_available():
            logger.warning("OpenClaw 不可用，返回模拟数据")
            return _get_mock_jobs(request)

        # 使用 OpenClaw 搜索
        jobs = await client.search_jobs(
            keywords=request.keywords,
            location=request.location,
            experience=request.experience,
            salary_min=request.salary_min,
            salary_max=request.salary_max,
            limit=request.limit
        )

        # 转换为响应格式
        job_list = []
        for job in jobs:
            job_list.append(JobDetail(
                job_id=job.get("job_id", ""),
                title=job.get("title", ""),
                company=job.get("company", ""),
                salary=job.get("salary", ""),
                location=job.get("location", ""),
                experience=job.get("experience", ""),
                education=job.get("education", ""),
                description=job.get("description", ""),
                skills=job.get("skills", []),
                welfare=job.get("welfare", []),
                boss_name=job.get("boss_name"),
                boss_title=job.get("boss_title"),
                url=job.get("url", "")
            ))

        return OpenClawSearchResponse(
            success=True,
            jobs=job_list,
            total=len(job_list),
            source="openclaw",
            message=f"找到 {len(job_list)} 个真实岗位"
        )

    except Exception as e:
        logger.error(f"OpenClaw 搜索失败: {e}")
        # 降级到模拟数据
        return _get_mock_jobs(request)


def _get_mock_jobs(request: OpenClawSearchRequest) -> OpenClawSearchResponse:
    """
    返回模拟岗位数据（当 OpenClaw 不可用时）
    """
    mock_jobs = [
        JobDetail(
            job_id="mock_001",
            title=f"{request.keywords}工程师",
            company="示例科技有限公司",
            salary="15-25K",
            location=request.location,
            experience="1-3年",
            education="本科",
            description=f"负责{request.keywords}相关开发工作，要求熟悉相关技术栈。",
            skills=["Python", "FastAPI", "React"],
            welfare=["五险一金", "弹性工作", "年终奖"],
            boss_name="张经理",
            boss_title="技术总监",
            url="https://www.zhipin.com"
        ),
        JobDetail(
            job_id="mock_002",
            title=f"高级{request.keywords}开发",
            company="创新互联网公司",
            salary="20-35K",
            location=request.location,
            experience="3-5年",
            education="本科",
            description=f"负责{request.keywords}架构设计和核心功能开发。",
            skills=["Python", "AI", "大模型"],
            welfare=["股票期权", "免费三餐", "健身房"],
            boss_name="李总",
            boss_title="CTO",
            url="https://www.zhipin.com"
        ),
        JobDetail(
            job_id="mock_003",
            title=f"{request.keywords}实习生",
            company="大型互联网公司",
            salary="8-12K",
            location=request.location,
            experience="在校生",
            education="本科",
            description=f"协助{request.keywords}项目开发，学习机会多。",
            skills=["Python", "基础算法"],
            welfare=["转正机会", "导师指导", "团建活动"],
            boss_name="王主管",
            boss_title="研发经理",
            url="https://www.zhipin.com"
        )
    ]

    return OpenClawSearchResponse(
        success=True,
        jobs=mock_jobs[:request.limit],
        total=len(mock_jobs),
        source="mock",
        message="OpenClaw 不可用，返回模拟数据"
    )


@router.get("/status")
async def get_openclaw_status():
    """
    检查 OpenClaw 状态
    """
    try:
        from ai.local_openclaw_client import LocalOpenClawClient

        client = LocalOpenClawClient()
        is_available = client.is_available()

        return {
            "available": is_available,
            "message": "OpenClaw 可用" if is_available else "OpenClaw 不可用，将使用模拟数据"
        }

    except Exception as e:
        logger.error(f"检查 OpenClaw 状态失败: {e}")
        return {
            "available": False,
            "message": f"检查失败: {str(e)}"
        }
