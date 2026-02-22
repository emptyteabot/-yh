@echo off
chcp 65001 >nul
title AI求职助手云端版 - 前端应用

cd /d "%~dp0frontend"

echo ========================================
echo   AI 求职助手 - 云端版前端应用
echo ========================================
echo.
echo 正在启动前端开发服务器...
echo.

npm run dev

pause

