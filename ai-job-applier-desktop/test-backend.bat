@echo off
chcp 65001 >nul
echo ========================================
echo 测试后端启动
echo ========================================
echo.

cd /d %~dp0backend

echo 正在启动后端...
python main.py --port 8765

pause
