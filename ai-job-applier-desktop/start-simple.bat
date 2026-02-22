@echo off
chcp 65001 >nul
cls
echo ========================================
echo AI 求职助手 - 简化启动
echo ========================================
echo.

echo [1/2] 检查后端...
curl -s http://localhost:8765/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 后端已在运行
) else (
    echo ⚠️  启动后端...
    cd /d %~dp0backend
    start "AI求职助手-后端" cmd /k "python main.py --port 8765"
    echo 等待后端启动...
    timeout /t 5 >nul
)

echo.
echo [2/2] 启动 Electron...
cd /d %~dp0electron
start "AI求职助手-前端" cmd /c "npm run dev && pause"

timeout /t 3 >nul

echo.
echo 等待 Vite 启动...
timeout /t 5 >nul

echo.
echo 启动 Electron 窗口...
start "" "%~dp0electron\node_modules\.bin\electron.cmd" "%~dp0electron\dist\main\index.js"

echo.
echo ========================================
echo ✅ 启动完成！
echo ========================================
echo.
echo 📝 如果应用没有打开：
echo   1. 检查是否有错误提示
echo   2. 手动运行: electron\node_modules\.bin\electron.cmd electron\dist\main\index.js
echo.
pause
