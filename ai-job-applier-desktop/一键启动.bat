@echo off
chcp 65001 >nul
title AI求职助手 - 快速启动

echo ========================================
echo    AI 求职助手 - 自动投递系统
echo ========================================
echo.
echo 正在启动后端服务...
echo.

cd /d "%~dp0backend"
start "AI求职助手-后端" cmd /k "python main.py --port 8765"

echo 等待后端启动...
timeout /t 5 /nobreak >nul

echo.
echo 正在启动前端应用...
echo.

cd /d "%~dp0electron"
start "AI求职助手-前端" cmd /k "npm run dev"

echo.
echo ========================================
echo 启动完成！
echo ========================================
echo.
echo 后端地址: http://127.0.0.1:8765
echo 前端窗口: 即将自动打开
echo.
echo 使用说明:
echo 1. 等待 Electron 窗口打开
echo 2. 点击左侧"登录"登录 Boss 直聘
echo 3. 点击"简历管理"上传简历
echo 4. 点击"Boss 自动投递"开始投递
echo.
echo 详细教程请查看: 产品说明.md
echo ========================================
echo.
pause

