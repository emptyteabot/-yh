@echo off
chcp 65001 >nul
title AI求职助手 - 云端后端服务

cd /d "%~dp0backend"

echo ========================================
echo   AI 求职助手 - 云端后端服务
echo ========================================
echo.
echo 正在启动后端服务 (端口 8765)...
echo 这个服务将为 Streamlit 提供自动投递功能
echo.
echo 启动后请保持此窗口打开！
echo ========================================
echo.

python main.py --port 8765

pause

