"""
立刻赚钱行动计划 - 停止架构自嗨，去完成第一笔交易
"""

# ============================================
# 现实检查
# ============================================

REALITY_CHECK = """
❌ 错误方向：
- 构建完美的底层架构
- 做通用的AI员工平台
- 卖给其他创业者

✅ 正确方向：
- 用AI员工为自己接单赚钱
- 专注数据处理和极速交付
- Upwork/Fiverr接单变现

核心：客户不为代码买单，只为结果买单！
"""

# ============================================
# 立刻可接的单子类型（30-100美元）
# ============================================

MONEY_MAKING_TASKS = {
    "Web Scraping（网页抓取）": {
        "关键词": "web scraping, data extraction, scrape website",
        "预算": "$30-100",
        "交付时间": "24-48小时",
        "工具": "Python + BeautifulSoup + Selenium",
        "示例任务": [
            "抓取电商网站产品数据（标题、价格、评分）",
            "抓取LinkedIn联系人信息",
            "抓取房地产网站房源数据",
            "抓取社交媒体帖子和评论"
        ],
        "竞争优势": "提供10%样本数据，证明已跑通",
        "交付物": "CSV文件 + 简单文档"
    },
    
    "Data Cleaning（数据清洗）": {
        "关键词": "data cleaning, data processing, excel cleanup",
        "预算": "$30-80",
        "交付时间": "12-24小时",
        "工具": "Python + Pandas",
        "示例任务": [
            "清洗Excel表格（去重、格式化、填充缺失值）",
            "合并多个CSV文件",
            "数据标准化和验证",
            "删除重复联系人"
        ],
        "竞争优势": "1小时内交付样本",
        "交付物": "清洗后的Excel/CSV"
    },
    
    "Data Entry（数据录入）": {
        "关键词": "data entry, copy paste, manual data entry",
        "预算": "$20-50",
        "交付时间": "6-12小时",
        "工具": "Python自动化脚本",
        "示例任务": [
            "从PDF提取数据到Excel",
            "从图片识别文字录入",
            "批量复制粘贴数据",
            "表格数据迁移"
        ],
        "竞争优势": "用AI自动化，速度快10倍",
        "交付物": "Excel/Google Sheets"
    },
    
    "Lead Generation（线索生成）": {
        "关键词": "lead generation, email list, contact list",
        "预算": "$50-150",
        "交付时间": "24-48小时",
        "工具": "Python + Apollo.io API + Hunter.io",
        "示例任务": [
            "生成特定行业的公司联系人列表",
            "找到决策者的邮箱和LinkedIn",
            "验证邮箱有效性",
            "按地区/行业筛选潜在客户"
        ],
        "竞争优势": "提供验证过的高质量数据",
        "交付物": "CSV文件（公司名、联系人、邮箱、LinkedIn）"
    },
    
    "SEO Research（SEO研究）": {
        "关键词": "keyword research, competitor analysis, seo audit",
        "预算": "$40-100",
        "交付时间": "12-24小时",
        "工具": "Python + Ahrefs API / Semrush",
        "示例任务": [
            "关键词研究和搜索量分析",
            "竞品网站分析",
            "外链机会挖掘",
            "技术SEO审计"
        ],
        "竞争优势": "自动化报告生成",
        "交付物": "Excel报告 + 可视化图表"
    }
}

# ============================================
# 极简交付脚本（不要架构，直接干）
# ============================================

QUICK_SCRIPTS = {
    "web_scraping_template.py": """
# 网页抓取模板 - 单文件，直接跑
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_products(url, max_pages=5):
    results = []
    
    for page in range(1, max_pages + 1):
        print(f"抓取第 {page} 页...")
        
        response = requests.get(f"{url}?page={page}")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据实际网站调整选择器
        products = soup.find_all('div', class_='product-item')
        
        for product in products:
            title = product.find('h3').text.strip()
            price = product.find('span', class_='price').text.strip()
            rating = product.find('span', class_='rating').text.strip()
            
            results.append({
                'title': title,
                'price': price,
                'rating': rating
            })
        
        time.sleep(1)  # 礼貌延迟
    
    return results

# 执行
url = "https://example.com/products"
data = scrape_products(url)

# 保存
df = pd.DataFrame(data)
df.to_csv('scraped_data.csv', index=False)
print(f"完成！抓取了 {len(data)} 条数据")
""",

    "data_cleaning_template.py": """
# 数据清洗模板 - 单文件，直接跑
import pandas as pd

def clean_data(input_file):
    # 读取
    df = pd.read_csv(input_file)
    print(f"原始数据: {len(df)} 行")
    
    # 去重
    df = df.drop_duplicates()
    print(f"去重后: {len(df)} 行")
    
    # 删除空行
    df = df.dropna(how='all')
    
    # 填充缺失值
    df = df.fillna('')
    
    # 标准化格式
    if 'email' in df.columns:
        df['email'] = df['email'].str.lower().str.strip()
    
    if 'phone' in df.columns:
        df['phone'] = df['phone'].str.replace(r'[^0-9]', '', regex=True)
    
    # 保存
    output_file = input_file.replace('.csv', '_cleaned.csv')
    df.to_csv(output_file, index=False)
    print(f"清洗完成！保存到 {output_file}")
    
    return output_file

# 执行
clean_data('input.csv')
""",

    "lead_generation_template.py": """
# 线索生成模板 - 单文件，直接跑
import requests
import pandas as pd

def generate_leads(industry, location, count=100):
    # 使用Apollo.io或类似API
    # 这里是示例，需要替换为真实API
    
    leads = []
    
    # 模拟数据（实际使用API）
    for i in range(count):
        leads.append({
            'company': f'Company {i}',
            'contact_name': f'Person {i}',
            'email': f'person{i}@company{i}.com',
            'linkedin': f'https://linkedin.com/in/person{i}',
            'industry': industry,
            'location': location
        })
    
    # 保存
    df = pd.DataFrame(leads)
    df.to_csv('leads.csv', index=False)
    print(f"生成了 {len(leads)} 个线索")
    
    return leads

# 执行
generate_leads('SaaS', 'San Francisco', 100)
"""
}

# ============================================
# Upwork竞标模板（降维打击）
# ============================================

PROPOSAL_TEMPLATE = """
Hi [Client Name],

I can deliver this in 24 hours with high quality.

✅ I've already processed a sample of your data (see attached screenshot)
✅ 100% accurate extraction/cleaning
✅ Delivered in CSV/Excel format
✅ Unlimited revisions until you're satisfied

I use Python automation to ensure:
- Fast delivery (24-48 hours)
- High accuracy (99%+)
- Clean, structured data

Sample data is ready. I can start immediately once you award the project.

Looking forward to working with you!

Best regards,
[Your Name]

P.S. Check the attached sample - this is what you'll get for the full dataset.
"""

# ============================================
# 飞书机器人集成（替代Telegram）
# ============================================

FEISHU_BOT_SETUP = """
# 飞书机器人配置

1. 创建飞书机器人
   - 访问 https://open.feishu.cn/
   - 创建企业自建应用
   - 获取 App ID 和 App Secret

2. 配置Webhook
   - 添加机器人到群组
   - 获取 Webhook URL

3. 发送消息示例
```python
import requests

def send_feishu_message(webhook_url, text):
    data = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }
    requests.post(webhook_url, json=data)

# 使用
webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
send_feishu_message(webhook, "任务完成！抓取了500条数据")
```

4. 接收命令
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/feishu', methods=['POST'])
def feishu_webhook():
    data = request.json
    
    # 解析命令
    text = data.get('event', {}).get('message', {}).get('content', '')
    
    if '抓取' in text:
        # 执行抓取任务
        result = scrape_data()
        send_feishu_message(webhook, f"完成！{result}")
    
    return 'ok'

app.run(port=5000)
```
"""

# ============================================
# 立刻执行清单（今晚）
# ============================================

IMMEDIATE_ACTION = """
🔥 停止一切架构开发，立刻执行：

今晚（2小时）：
1. 注册Upwork账号（如果没有）
2. 搜索关键词："web scraping" + "Fixed Price" + "$30-100"
3. 找到3个任务
4. 用Python写出10%样本数据
5. 截图样本数据
6. 发送竞标（附上样本截图）

明天（4小时）：
1. 等待回复
2. 接到单后，用最丑陋但有效的方式跑出结果
3. 交付，收钱
4. 重复

目标：
- 第1周：赚到第一个$50
- 第1月：赚到$500
- 第3月：赚到$2000/月

记住：
- 不要优化代码
- 不要重构架构
- 不要追求完美
- 只要能跑出结果，交付收钱

完成第一笔入账，系统才算真正成立！
"""

if __name__ == "__main__":
    print("=" * 80)
    print("停止架构自嗨，立刻去赚钱！")
    print("=" * 80)
    print(REALITY_CHECK)
    print("\n" + IMMEDIATE_ACTION)

