"""
飞书机器人 - 控制AI员工接单赚钱
"""
import requests
import json
from datetime import datetime
from loguru import logger

class FeishuBot:
    """飞书机器人"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        logger.info("🤖 飞书机器人已初始化")
    
    def send_text(self, text: str):
        """发送文本消息"""
        data = {
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
        response = requests.post(self.webhook_url, json=data)
        return response.json()
    
    def send_card(self, title: str, content: str, color: str = "blue"):
        """发送卡片消息"""
        data = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": title
                    },
                    "template": color
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "plain_text",
                            "content": content
                        }
                    }
                ]
            }
        }
        response = requests.post(self.webhook_url, json=data)
        return response.json()
    
    def notify_task_start(self, task_type: str, description: str):
        """通知任务开始"""
        text = f"""
🚀 新任务开始

类型: {task_type}
描述: {description}
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

AI员工正在处理中...
"""
        return self.send_text(text)
    
    def notify_task_complete(self, task_type: str, result: dict):
        """通知任务完成"""
        text = f"""
✅ 任务完成！

类型: {task_type}
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

结果摘要:
{self._format_result(result)}

💰 可以交付给客户了！
"""
        return self.send_text(text)
    
    def notify_money_earned(self, amount: float, task: str):
        """通知赚钱了"""
        text = f"""
💰💰💰 收款通知！

任务: {task}
金额: ${amount}
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

继续加油！🚀
"""
        return self.send_card("收款通知", text, "green")
    
    def _format_result(self, result: dict) -> str:
        """格式化结果"""
        if isinstance(result, dict):
            lines = []
            for key, value in result.items():
                if isinstance(value, (str, int, float)):
                    lines.append(f"• {key}: {value}")
            return '\n'.join(lines[:5])  # 只显示前5行
        return str(result)[:200]  # 限制长度


# ============================================
# 快速接单脚本（不要架构，直接干）
# ============================================

def scrape_and_notify(url: str, webhook_url: str):
    """抓取数据并通知飞书"""
    bot = FeishuBot(webhook_url)
    
    # 通知开始
    bot.notify_task_start("网页抓取", f"抓取 {url}")
    
    # 执行抓取（这里用最简单的方式）
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 简单示例：抓取所有链接
        links = []
        for a in soup.find_all('a', href=True):
            links.append({
                'text': a.text.strip(),
                'url': a['href']
            })
        
        # 保存
        df = pd.DataFrame(links)
        output_file = f'scraped_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        df.to_csv(output_file, index=False)
        
        # 通知完成
        result = {
            'status': 'success',
            'total_items': len(links),
            'output_file': output_file
        }
        bot.notify_task_complete("网页抓取", result)
        
        return output_file
        
    except Exception as e:
        bot.send_text(f"❌ 任务失败: {str(e)}")
        return None


def clean_data_and_notify(input_file: str, webhook_url: str):
    """清洗数据并通知飞书"""
    bot = FeishuBot(webhook_url)
    
    # 通知开始
    bot.notify_task_start("数据清洗", f"清洗 {input_file}")
    
    try:
        import pandas as pd
        
        # 读取
        df = pd.read_csv(input_file)
        original_count = len(df)
        
        # 清洗
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        df = df.fillna('')
        
        # 保存
        output_file = input_file.replace('.csv', '_cleaned.csv')
        df.to_csv(output_file, index=False)
        
        # 通知完成
        result = {
            'status': 'success',
            'original_rows': original_count,
            'cleaned_rows': len(df),
            'removed_rows': original_count - len(df),
            'output_file': output_file
        }
        bot.notify_task_complete("数据清洗", result)
        
        return output_file
        
    except Exception as e:
        bot.send_text(f"❌ 任务失败: {str(e)}")
        return None


# ============================================
# 使用示例
# ============================================

if __name__ == "__main__":
    # 配置飞书Webhook
    WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/你的webhook"
    
    # 示例1：抓取数据
    # scrape_and_notify("https://example.com", WEBHOOK_URL)
    
    # 示例2：清洗数据
    # clean_data_and_notify("input.csv", WEBHOOK_URL)
    
    # 示例3：通知赚钱
    bot = FeishuBot(WEBHOOK_URL)
    bot.notify_money_earned(50, "Upwork网页抓取任务")
    
    print("飞书机器人测试完成！")


