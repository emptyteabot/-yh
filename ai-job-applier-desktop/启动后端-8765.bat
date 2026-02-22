@echo off
chcp 65001
cd /d "%~dp0backend"
echo 正在启动后端服务 (端口 8765)...
python main.py --port 8765
pause

