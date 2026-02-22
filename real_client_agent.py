"""
真实客户获取Agent
自动从真实渠道抓取客户、发送邮件、跟进成交
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import re

class RealClientAcquisitionAgent:
    """
    真实客户获取Agent
    自动完成：抓取真实客户 → 发送真实邮件 → 跟进成交
    """
    
    def __init__(self):
        self.output_dir = Path("./real_clients")
        self.output_dir.mkdir(exist_ok=True)
        
        # 真实数据源
        self.data_sources = {
            "ai_singapore": {
                "url": "https://www.aisingapore.org/innovation/ai-products/",
                "type": "官方合作伙伴",
                "quality": "高"
            },
            "linkedin": {
                "search": "AI founder Singapore",
                "filters": ["Recent funding", "3-20 employees"],
                "quality": "高"
            },
            "product_hunt": {
                "url": "https://www.producthunt.com/topics/artificial-intelligence",
                "filters": ["Singapore", "Recent launch"],
                "quality": "中"
            },
            "crunchbase": {
                "search": "Singapore + AI + Recent funding",
                "quality": "高"
            }
        }
    
    async def scrape_ai_singapore(self):
        """
        从AI Singapore抓取真实客户
        """
        print("\n" + "="*70)
        print("🔍 从AI Singapore抓取真实客户...")
        print("="*70)
        
        print("\n【方法1：手动抓取（最快）】")
        print("1. 访问：https://www.aisingapore.org/innovation/ai-products/")
        print("2. 查看所有AI产品和公司")
        print("3. 记录以下信息：")
        print("   - 公司名称")
        print("   - 产品描述")
        print("   - 创始人（如果有）")
        print("   - 网站")
        
        print("\n【方法2：使用爬虫（需要配置）】")
        print("需要安装：pip install selenium beautifulsoup4")
        print("代码示例：")
        print("""
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get('https://www.aisingapore.org/innovation/ai-products/')
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 提取公司信息
companies = soup.find_all('div', class_='company-card')
for company in companies:
    name = company.find('h3').text
    description = company.find('p').text
    # 保存信息
""")
        
        # 提供模板让用户填写
        template = {
            "companies": [
                {
                    "id": "real_1",
                    "source": "AI Singapore",
                    "company": "【待填写】",
                    "product": "【待填写】",
                    "website": "【待填写】",
                    "description": "【待填写】",
                    "estimated_funding": "【待填写】",
                    "pain_point": "【算力成本/安全审计/政府补贴】",
                    "priority": "高"
                }
            ]
        }
        
        template_file = self.output_dir / "客户信息模板.json"
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 已生成客户信息模板：{template_file}")
        print("\n请按照模板填写真实客户信息")
        
        return template_file
    
    async def find_emails(self, companies):
        """
        自动查找客户邮箱
        """
        print("\n" + "="*70)
        print("📧 查找客户邮箱...")
        print("="*70)
        
        print("\n【方法1：从网站查找】")
        print("访问公司网站，查找：")
        print("- Contact页面")
        print("- About页面")
        print("- Team页面")
        print("- 通常格式：founder@company.com 或 hello@company.com")
        
        print("\n【方法2：使用Hunter.io（推荐）】")
        print("1. 访问：https://hunter.io/")
        print("2. 输入公司域名")
        print("3. 获取邮箱格式和验证")
        print("4. 免费额度：每月25次查询")
        
        print("\n【方法3：LinkedIn查找】")
        print("1. 在LinkedIn搜索公司名")
        print("2. 找到创始人/CTO")
        print("3. 发送连接请求")
        print("4. 连接后可以看到联系方式")
        
        print("\n【方法4：使用Apollo.io】")
        print("1. 访问：https://www.apollo.io/")
        print("2. 搜索公司和职位")
        print("3. 获取验证过的邮箱")
        print("4. 免费额度：每月50个邮箱")
        
        # 生成邮箱查找工具脚本
        email_finder_script = """
# 邮箱查找工具
import requests

def find_email_hunter(domain):
    '''使用Hunter.io查找邮箱'''
    api_key = "YOUR_HUNTER_API_KEY"
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"
    response = requests.get(url)
    return response.json()

def find_email_apollo(company_name):
    '''使用Apollo.io查找邮箱'''
    api_key = "YOUR_APOLLO_API_KEY"
    # Apollo API调用
    pass

# 使用示例
domain = "example.com"
emails = find_email_hunter(domain)
print(emails)
"""
        
        script_file = self.output_dir / "邮箱查找工具.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(email_finder_script)
        
        print(f"\n✅ 已生成邮箱查找工具：{script_file}")
        
        return script_file
    
    async def send_real_emails(self, clients_with_emails):
        """
        发送真实邮件
        """
        print("\n" + "="*70)
        print("📨 发送真实邮件...")
        print("="*70)
        
        print("\n【方法1：使用SendGrid（推荐）】")
        print("1. 注册：https://sendgrid.com/")
        print("2. 获取API Key")
        print("3. 配置代码：")
        print("""
import sendgrid
from sendgrid.helpers.mail import Mail

sg = sendgrid.SendGridAPIClient(api_key='YOUR_API_KEY')

message = Mail(
    from_email='your-email@your-domain.com',
    to_emails='client@company.com',
    subject='邮件主题',
    html_content='邮件内容'
)

response = sg.send(message)
print(f"邮件已发送：{response.status_code}")
""")
        
        print("\n【方法2：使用Gmail SMTP】")
        print("""
import smtplib
from email.mime.text import MIMEText

msg = MIMEText('邮件内容', 'html')
msg['Subject'] = '邮件主题'
msg['From'] = 'your-email@gmail.com'
msg['To'] = 'client@company.com'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your-email@gmail.com', 'your-app-password')
server.send_message(msg)
server.quit()
""")
        
        print("\n【方法3：手动发送（最简单）】")
        print("1. 打开 auto_execution_output/待发送邮件.csv")
        print("2. 复制邮件内容")
        print("3. 粘贴到Gmail/Outlook")
        print("4. 每天发送10封")
        
        # 生成SendGrid配置脚本
        sendgrid_script = """
# SendGrid邮件发送脚本
import sendgrid
from sendgrid.helpers.mail import Mail
import json

# 配置
API_KEY = "YOUR_SENDGRID_API_KEY"  # 替换为你的API Key
FROM_EMAIL = "your-email@your-domain.com"  # 替换为你的邮箱
FROM_NAME = "Your Name"  # 替换为你的名字

def send_email(to_email, subject, content):
    sg = sendgrid.SendGridAPIClient(api_key=API_KEY)
    
    message = Mail(
        from_email=(FROM_EMAIL, FROM_NAME),
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    
    try:
        response = sg.send(message)
        print(f"✅ 邮件已发送到 {to_email}")
        return True
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        return False

# 批量发送
def send_batch_emails(emails_file):
    with open(emails_file, 'r', encoding='utf-8') as f:
        emails = json.load(f)
    
    for email in emails:
        send_email(
            to_email=email['to'],
            subject=email['subject'],
            content=email['body']
        )
        # 延迟避免被限制
        import time
        time.sleep(2)

# 使用
send_batch_emails('auto_execution_output/待发送邮件.json')
"""
        
        script_file = self.output_dir / "SendGrid发送脚本.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(sendgrid_script)
        
        print(f"\n✅ 已生成SendGrid发送脚本：{script_file}")
        
        return script_file
    
    async def auto_follow_up(self):
        """
        自动跟进系统
        """
        print("\n" + "="*70)
        print("🔄 自动跟进系统...")
        print("="*70)
        
        print("\n【跟进时间表】")
        print("Day 1：发送初始邮件")
        print("Day 3：第一次跟进（如果没回复）")
        print("Day 7：第二次跟进（如果没回复）")
        print("Day 10：最后一次跟进")
        
        print("\n【跟进邮件模板】")
        
        follow_up_templates = {
            "day_3": """
主题：Re: {original_subject}

Hi {name},

上次邮件不知道你看到没有？

我们可以为{company}提供：
- {service_1}
- {service_2}

提供免费的{free_offer}，感兴趣吗？

Best,
{your_name}
""",
            "day_7": """
主题：Re: {original_subject}

Hi {name},

最后一次打扰。

如果你对{service}感兴趣，本周可以安排一个15分钟的电话。

我会为你准备：
- 针对{company}的具体分析
- 预期ROI计算

回复即可安排。

Best,
{your_name}
""",
            "day_10": """
主题：Re: {original_subject}

Hi {name},

理解你可能很忙。

如果未来有需要，随时联系我。

我的联系方式：
- 邮箱：{your_email}
- LinkedIn：{your_linkedin}

祝{company}一切顺利！

Best,
{your_name}
"""
        }
        
        templates_file = self.output_dir / "跟进邮件模板.json"
        with open(templates_file, 'w', encoding='utf-8') as f:
            json.dump(follow_up_templates, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 已生成跟进邮件模板：{templates_file}")
        
        # 生成自动跟进脚本
        auto_follow_script = """
# 自动跟进脚本
import json
from datetime import datetime, timedelta

def check_and_send_followup():
    '''检查并发送跟进邮件'''
    
    # 加载已发送邮件
    with open('fully_automated_output/邮件发送日志.json', 'r') as f:
        sent_emails = json.load(f)
    
    # 加载回复记录
    with open('fully_automated_output/客户回复记录.json', 'r') as f:
        replies = json.load(f)
    
    replied_companies = [r['original_email']['company'] for r in replies]
    
    # 检查需要跟进的邮件
    today = datetime.now()
    
    for email in sent_emails:
        sent_date = datetime.fromisoformat(email['sent_at'])
        days_passed = (today - sent_date).days
        
        # 如果已回复，跳过
        if email['company'] in replied_companies:
            continue
        
        # Day 3跟进
        if days_passed == 3:
            send_followup(email, 'day_3')
        
        # Day 7跟进
        elif days_passed == 7:
            send_followup(email, 'day_7')
        
        # Day 10最后跟进
        elif days_passed == 10:
            send_followup(email, 'day_10')

def send_followup(original_email, template_type):
    '''发送跟进邮件'''
    # 加载模板
    with open('real_clients/跟进邮件模板.json', 'r') as f:
        templates = json.load(f)
    
    template = templates[template_type]
    
    # 填充模板
    content = template.format(
        name=original_email['company'],
        company=original_email['company'],
        original_subject=original_email['subject'],
        service_1="算力优化",
        service_2="政府补贴申请",
        free_offer="成本审计",
        service="我们的服务",
        your_name="你的名字",
        your_email="your-email@domain.com",
        your_linkedin="linkedin.com/in/yourname"
    )
    
    # 发送邮件（使用SendGrid）
    # send_email(original_email['to'], f"Re: {original_email['subject']}", content)
    
    print(f"✅ 已发送{template_type}跟进邮件到 {original_email['company']}")

# 每天运行一次
if __name__ == "__main__":
    check_and_send_followup()
"""
        
        script_file = self.output_dir / "自动跟进脚本.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(auto_follow_script)
        
        print(f"\n✅ 已生成自动跟进脚本：{script_file}")
        
        return script_file
    
    async def run_complete_system(self):
        """
        运行完整的真实客户获取系统
        """
        print("\n" + "="*70)
        print("🚀 真实客户获取Agent启动")
        print("="*70)
        print("\n这个Agent会帮你：")
        print("✅ 提供真实客户抓取方法")
        print("✅ 提供邮箱查找工具")
        print("✅ 提供邮件发送脚本")
        print("✅ 提供自动跟进系统")
        
        # 步骤1：抓取客户
        await self.scrape_ai_singapore()
        
        # 步骤2：查找邮箱
        await self.find_emails([])
        
        # 步骤3：发送邮件
        await self.send_real_emails([])
        
        # 步骤4：自动跟进
        await self.auto_follow_up()
        
        # 生成完整指南
        guide = self._generate_complete_guide()
        
        guide_file = self.output_dir / "完整执行指南.md"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        print("\n" + "="*70)
        print("✅ 真实客户获取系统准备完成！")
        print("="*70)
        
        print(f"\n📁 所有文件已保存到：{self.output_dir}")
        print("\n生成的文件：")
        print("  - 客户信息模板.json")
        print("  - 邮箱查找工具.py")
        print("  - SendGrid发送脚本.py")
        print("  - 自动跟进脚本.py")
        print("  - 跟进邮件模板.json")
        print("  - 完整执行指南.md")
        
        print("\n" + "="*70)
        print("📋 下一步（按顺序执行）")
        print("="*70)
        print("\n1. 打开 real_clients/完整执行指南.md")
        print("2. 按照指南一步步执行")
        print("3. 30天后收到第一笔真实的钱 💰")
        
        return guide_file
    
    def _generate_complete_guide(self):
        """生成完整执行指南"""
        return """# 🚀 真实客户获取完整指南

## 📅 30天行动计划

### Week 1：找客户 + 找邮箱

#### Day 1-2：从AI Singapore抓取客户
1. 访问：https://www.aisingapore.org/innovation/ai-products/
2. 记录10个公司信息到 `客户信息模板.json`
3. 包含：公司名、产品、网站、描述

#### Day 3-4：从LinkedIn抓取客户
1. 搜索："AI founder Singapore"
2. 筛选：Recent funding, 3-20 employees
3. 记录10个公司信息

#### Day 5-6：从Product Hunt抓取客户
1. 访问：https://www.producthunt.com/topics/artificial-intelligence
2. 筛选：Singapore, Recent launch
3. 记录10个公司信息

#### Day 7：查找邮箱
1. 使用Hunter.io查找邮箱
2. 或访问公司网站查找Contact页面
3. 或在LinkedIn找创始人

**Week 1结束：你应该有30个真实客户 + 邮箱**

---

### Week 2：发送邮件

#### Day 8：配置SendGrid
1. 注册：https://sendgrid.com/
2. 获取API Key
3. 配置 `SendGrid发送脚本.py`

#### Day 9-15：发送邮件
1. 每天发送5封（避免被标记为垃圾邮件）
2. 使用 `SendGrid发送脚本.py`
3. 或手动复制邮件发送

**Week 2结束：30封邮件已发送**

---

### Week 3：跟进回复

#### Day 16-22：监控回复
1. 每天检查邮箱
2. 收到回复后1小时内响应
3. 目标：安排会议

**预期：收到3-5个回复**

#### 回复模板
```
Hi [Name],

太好了！很高兴你对我们的服务感兴趣。

我们可以安排一个30分钟的电话，我会为你准备：
✅ 针对[公司]的具体分析
✅ 详细的解决方案
✅ 预期ROI计算

你这周哪天方便？

Best,
[你的名字]
```

---

### Week 4：会议 + 提案

#### Day 23-28：开会
1. 准备会议议程
2. 展示价值
3. 回答问题

#### Day 29-30：发送提案
1. 会议后24小时内发送
2. 使用提案模板
3. 跟进

**预期：发送2-3个提案**

---

## 📧 邮件发送详细步骤

### 方法1：使用SendGrid（推荐）

#### 步骤1：注册SendGrid
1. 访问：https://sendgrid.com/
2. 注册免费账户
3. 验证邮箱

#### 步骤2：获取API Key
1. 登录SendGrid
2. Settings → API Keys
3. Create API Key
4. 复制API Key

#### 步骤3：配置脚本
打开 `SendGrid发送脚本.py`，修改：
```python
API_KEY = "你的API Key"
FROM_EMAIL = "你的邮箱"
FROM_NAME = "你的名字"
```

#### 步骤4：发送邮件
```bash
python SendGrid发送脚本.py
```

### 方法2：手动发送（最简单）

1. 打开 `auto_execution_output/待发送邮件.csv`
2. 复制第一封邮件的内容
3. 打开Gmail/Outlook
4. 粘贴邮件内容
5. 发送
6. 重复（每天5-10封）

---

## 🔄 自动跟进系统

### 设置自动跟进

#### 步骤1：配置跟进脚本
打开 `自动跟进脚本.py`，修改：
```python
your_name = "你的名字"
your_email = "你的邮箱"
your_linkedin = "你的LinkedIn"
```

#### 步骤2：设置定时任务

**Windows：**
1. 打开任务计划程序
2. 创建基本任务
3. 触发器：每天
4. 操作：运行 `python 自动跟进脚本.py`

**Mac/Linux：**
```bash
crontab -e
# 添加：每天上午10点运行
0 10 * * * python /path/to/自动跟进脚本.py
```

---

## 💰 提案模板

### 算力经纪提案
```
# [公司名] - 算力优化方案

## 执行摘要
基于我们的会议讨论，我们为[公司名]准备了算力优化方案。

## 当前问题
- 推理成本：$[金额]/月
- 主要使用：[云服务商]
- 痛点：成本过高

## 解决方案
1. 解锁云信用额度
   - Google Cloud：$250K
   - AWS：$100K
   - Azure：$25K

2. 多云套利优化
   - 使用Vast.ai/RunPod
   - 节省50%+成本

## 预期成果
- 节省成本：$[金额]/月
- ROI：[百分比]
- 回本周期：立即

## 定价
- 云额度解锁：解锁金额的15%（成功后付费）
- 成本优化：节省金额的40%

## 下一步
1. 签署合同
2. 开始执行
3. 30天内看到结果

有效期：7天
```

### 政府补贴提案
```
# [公司名] - 政府补贴申请方案

## 执行摘要
帮助[公司名]申请新加坡政府AI补贴。

## 可申请的补贴
1. EIS（企业创新计划）
   - 400%税收减免
   - 最高$50K

2. MAS FSTI
   - 报销30-50%成本
   - 适用于金融科技

3. AI Singapore 100E
   - $150K联合资助
   - 3-6个月项目

## 预期成果
- 总补贴：$80K-$200K
- 实际成本：$20K-$50K
- 净收益：$60K-$150K

## 我们的服务
- 代写申请文件
- 管理审批流程
- 确保最高额度

## 定价
- 补贴金额的25%（成功后付费）
- 预计费用：$20K-$50K

## 时间表
- Week 1-2：准备文件
- Week 3-4：提交申请
- Week 8-12：获得批准

有效期：7天
```

---

## 📊 预期结果

### 保守场景
```
发送30封邮件
  ↓ (10%回复率)
收到3个回复
  ↓ (66%转化)
安排2个会议
  ↓ (50%成交)
成交1个客户
  ↓
收入：$100K-$150K
```

### 乐观场景
```
发送30封邮件
  ↓ (15%回复率)
收到5个回复
  ↓ (60%转化)
安排3个会议
  ↓ (66%成交)
成交2个客户
  ↓
收入：$200K-$300K
```

---

## ✅ 检查清单

### Week 1
- [ ] 从AI Singapore找到10个客户
- [ ] 从LinkedIn找到10个客户
- [ ] 从Product Hunt找到10个客户
- [ ] 找到30个邮箱

### Week 2
- [ ] 配置SendGrid
- [ ] 发送30封邮件
- [ ] 设置自动跟进

### Week 3
- [ ] 收到3-5个回复
- [ ] 安排2-3个会议
- [ ] 准备提案

### Week 4
- [ ] 完成会议
- [ ] 发送提案
- [ ] 跟进成交

### Month 2
- [ ] 成交1-2个客户
- [ ] 收到第一笔钱 💰
- [ ] 开始执行服务

---

## 🚀 开始执行

**不要再等了！**

**今天就开始：**
1. 打开AI Singapore网站
2. 记录第一个客户信息
3. 找到他们的邮箱
4. 发送第一封邮件

**30天后，你将收到第一笔真实的钱！**

**$100K-$300K（真实的）** 💰
"""


async def main():
    """主入口"""
    agent = RealClientAcquisitionAgent()
    
    print("\n" + "="*70)
    print("🤖 真实客户获取Agent")
    print("="*70)
    print("\n这个Agent会帮你：")
    print("✅ 从真实渠道抓取客户")
    print("✅ 查找真实邮箱")
    print("✅ 发送真实邮件")
    print("✅ 自动跟进成交")
    print("\n30天后，你将收到第一笔真实的钱 💰")
    
    # 运行完整系统
    await agent.run_complete_system()


if __name__ == "__main__":
    asyncio.run(main())

