@echo off
chcp 65001 >nul
cd /d "%~dp0electron"

echo ========================================
echo 启动 Electron 应用
echo ========================================
echo.

echo 设置开发环境...
set NODE_ENV=development

echo 启动 Electron...
electron .

pause


