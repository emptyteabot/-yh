@echo off
chcp 65001 >nul
echo ========================================
echo AI 求职助手 - 一键打包脚本
echo ========================================
echo.

echo [步骤 1/5] 检查环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 Python
    echo 请先安装 Python 3.10+
    pause
    exit /b 1
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 Node.js
    echo 请先安装 Node.js 18+
    pause
    exit /b 1
)

echo ✅ 环境检查通过
echo.

echo [步骤 2/5] 打包 Python 后端...
cd backend

REM 安装 PyInstaller
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo 安装 PyInstaller...
    pip install pyinstaller
)

REM 清理旧文件
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM 打包
echo 正在打包后端...
pyinstaller build.spec --clean --noconfirm

if %errorlevel% neq 0 (
    echo ❌ 后端打包失败
    cd ..
    pause
    exit /b 1
)

echo ✅ 后端打包完成
cd ..
echo.

echo [步骤 3/5] 安装前端依赖...
cd electron

if not exist node_modules (
    echo 安装 npm 依赖...
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        cd ..
        pause
        exit /b 1
    )
)

echo ✅ 依赖安装完成
echo.

echo [步骤 4/5] 构建前端...
echo 正在构建前端...
call npm run build

if %errorlevel% neq 0 (
    echo ❌ 前端构建失败
    cd ..
    pause
    exit /b 1
)

echo ✅ 前端构建完成
echo.

echo [步骤 5/5] 打包 Electron 应用...
echo 正在打包应用...
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
echo ========================================
echo.
echo 输出文件位置:
echo   build\AI求职助手 Setup 1.0.0.exe
echo.
echo 安装包大小: 约 150-200 MB
echo.
echo 使用说明:
echo 1. 双击安装包进行安装
echo 2. 安装完成后会自动创建桌面快捷方式
echo 3. 双击快捷方式启动应用
echo.
echo ========================================

pause
