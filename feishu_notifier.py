"""
飞书实时通知 - 监控收单进度
"""

import requests
import json
from datetime import datetime

class FeishuNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
    
    def send_order_notification(self, user_name, amount, platform):
        """发送收单通知"""
        msg = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": "💰 新订单！"
                    },
                    "template": "green"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**用户：** {user_name}\n**金额：** ¥{amount}\n**来源：** {platform}\n**时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "立刻处理"
                                },
                                "type": "primary"
                            }
                        ]
                    }
                ]
            }
        }
        
        response = requests.post(self.webhook_url, json=msg)
        return response.status_code == 200
    
    def send_traffic_report(self, views, comments, wechat_adds):
        """发送流量报告"""
        msg = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": "📊 2小时流量报告"
                    },
                    "template": "blue"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**浏览量：** {views}\n**评论数：** {comments}\n**加微信：** {wechat_adds}\n\n{'✅ 数据正常' if views >= 100 else '⚠️ 浏览量过低，建议重发'}"
                        }
                    }
                ]
            }
        }
        
        response = requests.post(self.webhook_url, json=msg)
        return response.status_code == 200
    
    def send_delivery_reminder(self, user_name):
        """发送交付提醒"""
        msg = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": "⏰ 交付提醒"
                    },
                    "template": "orange"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**用户：** {user_name}\n**状态：** 已付款，等待交付\n**承诺时间：** 30分钟内"
                        }
                    }
                ]
            }
        }
        
        response = requests.post(self.webhook_url, json=msg)
        return response.status_code == 200

# 使用示例
if __name__ == "__main__":
    webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/6d05605e-13e9-469e-b060-bda1a168b96a"
    notifier = FeishuNotifier(webhook)
    
    # 测试通知
    notifier.send_order_notification("张三", 19.9, "小红书")
    print("✅ 飞书通知已发送")


