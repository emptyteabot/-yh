@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo AI 求职助手 - 快速启动
echo ========================================
echo.

echo [1/2] 启动后端服务...
cd backend
start "后端服务" cmd /k "python main.py --port 8000"
timeout /t 5 >nul
cd ..

echo [2/2] 启动前端应用...
cd electron
start "前端应用" cmd /k "npm run electron:dev"
cd ..

echo.
echo ========================================
echo ✅ 应用已启动！
echo ========================================
echo.
echo 后端地址: http://localhost:8000
echo 前端会自动打开窗口
echo.
echo 按任意键关闭此窗口...
pause >nul

