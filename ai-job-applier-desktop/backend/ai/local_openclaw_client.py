"""
本地 OpenClaw 客户端
用于 Streamlit 调用本地 OpenClaw 服务
"""

import requests
import time
from typing import Dict, Any


class LocalOpenClawClient:
    """本地 OpenClaw 客户端"""

    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url

    def check_health(self) -> bool:
        """检查本地服务是否运行"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False

    def send_apply_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """发送投递任务到本地服务"""
        try:
            response = requests.post(
                f"{self.base_url}/apply",
                json=task_data,
                timeout=5
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}"
                }

        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': '无法连接到本地服务，请确保 local_openclaw_service.py 正在运行'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """查询任务状态"""
        try:
            response = requests.get(
                f"{self.base_url}/status/{task_id}",
                timeout=5
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'error': '任务不存在'
                }

        except Exception as e:
            return {
                'error': str(e)
            }


# 全局实例
local_openclaw_client = LocalOpenClawClient()
