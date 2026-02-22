"""
简历分析 API - 集成 4 个 AI Agent
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
import asyncio

router = APIRouter(prefix="/api/analysis", tags=["简历分析"])
logger = logging.getLogger(__name__)


class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    analysis_type: str = "full"  # full, career, jobs, interview, quality


class ResumeAnalysisResponse(BaseModel):
    success: bool
    results: Dict[str, Any]
    message: str = ""


@router.post("/resume", response_model=ResumeAnalysisResponse)
async def analyze_resume(request: ResumeAnalysisRequest):
    """
    简历分析 - 使用 4 个 AI Agent
    - career_analyst: 职业分析师
    - job_matcher: 岗位推荐专家
    - interview_coach: 面试辅导专家
    - quality_auditor: 质量审核官
    """
    try:
        from ai.optimized_pipeline import OptimizedJobPipeline

        logger.info(f"开始简历分析，类型: {request.analysis_type}")

        pipeline = OptimizedJobPipeline()
        results = {}

        # Agent 1: 职业分析
        if request.analysis_type in ["full", "career"]:
            logger.info("执行职业分析...")
            career_analysis = await asyncio.to_thread(
                pipeline._ai_think,
                "career_analyst",
                f"请分析以下简历：\n\n{request.resume_text}"
            )
            results['career_analysis'] = career_analysis

        # Agent 2: 岗位推荐
        if request.analysis_type in ["full", "jobs"]:
            logger.info("执行岗位推荐...")
            job_recommendations = await asyncio.to_thread(
                pipeline._ai_think,
                "job_matcher",
                f"简历：\n{request.resume_text}\n\n职业分析：\n{results.get('career_analysis', '无')}"
            )
            results['job_recommendations'] = job_recommendations

        # Agent 3: 面试辅导
        if request.analysis_type in ["full", "interview"]:
            logger.info("执行面试辅导...")
            interview_prep = await asyncio.to_thread(
                pipeline._ai_think,
                "interview_coach",
                f"简历：\n{request.resume_text}\n\n职业分析：\n{results.get('career_analysis', '无')}\n\n岗位匹配：\n{results.get('job_recommendations', '无')}"
            )
            results['interview_preparation'] = interview_prep
            results['mock_interview'] = interview_prep

        # Agent 4: 质量审核
        if request.analysis_type in ["full", "quality"]:
            logger.info("执行质量审核...")
            quality_audit = await asyncio.to_thread(
                pipeline._ai_think,
                "quality_auditor",
                f"职业分析：\n{results.get('career_analysis', '无')}\n\n岗位匹配：\n{results.get('job_recommendations', '无')}\n\n面试准备：\n{results.get('interview_preparation', '无')}"
            )
            results['skill_gap_analysis'] = quality_audit
            results['quality_audit'] = quality_audit

        logger.info("简历分析完成")

        return ResumeAnalysisResponse(
            success=True,
            results=results,
            message="分析完成"
        )

    except Exception as e:
        logger.error(f"简历分析失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize")
async def optimize_resume(resume_text: str, target_job: Optional[str] = None):
    """
    简历优化 - 使用 resume_optimizer
    """
    try:
        from ai.resume_optimizer import ResumeOptimizer

        logger.info("开始简历优化...")

        optimizer = ResumeOptimizer()
        optimized = await asyncio.to_thread(
            optimizer.optimize,
            resume_text,
            target_job
        )

        return {
            "success": True,
            "original": resume_text,
            "optimized": optimized,
            "message": "优化完成"
        }

    except Exception as e:
        logger.error(f"简历优化失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/skills-gap")
async def analyze_skills_gap(resume_text: str, target_job: str):
    """
    技能差距分析
    """
    try:
        from ai.optimized_pipeline import OptimizedJobPipeline

        logger.info("开始技能差距分析...")

        pipeline = OptimizedJobPipeline()
        analysis = await asyncio.to_thread(
            pipeline._ai_think,
            "quality_auditor",
            f"简历：\n{resume_text}\n\n目标岗位：\n{target_job}\n\n请分析技能差距"
        )

        return {
            "success": True,
            "analysis": analysis,
            "message": "分析完成"
        }

    except Exception as e:
        logger.error(f"技能差距分析失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
