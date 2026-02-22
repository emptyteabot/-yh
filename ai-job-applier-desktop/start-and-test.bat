@echo off
chcp 65001 >nul
cls
echo ========================================
echo AI 求职助手 - 完整启动测试
echo ========================================
echo.

echo [步骤 1/4] 检查后端是否已启动...
curl -s http://localhost:8765/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 后端已在运行
) else (
    echo ⚠️  后端未启动，正在启动...
    start "AI求职助手-后端" cmd /k "cd /d %~dp0backend && python main.py --port 8765"
    echo 等待后端启动...
    timeout /t 5 >nul
)

echo.
echo [步骤 2/4] 测试后端 API...
curl -s http://localhost:8765/health
echo.

echo.
echo [步骤 3/4] 测试记录 API...
curl -s http://localhost:8765/api/records/stats
echo.

echo.
echo [步骤 4/4] 启动前端...
cd /d %~dp0electron
start "AI求职助手-前端" cmd /k "npm run electron:dev"

echo.
echo ========================================
echo ✅ 启动完成！
echo ========================================
echo.
echo 📝 如果应用点击没反应：
echo   1. 按 F12 打开开发者工具
echo   2. 查看 Console 里的错误信息
echo   3. 把错误信息发给我
echo.
echo 🔍 后端地址: http://localhost:8765
echo 🔍 前端正在启动...
echo.
pause
