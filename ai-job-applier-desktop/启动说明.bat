@echo off
chcp 65001 >nul

echo ========================================
echo AI 求职助手 - 完整启动
echo ========================================
echo.

echo [提示] 由于路径包含中文，请手动执行以下步骤：
echo.
echo ----------------------------------------
echo 步骤 1: 启动后端
echo ----------------------------------------
echo 1. 打开新的命令提示符（CMD）
echo 2. 复制并运行以下命令：
echo.
echo    cd Desktop\ai-job-applier-desktop\backend
echo    python main.py --port 8000
echo.
echo 等待看到：Uvicorn running on http://127.0.0.1:8000
echo.
echo ----------------------------------------
echo 步骤 2: 启动前端
echo ----------------------------------------
echo 1. 打开另一个命令提示符（CMD）
echo 2. 复制并运行以下命令：
echo.
echo    cd Desktop\ai-job-applier-desktop\electron
echo    set NODE_ENV=development
echo    npx electron .
echo.
echo 应该会弹出应用窗口
echo.
echo ========================================
echo.
echo 如果 electron 未安装，先运行：
echo    cd Desktop\ai-job-applier-desktop\electron
echo    npm install
echo.
echo ========================================
pause


