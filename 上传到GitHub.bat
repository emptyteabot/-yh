@echo off
chcp 65001 >nul
title 上传到 GitHub

echo ========================================
echo   上传 streamlit_app.py 到 GitHub
echo ========================================
echo.

echo 请按照以下步骤操作：
echo.
echo 1. 打开浏览器，访问：
echo    https://github.com/emptyteabot/ai-job-helper
echo.
echo 2. 如果有 streamlit_app.py 文件：
echo    - 点击文件
echo    - 点击右上角 ✏️ 编辑按钮
echo    - 删除所有内容
echo.
echo    如果没有这个文件：
echo    - 点击 "Add file"
echo    - 选择 "Create new file"
echo    - 文件名输入：streamlit_app.py
echo.
echo 3. 打开文件：
echo    C:\Users\陈盈桦\Desktop\一人公司260222\streamlit_app.py
echo.
echo 4. 全选（Ctrl+A）并复制（Ctrl+C）
echo.
echo 5. 回到 GitHub 网页，粘贴（Ctrl+V）
echo.
echo 6. 滚动到页面底部，点击 "Commit changes"
echo.
echo 7. 等待 1-2 分钟，访问：
echo    https://ai-job-apper-ibpzap2nnajzrnu8mkthuv.streamlit.app/
echo.
echo ========================================
echo.
echo 按任意键打开文件位置...
pause >nul

explorer "C:\Users\陈盈桦\Desktop\一人公司260222"

echo.
echo 按任意键打开 GitHub 网页...
pause >nul

start https://github.com/emptyteabot/ai-job-helper

echo.
echo 完成后，按任意键打开 Streamlit 应用...
pause >nul

start https://ai-job-apper-ibpzap2nnajzrnu8mkthuv.streamlit.app/

echo.
echo ========================================
echo 完成！
echo ========================================
pause

