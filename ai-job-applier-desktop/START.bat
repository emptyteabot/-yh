@echo off
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════╗
echo ║   🤖 AI 求职助手 - 启动中...          ║
echo ╚════════════════════════════════════════╝
echo.

REM 停止旧进程
taskkill /F /IM electron.exe >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq AI求职助手*" >nul 2>&1

echo [1/3] 启动后端服务...
cd /d "%~dp0backend"
start "AI求职助手-后端" /MIN cmd /c "python main.py --port 8765"
timeout /t 3 >nul

REM 等待后端启动
:wait_backend
curl -s http://localhost:8765/health >nul 2>&1
if %errorlevel% neq 0 (
    echo    等待后端启动...
    timeout /t 1 >nul
    goto wait_backend
)
echo    ✅ 后端已启动

echo.
echo [2/3] 启动前端开发服务器...
cd /d "%~dp0electron"
start "AI求职助手-Vite" /MIN cmd /c "npm run dev"
timeout /t 5 >nul
echo    ✅ Vite 已启动

echo.
echo [3/3] 启动 Electron 窗口...
start "" "%~dp0electron\node_modules\.bin\electron.cmd" "%~dp0electron"
timeout /t 2 >nul

echo.
echo ╔════════════════════════════════════════╗
echo ║   ✅ 启动完成！                        ║
echo ╚════════════════════════════════════════╝
echo.
echo 📝 提示:
echo    - 后端地址: http://localhost:8765
echo    - 前端地址: http://localhost:5173
echo    - 关闭此窗口不会停止应用
echo.
echo 🔧 如果遇到问题:
echo    1. 按 F12 打开开发者工具查看错误
echo    2. 检查后端日志
echo    3. 重新运行此脚本
echo.

pause
