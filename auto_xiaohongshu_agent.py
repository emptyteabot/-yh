"""
全自动小红书发布系统 - AI员工24小时自动获客
使用Gemini生成图片 + 自动发布到小红书
"""

import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from feishu_notifier import FeishuNotifier
import requests
import os

# 飞书通知
notifier = FeishuNotifier("https://open.feishu.cn/open-apis/bot/v2/hook/6d05605e-13e9-469e-b060-bda1a168b96a")

# ============================================
# 步骤1：使用Gemini生成图片
# ============================================

GEMINI_IMAGE_PROMPTS = [
    # 图1：凌晨电脑屏幕 + 宿舍环境
    """
    A realistic photo taken with smartphone at 2:13 AM in a messy college dorm room.
    Computer screen showing Boss Zhipin (Boss直聘) job application interface with "已投递217个岗位" displayed.
    Visible in frame: half-full water cup, desk lamp turned on, scattered books, charging cables, tissue box.
    Dim lighting, only screen glow and desk lamp light.
    Slightly tilted angle, looks like casual hand-held shot.
    Grainy, slightly blurry, authentic amateur photography style.
    Chinese text on screen.
    """,
    
    # 图2：Offer邮件截图
    """
    A realistic smartphone photo of computer screen showing email inbox.
    5-8 unread emails with subjects like "面试邀请" and "Offer通知".
    Email interface in Chinese (QQ Mail or 163 Mail style).
    Timestamps showing recent 3 days.
    Slight screen reflection visible.
    Photo taken with phone camera, not screenshot.
    Authentic amateur photography, slightly blurry.
    """,
    
    # 图3：后台运行界面（可以用截图工具生成）
    """
    A screen recording screenshot showing automated job application software running.
    Interface shows: job listings scrolling quickly, progress bar "正在投递... 已投递32/100".
    Clean modern UI with Chinese text.
    Dark theme interface.
    Professional software appearance.
    """
]

def generate_images_with_gemini(prompts):
    """
    使用Gemini图片生成模型生成图片
    
    你需要：
    1. 打开你的Gemini图片生成网页
    2. 运行这个脚本，它会自动输入提示词
    3. 等待生成完成后自动下载
    """
    print("🎨 准备使用Gemini生成图片...")
    print("\n请按照以下步骤操作：")
    print("1. 打开你的Gemini图片生成网页")
    print("2. 保持浏览器窗口打开")
    print("3. 按Enter继续...")
    input()
    
    # 使用Selenium自动化操作Gemini网页
    driver = webdriver.Chrome()
    
    try:
        # 这里需要你提供Gemini图片生成的网页URL
        gemini_url = input("请输入你的Gemini图片生成网页URL: ")
        driver.get(gemini_url)
        
        generated_images = []
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n🎨 正在生成图片 {i}/3...")
            
            # 找到输入框并输入提示词
            # 注意：这里的选择器需要根据实际网页调整
            input_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "textarea"))
            )
            input_box.clear()
            input_box.send_keys(prompt)
            
            # 点击生成按钮
            generate_btn = driver.find_element(By.XPATH, "//button[contains(text(), '生成') or contains(text(), 'Generate')]")
            generate_btn.click()
            
            # 等待生成完成（根据实际情况调整等待时间）
            print("⏳ 等待生成完成...")
            time.sleep(30)  # Gemini生成图片通常需要20-40秒
            
            # 下载图片
            # 注意：这里需要根据实际网页的下载方式调整
            download_btn = driver.find_element(By.XPATH, "//button[contains(text(), '下载') or contains(text(), 'Download')]")
            download_btn.click()
            
            time.sleep(3)
            
            # 重命名下载的图片
            downloads_folder = os.path.expanduser("~/Downloads")
            latest_file = max([os.path.join(downloads_folder, f) for f in os.listdir(downloads_folder)], key=os.path.getctime)
            
            new_filename = f"xiaohongshu_image_{i}.png"
            new_path = os.path.join(os.path.dirname(__file__), new_filename)
            os.rename(latest_file, new_path)
            
            generated_images.append(new_path)
            print(f"✅ 图片 {i} 已生成并保存: {new_filename}")
        
        return generated_images
        
    finally:
        driver.quit()

# ============================================
# 步骤2：自动发布到小红书
# ============================================

def auto_publish_to_xiaohongshu(images, title, content):
    """
    自动发布到小红书
    使用Selenium模拟人工操作
    """
    print("\n📱 准备发布到小红书...")
    
    driver = webdriver.Chrome()
    
    try:
        # 打开小红书创作者平台
        driver.get("https://creator.xiaohongshu.com/publish/publish")
        
        print("⏳ 请先登录小红书创作者平台...")
        print("登录完成后按Enter继续...")
        input()
        
        # 上传图片
        print("📤 正在上传图片...")
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        
        for image_path in images:
            file_input.send_keys(os.path.abspath(image_path))
            time.sleep(2)
        
        print("✅ 图片上传完成")
        
        # 填写标题
        print("✍️ 正在填写标题...")
        title_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='标题']")
        title_input.send_keys(title)
        
        # 填写内容
        print("✍️ 正在填写内容...")
        content_input = driver.find_element(By.CSS_SELECTOR, "textarea[placeholder*='内容']")
        content_input.send_keys(content)
        
        # 添加话题标签
        print("🏷️ 正在添加话题...")
        tags = ["#求职神器", "#找工作", "#应届生", "#Boss直聘", "#自动化"]
        for tag in tags:
            content_input.send_keys(f" {tag}")
            time.sleep(1)
        
        # 发布
        print("🚀 正在发布...")
        publish_btn = driver.find_element(By.XPATH, "//button[contains(text(), '发布')]")
        publish_btn.click()
        
        time.sleep(5)
        
        print("✅ 发布成功！")
        
        # 获取笔记链接
        note_url = driver.current_url
        
        return note_url
        
    finally:
        driver.quit()

# ============================================
# 步骤3：自动监控并回复
# ============================================

def auto_monitor_and_reply(note_url):
    """
    自动监控评论并回复
    每5分钟检查一次
    """
    print("\n👀 开始监控评论...")
    
    driver = webdriver.Chrome()
    
    try:
        while True:
            driver.get(note_url)
            time.sleep(5)
            
            # 检查评论
            comments = driver.find_elements(By.CSS_SELECTOR, ".comment-item")
            
            for comment in comments:
                comment_text = comment.text.lower()
                
                # 检测关键词
                if "怎么弄" in comment_text or "求分享" in comment_text:
                    print(f"🔔 发现新评论: {comment_text}")
                    
                    # 点击回复按钮
                    reply_btn = comment.find_element(By.CSS_SELECTOR, ".reply-btn")
                    reply_btn.click()
                    time.sleep(1)
                    
                    # 输入回复（延迟3-5分钟后）
                    print("⏳ 延迟3分钟后回复（模拟真人）...")
                    time.sleep(180)  # 3分钟
                    
                    reply_input = driver.find_element(By.CSS_SELECTOR, "textarea[placeholder*='回复']")
                    reply_text = """看到你的评论啦！
这边不能发链接（会被封号）
加我微 [你的微信号]
我把工具和教程都发你"""
                    
                    reply_input.send_keys(reply_text)
                    
                    # 发送回复
                    send_btn = driver.find_element(By.XPATH, "//button[contains(text(), '发送')]")
                    send_btn.click()
                    
                    print("✅ 已自动回复")
                    
                    # 发送飞书通知
                    notifier.send_order_notification("新用户", 0, "小红书评论")
            
            # 检查浏览量
            views_element = driver.find_element(By.CSS_SELECTOR, ".view-count")
            views = int(views_element.text)
            
            print(f"📊 当前浏览量: {views}")
            
            # 如果2小时后浏览量 < 100，发送警告
            # 这里需要记录发布时间并计算
            
            # 每5分钟检查一次
            print("⏳ 5分钟后再次检查...")
            time.sleep(300)
            
    finally:
        driver.quit()

# ============================================
# 主流程：全自动执行
# ============================================

def main():
    """
    全自动流程：
    1. 使用Gemini生成图片
    2. 自动发布到小红书
    3. 自动监控并回复评论
    """
    print("🤖 AI员工开始24小时自动工作...")
    
    # 步骤1：生成图片
    print("\n" + "="*50)
    print("步骤1：使用Gemini生成图片")
    print("="*50)
    
    images = generate_images_with_gemini(GEMINI_IMAGE_PROMPTS)
    
    # 步骤2：发布到小红书
    print("\n" + "="*50)
    print("步骤2：自动发布到小红书")
    print("="*50)
    
    title = "凌晨2点还在手动投简历？我3天拿到200+面试邀请😭"
    content = """凌晨2点还在手动投简历？
我用了个工具，3天自动投了200+
现在每天都有面试邀请...
太爽了😭

想知道怎么弄的评论区说一声"""
    
    note_url = auto_publish_to_xiaohongshu(images, title, content)
    
    # 发送飞书通知
    notifier.send_traffic_report(0, 0, 0)
    
    # 步骤3：自动监控并回复
    print("\n" + "="*50)
    print("步骤3：自动监控并回复评论")
    print("="*50)
    
    auto_monitor_and_reply(note_url)

if __name__ == "__main__":
    main()


