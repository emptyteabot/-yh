@echo off
chcp 65001 >nul
echo ========================================
echo AI 求职助手 - 快速打包
echo （假设依赖已安装）
echo ========================================
echo.

echo [1/3] 打包 Python 后端...
cd backend
pyinstaller build.spec --clean --noconfirm
if %errorlevel% neq 0 (
    echo ❌ 后端打包失败
    cd ..
    pause
    exit /b 1
)
cd ..
echo ✅ 后端打包完成
echo.

echo [2/3] 构建前端...
cd electron
call npm run build
if %errorlevel% neq 0 (
    echo ❌ 前端构建失败
    cd ..
    pause
    exit /b 1
)
echo ✅ 前端构建完成
echo.

echo [3/3] 打包应用...
call npm run electron:build
if %errorlevel% neq 0 (
    echo ❌ 应用打包失败
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo ✅ 打包完成！
echo 输出: build\AI求职助手 Setup 1.0.0.exe
echo ========================================
pause
