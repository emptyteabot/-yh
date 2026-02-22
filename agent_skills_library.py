"""
Agent技能库 - 可复用的技能模块
每个技能都是独立的，可以被任何Agent调用
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from typing import Dict, List
import re


class WebScrapingSkill:
    """网页爬取技能"""
    
    @staticmethod
    async def scrape_with_requests(url: str):
        """使用requests爬取"""
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            return {
                "success": True,
                "content": response.text,
                "status_code": response.status_code
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def extract_emails_from_text(text: str):
        """从文本中提取邮箱"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return list(set(emails))  # 去重
    
    @staticmethod
    async def extract_links(html: str, base_url: str):
        """提取所有链接"""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http'):
                links.append(href)
            elif href.startswith('/'):
                links.append(base_url + href)
        return links


class EmailFinderSkill:
    """邮箱查找技能"""
    
    @staticmethod
    async def guess_email_formats(domain: str, name: str = None):
        """推测邮箱格式"""
        formats = [
            f"hello@{domain}",
            f"contact@{domain}",
            f"info@{domain}",
            f"sales@{domain}",
            f"support@{domain}",
            f"team@{domain}"
        ]
        
        if name:
            first, last = name.split()[0], name.split()[-1]
            formats.extend([
                f"{first.lower()}@{domain}",
                f"{first.lower()}.{last.lower()}@{domain}",
                f"{first[0].lower()}{last.lower()}@{domain}"
            ])
        
        return formats
    
    @staticmethod
    async def verify_email_format(email: str):
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    async def find_email_from_website(url: str):
        """从网站查找邮箱"""
        try:
            response = requests.get(url, timeout=10)
            emails = await WebScrapingSkill.extract_emails_from_text(response.text)
            return emails
        except:
            return []


class EmailGenerationSkill:
    """邮件生成技能"""
    
    @staticmethod
    async def generate_cold_email(company_info: Dict, template: str = "default"):
        """生成冷邮件"""
        company = company_info.get("company", "Company")
        
        templates = {
            "default": {
                "subject": f"帮助 {company} 节省50%算力成本",
                "body": f"""Hi {company} team,

我注意到你们在AI领域的工作。

我们专门帮助新加坡AI初创企业：
✅ 解锁 $250K+ 云信用额度
✅ 节省50%+算力成本
✅ 申请政府AI补贴（$80K-$200K）

感兴趣的话，我可以为你准备免费的成本审计报告。

Best regards,
[Your Name]
"""
            },
            "short": {
                "subject": f"快速问题 - {company}",
                "body": f"""Hi,

你们目前的算力成本是多少？

我们帮助AI公司节省50%+成本。

5分钟电话即可了解。

Best,
[Your Name]
"""
            },
            "value_first": {
                "subject": f"免费成本审计 - {company}",
                "body": f"""Hi {company} team,

我们为新加坡AI公司提供免费的算力成本审计。

通常能发现$50K+/年的节省机会。

需要吗？

Best,
[Your Name]
"""
            }
        }
        
        return templates.get(template, templates["default"])
    
    @staticmethod
    async def generate_followup_email(original_email: Dict, day: int):
        """生成跟进邮件"""
        company = original_email.get("company", "")
        
        if day == 3:
            return {
                "subject": f"Re: {original_email['subject']}",
                "body": f"""Hi {company} team,

上次邮件不知道你看到没有？

我们的客户平均节省了50%+的算力成本。

感兴趣吗？

Best,
[Your Name]
"""
            }
        elif day == 7:
            return {
                "subject": f"Re: {original_email['subject']}",
                "body": f"""Hi {company} team,

最后一次打扰。

如果感兴趣，本周可以安排15分钟电话。

Best,
[Your Name]
"""
            }
        else:
            return {
                "subject": f"Re: {original_email['subject']}",
                "body": f"""Hi {company} team,

理解你可能很忙。

如果未来有需要，随时联系我。

Best,
[Your Name]
"""
            }


class ProposalGenerationSkill:
    """提案生成技能"""
    
    @staticmethod
    async def generate_proposal(company_info: Dict, services: List[str]):
        """生成提案"""
        company = company_info.get("company", "Company")
        
        proposal = f"""# {company} - 算力优化与政府补贴方案

## 执行摘要
为 {company} 准备的完整成本优化方案。

## 服务内容

### 1. 云信用额度解锁
- Google Cloud: $250,000
- AWS Activate: $100,000
- Azure: $25,000
- **费用: 解锁金额的15%（成功后付费）**

### 2. 多云成本优化
- 预期节省: 50%+
- **费用: 节省金额的40%**

### 3. 政府补贴申请
- 预期补贴: $80K-$200K
- **费用: 补贴金额的25%**

## 投资回报
**总价值: $575K+**
**总费用: $113K**
**净收益: $462K+**
**ROI: 409%**

## 付款条款
成功后付费

**有效期: 7天**
"""
        
        return proposal
    
    @staticmethod
    async def calculate_roi(investment: float, return_value: float):
        """计算ROI"""
        roi = ((return_value - investment) / investment) * 100
        return {
            "investment": investment,
            "return": return_value,
            "profit": return_value - investment,
            "roi_percentage": round(roi, 2)
        }


class DataManagementSkill:
    """数据管理技能"""
    
    @staticmethod
    async def save_to_json(data: Dict, filepath: str):
        """保存到JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return {"success": True, "filepath": filepath}
    
    @staticmethod
    async def load_from_json(filepath: str):
        """从JSON加载"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    
    @staticmethod
    async def append_to_log(log_entry: Dict, log_file: str):
        """追加到日志"""
        logs = await DataManagementSkill.load_from_json(log_file) or []
        logs.append({
            **log_entry,
            "timestamp": datetime.now().isoformat()
        })
        await DataManagementSkill.save_to_json(logs, log_file)


class APIIntegrationSkill:
    """API集成技能"""
    
    @staticmethod
    async def call_hunter_io(domain: str, api_key: str):
        """调用Hunter.io API"""
        try:
            url = "https://api.hunter.io/v2/domain-search"
            params = {"domain": domain, "api_key": api_key}
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    async def call_sendgrid(to_email: str, subject: str, content: str, api_key: str):
        """调用SendGrid API"""
        try:
            url = "https://api.sendgrid.com/v3/mail/send"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "personalizations": [{"to": [{"email": to_email}]}],
                "from": {"email": "your-email@domain.com"},
                "subject": subject,
                "content": [{"type": "text/html", "value": content}]
            }
            response = requests.post(url, headers=headers, json=data)
            return {"success": response.status_code == 202}
        except Exception as e:
            return {"error": str(e)}


class AnalyticsSkill:
    """分析技能"""
    
    @staticmethod
    async def calculate_conversion_rate(total: int, converted: int):
        """计算转化率"""
        if total == 0:
            return 0
        return round((converted / total) * 100, 2)
    
    @staticmethod
    async def analyze_email_campaign(sent: int, opened: int, replied: int, meetings: int):
        """分析邮件活动"""
        return {
            "sent": sent,
            "open_rate": await AnalyticsSkill.calculate_conversion_rate(sent, opened),
            "reply_rate": await AnalyticsSkill.calculate_conversion_rate(sent, replied),
            "meeting_rate": await AnalyticsSkill.calculate_conversion_rate(replied, meetings)
        }
    
    @staticmethod
    async def predict_revenue(leads: int, conversion_rate: float, avg_deal_size: float):
        """预测收入"""
        expected_deals = leads * (conversion_rate / 100)
        expected_revenue = expected_deals * avg_deal_size
        return {
            "leads": leads,
            "conversion_rate": conversion_rate,
            "expected_deals": round(expected_deals, 2),
            "avg_deal_size": avg_deal_size,
            "expected_revenue": round(expected_revenue, 2)
        }


# 技能注册表
SKILL_REGISTRY = {
    "web_scraping": WebScrapingSkill,
    "email_finder": EmailFinderSkill,
    "email_generation": EmailGenerationSkill,
    "proposal_generation": ProposalGenerationSkill,
    "data_management": DataManagementSkill,
    "api_integration": APIIntegrationSkill,
    "analytics": AnalyticsSkill
}


def get_skill(skill_name: str):
    """获取技能"""
    return SKILL_REGISTRY.get(skill_name)


if __name__ == "__main__":
    print("="*70)
    print("🛠️ Agent技能库")
    print("="*70)
    print("\n可用技能:")
    for name, skill_class in SKILL_REGISTRY.items():
        print(f"  ✅ {name}: {skill_class.__doc__}")
    print("\n每个Agent都可以调用这些技能！")

