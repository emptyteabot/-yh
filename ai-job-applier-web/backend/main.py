"""
云端自动投递后端 - 完整版
支持任务队列、用户认证、计费系统
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List
import os
from pathlib import Path
import PyPDF2
import docx
from openai import AsyncOpenAI
import jwt
from datetime import datetime, timedelta
import asyncio
import json
import uuid
from collections import defaultdict

app = FastAPI(title="AI求职助手云端版", version="2.0.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

# DeepSeek API
llm_client = AsyncOpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

# 简单的内存数据库（生产环境用 PostgreSQL/MySQL）
users_db = {}
tasks_db = {}
active_connections = defaultdict(list)

security = HTTPBearer()

# ==================== 数据模型 ====================

class User(BaseModel):
    id: str
    phone: str
    nickname: str = "用户"
    plan: str = "free"  # free/basic/pro/yearly
    remaining_quota: int = 5  # 剩余投递次数
    created_at: datetime
    expired_at: Optional[datetime] = None

class RegisterRequest(BaseModel):
    phone: str
    code: str
    nickname: Optional[str] = "用户"

class LoginRequest(BaseModel):
    phone: str
    code: str

class ApplyTask(BaseModel):
    keyword: str
    city: str = "全国"
    max_count: int = 10
    resume_text: str

class UpgradeRequest(BaseModel):
    plan: str  # basic/pro/yearly

# ==================== 工具函数 ====================

def extract_text_from_pdf(file_path: str) -> str:
    """从 PDF 提取文本"""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path: str) -> str:
    """从 Word 提取文本"""
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def create_token(user_id: str) -> str:
    """创建 JWT Token"""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> Optional[str]:
    """验证 Token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("user_id")
    except:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """获取当前用户"""
    user_id = verify_token(credentials.credentials)
    if not user_id or user_id not in users_db:
        raise HTTPException(401, "未登录或 Token 已过期")
    return users_db[user_id]

# ==================== 模拟投递引擎 ====================

async def search_jobs(keyword: str, city: str, max_count: int) -> List[dict]:
    """
    搜索岗位（模拟）
    生产环境：调用 Desktop 版的 boss_auto_apply.py
    """
    # 模拟搜索结果
    jobs = []
    for i in range(min(max_count, 10)):
        jobs.append({
            "id": f"job_{i}",
            "title": f"{keyword}工程师",
            "company": f"公司{i+1}",
            "salary": "8-15K",
            "url": f"https://www.zhipin.com/job_detail/{i}.html"
        })
    
    await asyncio.sleep(2)  # 模拟搜索延迟
    return jobs

async def generate_greeting(job: dict, resume_text: str) -> str:
    """
    AI 生成打招呼消息
    """
    try:
        prompt = f"""你是求职助手。请根据岗位和简历生成一条简短的打招呼消息（50字以内）。

岗位：{job['title']} - {job['company']}
简历：{resume_text[:500]}

要求：
1. 突出匹配度
2. 表达求职意愿
3. 简洁专业
4. 不要客套话

打招呼消息："""

        response = await llm_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )
        
        return response.choices[0].message.content.strip()
    except:
        return f"您好，我对{job['title']}岗位很感兴趣，期待与您沟通！"

async def apply_single_job(job: dict, greeting: str) -> bool:
    """
    投递单个岗位（模拟）
    生产环境：调用 Playwright 自动化投递
    """
    # 模拟投递延迟
    await asyncio.sleep(3)
    
    # 90% 成功率
    import random
    return random.random() < 0.9

# ==================== API 接口 ====================

@app.get("/")
async def root():
    return {
        "name": "AI求职助手云端版",
        "version": "2.0.0",
        "status": "running"
    }

@app.post("/api/auth/send-code")
async def send_verification_code(phone: str):
    """
    发送验证码（模拟）
    生产环境：对接短信服务商
    """
    # 模拟发送验证码
    code = "123456"  # 生产环境：生成随机验证码并发送短信
    
    return {
        "success": True,
        "message": "验证码已发送",
        "code": code  # 仅开发环境返回，生产环境删除
    }

@app.post("/api/auth/register")
async def register(req: RegisterRequest):
    """
    用户注册
    """
    # 验证验证码（模拟）
    if req.code != "123456":
        raise HTTPException(400, "验证码错误")
    
    # 检查是否已注册
    for user in users_db.values():
        if user.phone == req.phone:
            raise HTTPException(400, "手机号已注册")
    
    # 创建用户
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        phone=req.phone,
        nickname=req.nickname,
        plan="free",
        remaining_quota=5,
        created_at=datetime.now()
    )
    
    users_db[user_id] = user
    token = create_token(user_id)
    
    return {
        "success": True,
        "token": token,
        "user": user.dict()
    }

@app.post("/api/auth/login")
async def login(req: LoginRequest):
    """
    用户登录
    """
    # 验证验证码（模拟）
    if req.code != "123456":
        raise HTTPException(400, "验证码错误")
    
    # 查找用户
    user = None
    for u in users_db.values():
        if u.phone == req.phone:
            user = u
            break
    
    if not user:
        raise HTTPException(404, "用户不存在，请先注册")
    
    token = create_token(user.id)
    
    return {
        "success": True,
        "token": token,
        "user": user.dict()
    }

@app.get("/api/user/info")
async def get_user_info(user: User = Depends(get_current_user)):
    """
    获取用户信息
    """
    return {
        "success": True,
        "user": user.dict()
    }

@app.post("/api/user/upgrade")
async def upgrade_plan(req: UpgradeRequest, user: User = Depends(get_current_user)):
    """
    升级套餐
    """
    plans = {
        "basic": {"quota": 30, "price": 19.9, "days": 30},
        "pro": {"quota": 100, "price": 39.9, "days": 30},
        "yearly": {"quota": 999999, "price": 199, "days": 365}
    }
    
    if req.plan not in plans:
        raise HTTPException(400, "套餐不存在")
    
    plan_info = plans[req.plan]
    
    # 更新用户套餐（实际需要对接支付）
    user.plan = req.plan
    user.remaining_quota = plan_info["quota"]
    user.expired_at = datetime.now() + timedelta(days=plan_info["days"])
    
    return {
        "success": True,
        "message": f"升级成功！获得 {plan_info['quota']} 次投递额度",
        "user": user.dict()
    }

@app.post("/api/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user)
):
    """
    上传简历
    """
    try:
        # 保存文件
        file_path = UPLOAD_DIR / f"{user.id}_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # 提取文本
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(str(file_path))
        elif file.filename.endswith('.docx'):
            text = extract_text_from_docx(str(file_path))
        else:
            raise HTTPException(400, "只支持 PDF 和 Word 格式")

        return {
            "success": True,
            "filename": file.filename,
            "text": text
        }
    except Exception as e:
        raise HTTPException(500, f"上传失败: {str(e)}")

@app.websocket("/api/apply/ws")
async def websocket_apply(websocket: WebSocket):
    """
    WebSocket 自动投递
    """
    await websocket.accept()
    
    try:
        # 接收任务数据
        data = await websocket.receive_json()
        
        # 验证 Token
        token = data.get('token')
        user_id = verify_token(token)
        if not user_id or user_id not in users_db:
            await websocket.send_json({"error": True, "message": "未登录"})
            await websocket.close()
            return
        
        user = users_db[user_id]
        
        # 解析任务
        keyword = data.get('keyword', '')
        city = data.get('city', '全国')
        max_count = min(data.get('max_count', 10), user.remaining_quota)
        resume_text = data.get('resume_text', '')
        
        if max_count <= 0:
            await websocket.send_json({
                "error": True,
                "message": "投递次数已用完，请升级套餐"
            })
            await websocket.close()
            return
        
        # 搜索岗位
        await websocket.send_json({
            "stage": "searching",
            "message": f"正在搜索 {keyword} 岗位...",
            "progress": 0.1
        })
        
        jobs = await search_jobs(keyword, city, max_count)
        
        await websocket.send_json({
            "stage": "found",
            "message": f"找到 {len(jobs)} 个岗位",
            "progress": 0.3,
            "job_count": len(jobs)
        })
        
        # 批量投递
        await websocket.send_json({
            "stage": "applying",
            "message": "开始批量投递...",
            "progress": 0.4
        })
        
        success_count = 0
        failed_count = 0
        
        for i, job in enumerate(jobs):
            try:
                # 生成打招呼消息
                greeting = await generate_greeting(job, resume_text)
                
                # 投递
                success = await apply_single_job(job, greeting)
                
                if success:
                    success_count += 1
                    user.remaining_quota -= 1
                else:
                    failed_count += 1
                
                # 推送进度
                progress = 0.4 + (i + 1) / len(jobs) * 0.6
                await websocket.send_json({
                    "stage": "applying",
                    "current": i + 1,
                    "total": len(jobs),
                    "progress": progress,
                    "job": job['title'],
                    "company": job['company'],
                    "greeting": greeting,
                    "success": success,
                    "success_count": success_count,
                    "failed_count": failed_count,
                    "remaining_quota": user.remaining_quota
                })
                
                # 延迟
                await asyncio.sleep(2)
                
            except Exception as e:
                failed_count += 1
                print(f"投递失败: {e}")
        
        # 完成
        await websocket.send_json({
            "stage": "completed",
            "message": f"投递完成！成功 {success_count} 个，失败 {failed_count} 个",
            "progress": 1.0,
            "success_count": success_count,
            "failed_count": failed_count,
            "remaining_quota": user.remaining_quota
        })
        
    except WebSocketDisconnect:
        print("WebSocket 连接断开")
    except Exception as e:
        print(f"WebSocket 错误: {e}")
        try:
            await websocket.send_json({
                "error": True,
                "message": str(e)
            })
        except:
            pass
    finally:
        try:
            await websocket.close()
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    print("🚀 AI求职助手云端版启动中...")
    print("📍 后端地址: http://0.0.0.0:8765")
    print("📖 API 文档: http://0.0.0.0:8765/docs")
    uvicorn.run(app, host="0.0.0.0", port=8765)
