@echo off
chcp 65001 >nul
title AI求职助手 - 云端服务一键启动

echo ========================================
echo   AI 求职助手 - 云端服务一键启动
echo ========================================
echo.
echo 正在启动服务，请稍候...
echo.

echo [1/2] 启动后端服务...
start "AI求职助手-后端服务" cmd /k "cd /d %~dp0ai-job-applier-desktop\backend && python main.py --port 8765"

echo 等待后端启动...
timeout /t 5 /nobreak >nul

echo.
echo [2/2] 启动 ngrok 内网穿透...
start "AI求职助手-ngrok" cmd /k "cd /d %USERPROFILE%\Desktop && ngrok http 8765"

echo.
echo ========================================
echo 云端服务启动完成！
echo ========================================
echo.
echo 📋 下一步操作：
echo.
echo 1. 在 ngrok 窗口中找到 Forwarding 地址
echo    格式：https://abc123.ngrok.io
echo.
echo 2. 复制这个地址
echo.
echo 3. 打开 streamlit_app.py 文件
echo    找到第 12 行：API_URL = "https://your-domain.ngrok.io"
echo    替换成你的 ngrok 地址
echo.
echo 4. 推送到 GitHub
echo.
echo 5. 访问 Streamlit 应用测试
echo    https://ai-job-apper-ibpzap2nnajzrnu8mkthuv.streamlit.app/
echo.
echo ========================================
echo.
echo 💡 提示：
echo - 保持这两个窗口一直开着
echo - 关闭任何一个，服务就会中断
echo - 电脑不要关机或休眠
echo.
echo ========================================
pause

