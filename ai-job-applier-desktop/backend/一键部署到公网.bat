@echo off
chcp 65001 >nul
echo ========================================
echo   快速部署到公网 - 一键启动
echo ========================================
echo.

echo [步骤 1/4] 检查 ngrok...
where ngrok >nul 2>&1
if errorlevel 1 (
    echo ❌ ngrok 未安装
    echo.
    echo 请按以下步骤操作：
    echo 1. 访问 https://ngrok.com/download
    echo 2. 下载 Windows 版本
    echo 3. 解压到任意文件夹
    echo 4. 将 ngrok.exe 所在文件夹添加到系统 PATH
    echo.
    echo 或者直接下载：
    echo https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip
    echo.
    pause
    exit /b 1
)

echo ✅ ngrok 已安装
echo.

echo [步骤 2/4] 启动后端服务...
start "AI Job Backend" cmd /k "cd /d %~dp0 && python main.py --port 8765"
timeout /t 3 >nul

echo ✅ 后端服务已启动
echo.

echo [步骤 3/4] 启动 ngrok 隧道...
start "Ngrok Tunnel" cmd /k "ngrok http 8765"
timeout /t 5 >nul

echo ✅ ngrok 隧道已启动
echo.

echo [步骤 4/4] 获取公网地址...
echo.
echo ========================================
echo   🎉 部署完成！
echo ========================================
echo.
echo 📋 下一步操作：
echo.
echo 1. 查看 ngrok 窗口，找到类似这样的地址：
echo    https://xxxx-xx-xx-xx-xx.ngrok-free.app
echo.
echo 2. 复制这个地址
echo.
echo 3. 修改 ai-job-helper/streamlit_app.py 第 19 行：
echo    BACKEND_URL = "你复制的地址"
echo.
echo 4. 推送到 GitHub：
echo    cd ai-job-helper
echo    git add streamlit_app.py
echo    git commit -m "Update backend URL"
echo    git push
echo.
echo 5. 等待 Streamlit Cloud 部署完成（1-2分钟）
echo.
echo ========================================
echo.
echo 💡 提示：
echo    - 保持这两个窗口打开
echo    - 用户现在可以通过网站使用你的服务了
echo    - 按任意键关闭此窗口
echo.
pause

