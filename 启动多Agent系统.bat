@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 启动多Agent协作系统
echo ========================================
echo.
echo 6个Agent将自动执行30天客户获取计划
echo.
python multi_agent_system.py
echo.
echo ========================================
echo ✅ 执行完成！
echo ========================================
echo.
echo 查看结果：multi_agent_output 文件夹
echo.
pause

