@echo off
chcp 65001 >nul
title AI求职助手云端版 - 后端服务

cd /d "%~dp0backend"

echo ========================================
echo   AI 求职助手 - 云端版后端服务
echo ========================================
echo.
echo 正在启动后端服务 (端口 8765)...
echo.

python main.py

pause

