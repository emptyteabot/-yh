"""
岗位搜索 API
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging

from api.auth import get_applier

router = APIRouter(prefix="/api/jobs", tags=["岗位"])
logger = logging.getLogger(__name__)


class JobSearchRequest(BaseModel):
    keywords: str
    location: str = ""
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    experience: Optional[str] = None
    limit: int = 50


class JobInfo(BaseModel):
    job_id: str
    title: str
    company: str
    salary: str
    location: str
    experience: str
    education: str
    description: str
    url: str
    boss_name: Optional[str] = None
    boss_title: Optional[str] = None


class JobSearchResponse(BaseModel):
    success: bool
    jobs: List[JobInfo]
    total: int
    message: str = ""


@router.post("/search", response_model=JobSearchResponse)
async def search_jobs(request: JobSearchRequest):
    """
    搜索岗位
    """
    applier = get_applier()

    if not applier:
        raise HTTPException(status_code=401, detail="请先登录")

    try:
        logger.info(f"搜索岗位: {request.keywords} @ {request.location}")

        # 构建搜索参数
        search_params = {
            "query": request.keywords,
            "city": request.location,
        }

        if request.salary_min:
            search_params["salary_min"] = request.salary_min
        if request.salary_max:
            search_params["salary_max"] = request.salary_max
        if request.experience:
            search_params["experience"] = request.experience

        # 执行搜索
        jobs = await applier.search_jobs(search_params, limit=request.limit)

        # 转换为响应格式
        job_list = []
        for job in jobs:
            job_list.append(JobInfo(
                job_id=job.get("job_id", ""),
                title=job.get("title", ""),
                company=job.get("company", ""),
                salary=job.get("salary", ""),
                location=job.get("location", ""),
                experience=job.get("experience", ""),
                education=job.get("education", ""),
                description=job.get("description", ""),
                url=job.get("url", ""),
                boss_name=job.get("boss_name"),
                boss_title=job.get("boss_title")
            ))

        return JobSearchResponse(
            success=True,
            jobs=job_list,
            total=len(job_list),
            message=f"找到 {len(job_list)} 个岗位"
        )

    except Exception as e:
        logger.error(f"搜索失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/detail/{job_id}")
async def get_job_detail(job_id: str):
    """获取岗位详情"""
    applier = get_applier()

    if not applier:
        raise HTTPException(status_code=401, detail="请先登录")

    try:
        # TODO: 实现岗位详情获取
        return {"job_id": job_id, "message": "功能开发中"}
    except Exception as e:
        logger.error(f"获取岗位详情失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
