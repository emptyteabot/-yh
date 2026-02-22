@echo off
chcp 65001 >nul
title 推送到 GitHub

echo ========================================
echo   推送 streamlit_app.py 到 GitHub
echo ========================================
echo.

cd /d "C:\Users\陈盈桦\Desktop\Desktop_整理_2026-02-09_172732\Folders\自动投简历"

echo [1/4] 复制新文件...
copy /Y "C:\Users\陈盈桦\Desktop\一人公司260222\streamlit_app.py" "streamlit_app.py"

echo.
echo [2/4] 添加到 Git...
git add streamlit_app.py

echo.
echo [3/4] 提交更改...
git commit -m "添加自动投递功能 - 集成云端后端"

echo.
echo [4/4] 推送到 GitHub...
git push

echo.
echo ========================================
echo 推送完成！
echo ========================================
echo.
echo Streamlit Cloud 会在 1-2 分钟内自动重新部署
echo.
echo 访问：https://ai-job-apper-ibpzap2nnajzrnu8mkthuv.streamlit.app/
echo.
echo ========================================
pause

