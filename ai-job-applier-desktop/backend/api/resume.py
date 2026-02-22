"""
简历管理 API
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import logging
import os
import PyPDF2
from docx import Document

router = APIRouter(prefix="/api/resume", tags=["简历"])
logger = logging.getLogger(__name__)

RESUME_DIR = "data/resumes"


class ResumeInfo(BaseModel):
    filename: str
    text: str
    size: int
    uploaded_at: str


def _ensure_resume_dir():
    """确保简历目录存在"""
    os.makedirs(RESUME_DIR, exist_ok=True)


def _extract_text_from_pdf(file_path: str) -> str:
    """从 PDF 提取文本"""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        logger.error(f"PDF 提取失败: {e}")
        return ""


def _extract_text_from_docx(file_path: str) -> str:
    """从 Word 提取文本"""
    try:
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        logger.error(f"Word 提取失败: {e}")
        return ""


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    上传简历
    支持 PDF 和 Word 格式
    """
    try:
        _ensure_resume_dir()

        # 检查文件类型
        if not file.filename.endswith(('.pdf', '.doc', '.docx')):
            raise HTTPException(status_code=400, detail="仅支持 PDF 和 Word 格式")

        # 保存文件
        file_path = os.path.join(RESUME_DIR, file.filename)
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)

        # 提取文本
        if file.filename.endswith('.pdf'):
            text = _extract_text_from_pdf(file_path)
        else:
            text = _extract_text_from_docx(file_path)

        logger.info(f"简历上传成功: {file.filename}")

        return {
            "success": True,
            "message": "简历上传成功",
            "filename": file.filename,
            "text_length": len(text),
            "text_preview": text[:200] if text else ""
        }

    except Exception as e:
        logger.error(f"简历上传失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_resumes():
    """
    列出所有简历
    """
    try:
        _ensure_resume_dir()

        files = []
        for filename in os.listdir(RESUME_DIR):
            if filename.endswith(('.pdf', '.doc', '.docx')):
                file_path = os.path.join(RESUME_DIR, filename)
                size = os.path.getsize(file_path)
                files.append({
                    "filename": filename,
                    "size": size,
                    "path": file_path
                })

        return {
            "success": True,
            "resumes": files,
            "total": len(files)
        }

    except Exception as e:
        logger.error(f"列出简历失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/text/{filename}")
async def get_resume_text(filename: str):
    """
    获取简历文本
    """
    try:
        file_path = os.path.join(RESUME_DIR, filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="简历不存在")

        # 提取文本
        if filename.endswith('.pdf'):
            text = _extract_text_from_pdf(file_path)
        else:
            text = _extract_text_from_docx(file_path)

        return {
            "success": True,
            "filename": filename,
            "text": text
        }

    except Exception as e:
        logger.error(f"获取简历文本失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{filename}")
async def delete_resume(filename: str):
    """
    删除简历
    """
    try:
        file_path = os.path.join(RESUME_DIR, filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="简历不存在")

        os.remove(file_path)

        return {
            "success": True,
            "message": "简历删除成功"
        }

    except Exception as e:
        logger.error(f"删除简历失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
