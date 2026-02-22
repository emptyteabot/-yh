"""
投递记录 API
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging
import json
import os

router = APIRouter(prefix="/api/records", tags=["记录"])
logger = logging.getLogger(__name__)

# 简单的 JSON 文件存储
RECORDS_FILE = "data/application_records.json"


class ApplicationRecord(BaseModel):
    id: str
    job_id: str
    job_title: str
    company: str
    salary: str
    location: str
    status: str  # success, failed, pending
    cover_letter: str
    applied_at: str
    response: Optional[str] = None


class RecordsResponse(BaseModel):
    success: bool
    records: List[ApplicationRecord]
    total: int


def _ensure_data_dir():
    """确保数据目录存在"""
    os.makedirs("data", exist_ok=True)


def _load_records() -> List[dict]:
    """加载记录"""
    _ensure_data_dir()

    if not os.path.exists(RECORDS_FILE):
        return []

    try:
        with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载记录失败: {e}")
        return []


def _save_records(records: List[dict]):
    """保存记录"""
    _ensure_data_dir()

    try:
        with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"保存记录失败: {e}")


@router.get("", response_model=RecordsResponse)
async def get_records(
    status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    获取投递记录
    """
    try:
        records = _load_records()

        # 筛选
        if status:
            records = [r for r in records if r.get('status') == status]

        # 排序（最新的在前）
        records.sort(key=lambda x: x.get('applied_at', ''), reverse=True)

        # 分页
        total = len(records)
        records = records[offset:offset + limit]

        # 转换为响应格式
        record_list = []
        for r in records:
            record_list.append(ApplicationRecord(
                id=r.get('id', ''),
                job_id=r.get('job_id', ''),
                job_title=r.get('job_title', ''),
                company=r.get('company', ''),
                salary=r.get('salary', ''),
                location=r.get('location', ''),
                status=r.get('status', ''),
                cover_letter=r.get('cover_letter', ''),
                applied_at=r.get('applied_at', ''),
                response=r.get('response')
            ))

        return RecordsResponse(
            success=True,
            records=record_list,
            total=total
        )

    except Exception as e:
        logger.error(f"获取记录失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def add_record(record: ApplicationRecord):
    """
    添加投递记录
    """
    try:
        records = _load_records()

        # 添加新记录
        record_dict = record.dict()
        if not record_dict.get('id'):
            record_dict['id'] = f"{record.job_id}_{int(datetime.now().timestamp())}"
        if not record_dict.get('applied_at'):
            record_dict['applied_at'] = datetime.now().isoformat()

        records.append(record_dict)
        _save_records(records)

        return {"success": True, "message": "记录添加成功"}

    except Exception as e:
        logger.error(f"添加记录失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{record_id}")
async def delete_record(record_id: str):
    """
    删除投递记录
    """
    try:
        records = _load_records()
        records = [r for r in records if r.get('id') != record_id]
        _save_records(records)

        return {"success": True, "message": "记录删除成功"}

    except Exception as e:
        logger.error(f"删除记录失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats():
    """
    获取统计信息
    """
    try:
        records = _load_records()

        total = len(records)
        success = len([r for r in records if r.get('status') == 'success'])
        failed = len([r for r in records if r.get('status') == 'failed'])
        pending = len([r for r in records if r.get('status') == 'pending'])

        return {
            "total": total,
            "success": success,
            "failed": failed,
            "pending": pending,
            "success_rate": round(success / total * 100, 2) if total > 0 else 0
        }

    except Exception as e:
        logger.error(f"获取统计失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export")
async def export_records():
    """
    导出记录为 CSV
    """
    try:
        records = _load_records()

        # TODO: 实现 CSV 导出
        return {"message": "功能开发中"}

    except Exception as e:
        logger.error(f"导出失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
