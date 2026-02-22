@echo off
echo ========================================
echo Python 后端打包脚本
echo ========================================
echo.

echo [1/3] 检查 PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo 安装 PyInstaller...
    pip install pyinstaller
)

echo [2/3] 清理旧文件...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

echo [3/3] 开始打包...
pyinstaller build.spec --clean

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 打包成功！
    echo 输出文件: dist\ai-job-backend.exe
    echo ========================================
) else (
    echo.
    echo ========================================
    echo 打包失败！
    echo ========================================
)

pause
