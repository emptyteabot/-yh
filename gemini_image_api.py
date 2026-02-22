"""
Gemini图片生成API - 自动生成小红书素材
使用你的API密钥自动生成3张图片
"""

import requests
import json
import base64
import os
from datetime import datetime

class GeminiImageAPI:
    def __init__(self, api_key):
        """
        初始化Gemini图片生成API
        
        Args:
            api_key: 你的API密钥
        """
        self.api_key = api_key
        self.base_url = "https://oneapi.gemiaude.com/v1/chat/completions"
        self.model = "gemini-3-pro-image-preview-4k"  # 或 nano-banana-pro-4k
        
    def generate_image(self, prompt, aspect_ratio="16:9", output_filename=None):
        """
        生成单张图片
        
        Args:
            prompt: 图片生成提示词
            aspect_ratio: 图片比例 (2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9)
            output_filename: 输出文件名
        
        Returns:
            图片文件路径
        """
        print(f"\n🎨 正在生成图片...")
        print(f"📝 提示词: {prompt[:100]}...")
        print(f"📐 比例: {aspect_ratio}")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": json.dumps({"imageConfig": {"aspectRatio": aspect_ratio}})
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            "extra_body": {
                "imageConfig": {
                    "aspectRatio": aspect_ratio
                }
            },
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            # 提取图片URL或base64数据
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                
                # 如果返回的是Markdown格式的图片链接
                if "![" in content and "](" in content and ")" in content:
                    # 提取URL: ![xxx](url)
                    import re
                    match = re.search(r'!\[.*?\]\((https?://[^\)]+)\)', content)
                    if match:
                        image_url = match.group(1)
                        print(f"✅ 图片生成成功: {image_url}")
                        
                        # 下载图片
                        image_response = requests.get(image_url)
                        image_data = image_response.content
                    else:
                        print(f"⚠️ 无法提取图片URL: {content}")
                        return None
                
                # 如果返回的是直接的图片URL
                elif content.startswith("http"):
                    image_url = content
                    print(f"✅ 图片生成成功: {image_url}")
                    
                    # 下载图片
                    image_response = requests.get(image_url)
                    image_data = image_response.content
                    
                # 如果返回的是base64数据
                elif "data:image" in content:
                    # 提取base64数据
                    base64_data = content.split("base64,")[1]
                    image_data = base64.b64decode(base64_data)
                    print(f"✅ 图片生成成功（base64）")
                    
                else:
                    print(f"⚠️ 未知的返回格式: {content}")
                    return None
                
                # 保存图片
                if output_filename is None:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_filename = f"xiaohongshu_image_{timestamp}.png"
                
                output_path = os.path.join(os.path.dirname(__file__), output_filename)
                
                with open(output_path, "wb") as f:
                    f.write(image_data)
                
                print(f"💾 图片已保存: {output_filename}")
                return output_path
                
            else:
                print(f"❌ 生成失败: {result}")
                return None
                
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            return None
    
    def generate_all_xiaohongshu_images(self):
        """
        生成所有3张小红书图片
        
        Returns:
            图片文件路径列表
        """
        prompts = [
            # 图1：凌晨电脑屏幕 + 宿舍环境
            {
                "prompt": (
                    "A realistic photo taken with smartphone at 2:13 AM in a messy college dorm room. "
                    "Computer screen showing Boss Zhipin (Boss直聘) job application interface with '已投递217个岗位' displayed. "
                    "Visible in frame: half-full water cup, desk lamp turned on, scattered books, charging cables, tissue box. "
                    "Dim lighting, only screen glow and desk lamp light. "
                    "Slightly tilted angle, looks like casual hand-held shot. "
                    "Grainy, slightly blurry, authentic amateur photography style. "
                    "Chinese text on screen."
                ),
                "aspect_ratio": "3:4",  # 小红书竖图
                "filename": "xiaohongshu_image_1.png"
            },
            
            # 图2：Offer邮件截图
            {
                "prompt": (
                    "A realistic smartphone photo of computer screen showing email inbox. "
                    "5-8 unread emails with subjects like '面试邀请' and 'Offer通知'. "
                    "Email interface in Chinese (QQ Mail or 163 Mail style). "
                    "Timestamps showing recent 3 days. "
                    "Slight screen reflection visible. "
                    "Photo taken with phone camera, not screenshot. "
                    "Authentic amateur photography, slightly blurry."
                ),
                "aspect_ratio": "3:4",  # 小红书竖图
                "filename": "xiaohongshu_image_2.png"
            },
            
            # 图3：后台运行界面
            {
                "prompt": (
                    "A screen recording screenshot showing automated job application software running. "
                    "Interface shows: job listings scrolling quickly, progress bar '正在投递... 已投递32/100'. "
                    "Clean modern UI with Chinese text. "
                    "Dark theme interface. "
                    "Professional software appearance."
                ),
                "aspect_ratio": "3:4",  # 小红书竖图
                "filename": "xiaohongshu_image_3.png"
            }
        ]
        
        generated_images = []
        
        for i, config in enumerate(prompts, 1):
            print(f"\n{'='*60}")
            print(f"生成图片 {i}/3")
            print(f"{'='*60}")
            
            image_path = self.generate_image(
                prompt=config["prompt"],
                aspect_ratio=config["aspect_ratio"],
                output_filename=config["filename"]
            )
            
            if image_path:
                generated_images.append(image_path)
                print(f"✅ 图片 {i}/3 完成")
            else:
                print(f"❌ 图片 {i}/3 失败")
            
            # 避免API限流
            if i < len(prompts):
                print("\n⏳ 等待5秒后生成下一张...")
                import time
                time.sleep(5)
        
        return generated_images

def main():
    """主流程"""
    print("🤖 Gemini图片生成API启动")
    print("="*60)
    
    # API配置
    API_KEY = "sk-Oyw295f1RAWkOuFjExGhHoGzJbYOVRFVIcGecC2z63TCRtAm"
    
    # 创建生成器
    generator = GeminiImageAPI(API_KEY)
    
    # 生成所有图片
    images = generator.generate_all_xiaohongshu_images()
    
    print("\n" + "="*60)
    print("🎉 图片生成完成！")
    print("="*60)
    
    if images:
        for i, image_path in enumerate(images, 1):
            print(f"图片 {i}: {image_path}")
        
        print(f"\n✅ 成功生成 {len(images)}/3 张图片")
        print("\n下一步：运行 auto_xiaohongshu_agent.py 自动发布到小红书")
    else:
        print("\n❌ 图片生成失败，请检查API配置")

if __name__ == "__main__":
    main()

