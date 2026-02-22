@echo off
title AI求职助手 - 前端应用
chcp 65001 >nul
cd /d "%~dp0electron"

echo ========================================
echo AI 求职助手 - 前端应用
echo ========================================
echo.
echo 正在启动前端应用...
echo.

set NODE_ENV=development
npx electron .

pause


