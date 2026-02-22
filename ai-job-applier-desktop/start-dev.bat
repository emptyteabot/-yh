@echo off
chcp 65001 >nul
echo ========================================
echo AI 求职助手 - 开发模式启动
echo ========================================
echo.

echo [1/3] 检查环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 Python
    pause
    exit /b 1
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 Node.js
    pause
    exit /b 1
)

echo ✅ 环境检查通过
echo.

echo [2/3] 启动 Python 后端...
start "AI求职助手 - 后端" cmd /k "cd /d %~dp0backend && python main.py --port 8765"
timeout /t 3 >nul
echo ✅ 后端已启动: http://localhost:8765
echo.

echo [3/3] 启动 Electron 前端...
start "AI求职助手 - 前端" cmd /k "cd /d %~dp0electron && npm run electron:dev"
echo ✅ 前端正在启动...
echo.

echo ========================================
echo ✅ 开发环境已启动！
echo ========================================
echo.
echo 📝 提示：
echo   - 后端: http://localhost:8765
echo   - 前端: http://localhost:5173
echo   - 修改代码后会自动重载
echo   - 关闭窗口即可停止服务
echo.
echo 💡 开发流程：
echo   1. 修改代码
echo   2. 保存文件
echo   3. 查看效果
echo   4. 不需要重新打包！
echo.
echo ========================================
pause
