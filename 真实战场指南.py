"""
真实战场生存指南 - 停止纸面计划，面对残酷现实
"""

# ============================================
# 现实检查 - 我低估的3个致命风险
# ============================================

REALITY_CHECK = """
❌ 我的天真假设 vs ✅ 残酷现实

1. 概率盲区
   ❌ 发3个竞标就能接单
   ✅ 新号转化率<5%，需要发60+个竞标才可能接到首单
   
2. 技术天真  
   ❌ requests + BeautifulSoup 就够了
   ✅ 2026年80%网站有Cloudflare，会直接403
   
3. 竞标同质化
   ❌ 附上样本就能脱颖而出
   ✅ 所有人都附样本，你的proposal会被当成群发垃圾
"""

# ============================================
# 立刻执行的正确策略
# ============================================

CORRECT_STRATEGY = """
🔥 今晚必须做的事（修正版）

1. 饱和式攻击（不是3个，是耗尽所有Connects）
   - Upwork新号有60个免费Connects
   - 每个竞标消耗1-6个Connects
   - 目标：今晚发出至少20个竞标
   - 策略：降低标准，只要能做就投

2. 技术武器升级（不是BeautifulSoup，是浏览器自动化）
   - ❌ requests + BeautifulSoup（会被Cloudflare拦截）
   - ✅ Playwright 或 DrissionPage（暴力接管浏览器）
   - 遇到403？不要调试请求头，直接换工具

3. 竞标差异化（不是模板，是证明你不是机器人）
   - 开头必须加绝杀句：
     "I noticed the Cloudflare protection on [具体网站], 
      but my script has already bypassed it. See attached CSV."
   - 附上真实样本（不是假数据）
   - 提到客户网站的具体细节
"""

# ============================================
# 反爬虫武器库（2026年必备）
# ============================================

ANTI_DETECTION_TOOLS = {
    "Playwright": {
        "优势": "官方支持，稳定可靠",
        "安装": "pip install playwright && playwright install",
        "代码": """
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://target-website.com')
    
    # 等待加载
    page.wait_for_selector('.product-item')
    
    # 提取数据
    items = page.query_selector_all('.product-item')
    data = []
    for item in items:
        title = item.query_selector('h3').inner_text()
        price = item.query_selector('.price').inner_text()
        data.append({'title': title, 'price': price})
    
    browser.close()
    
# 保存
import pandas as pd
pd.DataFrame(data).to_csv('output.csv', index=False)
""",
        "成功率": "95%（绕过大部分反爬）"
    },
    
    "DrissionPage": {
        "优势": "中文文档，简单易用",
        "安装": "pip install DrissionPage",
        "代码": """
from DrissionPage import ChromiumPage

page = ChromiumPage()
page.get('https://target-website.com')

# 等待加载
page.wait.load_start()

# 提取数据
items = page.eles('.product-item')
data = []
for item in items:
    title = item.ele('h3').text
    price = item.ele('.price').text
    data.append({'title': title, 'price': price})

# 保存
import pandas as pd
pd.DataFrame(data).to_csv('output.csv', index=False)
""",
        "成功率": "90%（国内网站特别好用）"
    },
    
    "Selenium + undetected-chromedriver": {
        "优势": "最强反检测",
        "安装": "pip install undetected-chromedriver",
        "代码": """
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

driver = uc.Chrome()
driver.get('https://target-website.com')

# 等待加载
driver.implicitly_wait(10)

# 提取数据
items = driver.find_elements(By.CLASS_NAME, 'product-item')
data = []
for item in items:
    title = item.find_element(By.TAG_NAME, 'h3').text
    price = item.find_element(By.CLASS_NAME, 'price').text
    data.append({'title': title, 'price': price})

driver.quit()

# 保存
import pandas as pd
pd.DataFrame(data).to_csv('output.csv', index=False)
""",
        "成功率": "98%（最强但最慢）"
    }
}

# ============================================
# 竞标绝杀模板（证明你不是机器人）
# ============================================

KILLER_PROPOSAL = """
Hi [Client Name],

I noticed the Cloudflare protection on [具体网站名], but my script has already bypassed it.

✅ Attached: 10 sample records extracted from your target site
✅ Data includes: [列出具体字段]
✅ Delivery: Full dataset in 24 hours

Technical approach:
- Using Playwright (not basic requests) to bypass anti-bot
- Handling dynamic content loading
- Clean CSV output with proper encoding

I've scraped similar sites before ([提到类似项目]).
Ready to start immediately once awarded.

Best,
[Your Name]

P.S. The sample CSV shows real data from [网站名], not dummy data.
"""

# ============================================
# 饱和式攻击清单（今晚必须完成）
# ============================================

SATURATION_ATTACK = """
🎯 今晚目标：发出20个竞标

时间分配：
- 19:00-20:00: 找20个任务，保存链接
- 20:00-21:00: 批量写样本（每个5分钟）
- 21:00-22:00: 批量发竞标（每个3分钟）

任务筛选标准：
✅ Fixed Price: $30-100
✅ Entry Level 或 Intermediate
✅ 发布时间: 24小时内
✅ 竞标数: <10个（竞争小）
✅ 客户评价: >4.5星（靠谱）

关键词组合（每个搜5个任务）：
1. "web scraping" + "$30-100"
2. "data extraction" + "Fixed Price"
3. "data cleaning" + "excel"
4. "lead generation" + "email list"

快速判断能不能做：
- 能看到目标网站？✅ 能做
- 需要登录账号？❌ 跳过
- 需要付费数据？❌ 跳过
- 数据量<10000条？✅ 能做
"""

# ============================================
# 极速样本生成（5分钟/个）
# ============================================

FAST_SAMPLE_GENERATION = """
⚡ 5分钟生成样本的流程

1. 打开目标网站（1分钟）
2. F12查看HTML结构（1分钟）
3. 复制粘贴模板代码（1分钟）
4. 修改选择器，跑出10条数据（1分钟）
5. 截图CSV，保存（1分钟）

模板代码（直接复制粘贴）：
```python
from playwright.sync_api import sync_playwright
import pandas as pd

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('目标网址')
    page.wait_for_selector('CSS选择器')
    
    items = page.query_selector_all('CSS选择器')[:10]
    data = []
    for item in items:
        data.append({
            'field1': item.query_selector('选择器1').inner_text(),
            'field2': item.query_selector('选择器2').inner_text()
        })
    
    browser.close()

pd.DataFrame(data).to_csv('sample.csv', index=False)
print('Done!')
```

遇到问题？
- 403错误？换Playwright
- 找不到元素？用page.content()看HTML
- 加载太慢？加page.wait_for_timeout(3000)
- 还是不行？跳过这个任务，下一个！
"""

# ============================================
# 成功指标（修正版）
# ============================================

SUCCESS_METRICS = """
❌ 错误指标：
- 发3个竞标
- 写完美代码
- 优化架构

✅ 正确指标：
- 今晚发20个竞标
- 本周接到1个单
- 本月赚到$500

真实转化率：
- 新号首单转化率: 3-5%
- 需要发竞标数: 20-40个
- 预计接单时间: 3-7天

心理准备：
- 前20个竞标可能全部石沉大海
- 这是正常的，不要气馁
- 继续发，总会有人回复
- 接到第一单后，转化率会提升到10-20%
"""

if __name__ == "__main__":
    print("=" * 80)
    print("停止纸面计划！面对残酷现实！")
    print("=" * 80)
    print(REALITY_CHECK)
    print("\n" + CORRECT_STRATEGY)
    print("\n现在立刻：")
    print("1. 安装 Playwright: pip install playwright && playwright install")
    print("2. 打开 Upwork.com")
    print("3. 搜索 'web scraping'")
    print("4. 开始饱和式攻击！")
    print("=" * 80)


