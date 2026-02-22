@echo off
title AI求职助手 - 后端服务
chcp 65001 >nul
cd /d "%~dp0backend"

echo ========================================
echo AI 求职助手 - 后端服务
echo ========================================
echo.
echo 正在启动后端服务...
echo.

python main.py --port 8000

pause


