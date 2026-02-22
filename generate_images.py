"""
一键生成小红书图片 - 直接运行
"""

import requests
import json
import re
import os

# API配置
API_KEY = "sk-Oyw295f1RAWkOuFjExGhHoGzJbYOVRFVIcGecC2z63TCRtAm"
API_URL = "https://oneapi.gemiaude.com/v1/chat/completions"
MODEL = "gemini-3-pro-image-preview-4k"

# 提示词
PROMPTS = [
    "A realistic photo taken with smartphone at 2:13 AM in a messy college dorm room. Computer screen showing Boss Zhipin job application interface with '已投递217个岗位' displayed. Visible: half-full water cup, desk lamp on, scattered books, charging cables, tissue box. Dim lighting, screen glow and desk lamp light. Slightly tilted angle, casual hand-held shot. Grainy, slightly blurry, authentic amateur photography. Chinese text on screen.",
    
    "A realistic smartphone photo of computer screen showing email inbox. 5-8 unread emails with subjects like '面试邀请' and 'Offer通知'. Email interface in Chinese (QQ Mail style). Timestamps showing recent 3 days. Slight screen reflection. Photo taken with phone camera, not screenshot. Authentic amateur photography, slightly blurry.",
    
    "A screen recording screenshot showing automated job application software running. Interface shows: job listings scrolling quickly, progress bar '正在投递... 已投递32/100'. Clean modern UI with Chinese text. Dark theme interface. Professional software appearance."
]

def generate_image(prompt, filename):
    """生成单张图片"""
    print(f"\n🎨 正在生成: {filename}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": json.dumps({"imageConfig": {"aspectRatio": "3:4"}})
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ],
        "extra_body": {
            "imageConfig": {"aspectRatio": "3:4"}
        },
        "max_tokens": 150,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()
        
        content = result["choices"][0]["message"]["content"]
        
        # 提取图片URL
        match = re.search(r'!\[.*?\]\((https?://[^\)]+)\)', content)
        if match:
            image_url = match.group(1)
            print(f"✅ 图片URL: {image_url}")
            
            # 下载图片
            img_response = requests.get(image_url)
            
            # 保存图片
            with open(filename, "wb") as f:
                f.write(img_response.content)
            
            print(f"💾 已保存: {filename}")
            return filename
        else:
            print(f"❌ 无法提取URL: {content}")
            return None
            
    except Exception as e:
        print(f"❌ 失败: {e}")
        return None

# 生成3张图片
print("🤖 开始生成小红书图片...")
print("="*60)

images = []
for i, prompt in enumerate(PROMPTS, 1):
    filename = f"xiaohongshu_{i}.png"
    result = generate_image(prompt, filename)
    if result:
        images.append(result)
    
    if i < len(PROMPTS):
        print("\n⏳ 等待5秒...")
        import time
        time.sleep(5)

print("\n" + "="*60)
print(f"🎉 完成！成功生成 {len(images)}/3 张图片")
print("="*60)

for img in images:
    print(f"✅ {img}")

print("\n下一步：使用这3张图片发布到小红书")


