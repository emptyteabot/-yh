"""
Gemini图片生成器 - 自动生成小红书素材
给我你的Gemini图片生成网页，我自动生成3张图
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class GeminiImageGenerator:
    def __init__(self, gemini_url):
        """
        初始化Gemini图片生成器
        
        Args:
            gemini_url: 你的Gemini图片生成网页URL
        """
        self.gemini_url = gemini_url
        self.driver = None
        
    def start(self):
        """启动浏览器"""
        print("🚀 启动浏览器...")
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        
    def generate_image(self, prompt, output_filename):
        """
        生成单张图片
        
        Args:
            prompt: 图片生成提示词
            output_filename: 输出文件名
        """
        print(f"\n🎨 正在生成: {output_filename}")
        print(f"📝 提示词: {prompt[:100]}...")
        
        try:
            # 打开Gemini网页
            if self.driver.current_url != self.gemini_url:
                self.driver.get(self.gemini_url)
                time.sleep(3)
            
            # 找到输入框（根据你的网页调整选择器）
            # 常见的选择器：textarea, input[type="text"], .prompt-input
            input_selectors = [
                "textarea",
                "input[type='text']",
                ".prompt-input",
                "[placeholder*='prompt']",
                "[placeholder*='输入']",
                "#prompt"
            ]
            
            input_box = None
            for selector in input_selectors:
                try:
                    input_box = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not input_box:
                print("❌ 找不到输入框！请手动输入提示词...")
                print(f"\n提示词：\n{prompt}\n")
                input("输入完成后按Enter继续...")
            else:
                # 清空并输入提示词
                input_box.clear()
                input_box.send_keys(prompt)
                time.sleep(1)
                
                # 查找并点击生成按钮
                generate_selectors = [
                    "//button[contains(text(), '生成')]",
                    "//button[contains(text(), 'Generate')]",
                    "//button[contains(text(), '创建')]",
                    "//button[contains(text(), 'Create')]",
                    ".generate-btn",
                    "#generate"
                ]
                
                generate_btn = None
                for selector in generate_selectors:
                    try:
                        if selector.startswith("//"):
                            generate_btn = self.driver.find_element(By.XPATH, selector)
                        else:
                            generate_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if generate_btn:
                    generate_btn.click()
                    print("✅ 已点击生成按钮")
                else:
                    print("⚠️ 找不到生成按钮，请手动点击...")
                    input("点击完成后按Enter继续...")
            
            # 等待生成完成
            print("⏳ 等待生成完成（预计30-60秒）...")
            print("生成完成后，请手动右键保存图片...")
            print(f"保存为: {output_filename}")
            input("保存完成后按Enter继续...")
            
            # 移动文件到项目目录
            downloads_folder = os.path.expanduser("~/Downloads")
            source_files = [f for f in os.listdir(downloads_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
            
            if source_files:
                # 获取最新下载的图片
                latest_file = max([os.path.join(downloads_folder, f) for f in source_files], key=os.path.getctime)
                
                # 移动到项目目录
                target_path = os.path.join(os.path.dirname(__file__), output_filename)
                os.rename(latest_file, target_path)
                
                print(f"✅ 图片已保存: {output_filename}")
                return target_path
            else:
                print("⚠️ 未找到下载的图片，请确认文件位置")
                manual_path = input("请输入图片完整路径: ")
                return manual_path
                
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            print("请手动完成生成并保存图片...")
            manual_path = input("请输入图片完整路径: ")
            return manual_path
    
    def generate_all_images(self):
        """生成所有3张图片"""
        prompts = [
            # 图1：凌晨电脑屏幕 + 宿舍环境
            (
                "A realistic photo taken with smartphone at 2:13 AM in a messy college dorm room. "
                "Computer screen showing Boss Zhipin (Boss直聘) job application interface with '已投递217个岗位' displayed. "
                "Visible in frame: half-full water cup, desk lamp turned on, scattered books, charging cables, tissue box. "
                "Dim lighting, only screen glow and desk lamp light. "
                "Slightly tilted angle, looks like casual hand-held shot. "
                "Grainy, slightly blurry, authentic amateur photography style. "
                "Chinese text on screen.",
                "xiaohongshu_image_1.png"
            ),
            
            # 图2：Offer邮件截图
            (
                "A realistic smartphone photo of computer screen showing email inbox. "
                "5-8 unread emails with subjects like '面试邀请' and 'Offer通知'. "
                "Email interface in Chinese (QQ Mail or 163 Mail style). "
                "Timestamps showing recent 3 days. "
                "Slight screen reflection visible. "
                "Photo taken with phone camera, not screenshot. "
                "Authentic amateur photography, slightly blurry.",
                "xiaohongshu_image_2.png"
            ),
            
            # 图3：后台运行界面
            (
                "A screen recording screenshot showing automated job application software running. "
                "Interface shows: job listings scrolling quickly, progress bar '正在投递... 已投递32/100'. "
                "Clean modern UI with Chinese text. "
                "Dark theme interface. "
                "Professional software appearance.",
                "xiaohongshu_image_3.png"
            )
        ]
        
        generated_images = []
        
        for i, (prompt, filename) in enumerate(prompts, 1):
            print(f"\n{'='*60}")
            print(f"生成图片 {i}/3")
            print(f"{'='*60}")
            
            image_path = self.generate_image(prompt, filename)
            generated_images.append(image_path)
            
            print(f"✅ 图片 {i}/3 完成")
            
            if i < len(prompts):
                print("\n准备生成下一张图片...")
                time.sleep(2)
        
        return generated_images
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("✅ 浏览器已关闭")

def main():
    """主流程"""
    print("🤖 Gemini图片生成器启动")
    print("="*60)
    
    # 获取Gemini网页URL
    print("\n请提供你的Gemini图片生成网页URL")
    print("例如: https://gemini.google.com/app 或其他图片生成网页")
    gemini_url = input("\nGemini网页URL: ").strip()
    
    if not gemini_url:
        print("❌ 未提供URL，使用默认值")
        gemini_url = "https://gemini.google.com/app"
    
    # 创建生成器
    generator = GeminiImageGenerator(gemini_url)
    
    try:
        # 启动浏览器
        generator.start()
        
        # 生成所有图片
        images = generator.generate_all_images()
        
        print("\n" + "="*60)
        print("🎉 所有图片生成完成！")
        print("="*60)
        
        for i, image_path in enumerate(images, 1):
            print(f"图片 {i}: {image_path}")
        
        print("\n✅ 图片已保存到项目目录")
        print("下一步：运行 auto_xiaohongshu_agent.py 自动发布到小红书")
        
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        
    finally:
        generator.close()

if __name__ == "__main__":
    main()


