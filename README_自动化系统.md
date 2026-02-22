# 全自动小红书获客系统 - 使用说明

## 🎯 系统功能

AI员工24小时自动工作：
1. ✅ 使用Gemini自动生成图片
2. ✅ 自动发布到小红书
3. ✅ 自动监控评论并回复
4. ✅ 自动引导用户加微信
5. ✅ 飞书实时通知收单进度

---

## 🚀 快速开始（3步）

### 步骤1：生成图片（5分钟）

```bash
python gemini_image_generator.py
```

**操作流程：**
1. 输入你的Gemini图片生成网页URL
2. 脚本会自动打开浏览器
3. 自动输入提示词并生成3张图片
4. 图片自动保存到项目目录

**如果自动化失败：**
- 脚本会显示提示词
- 你手动复制粘贴到Gemini
- 生成后手动保存图片
- 按Enter继续下一张

---

### 步骤2：自动发布到小红书（3分钟）

```bash
python auto_xiaohongshu_agent.py
```

**操作流程：**
1. 脚本自动打开小红书创作者平台
2. 你手动登录一次（之后会保持登录）
3. 脚本自动上传图片、填写标题、内容、话题
4. 自动点击发布

---

### 步骤3：自动监控并回复（24小时运行）

发布完成后，脚本会自动：
- 每5分钟检查一次评论
- 发现"怎么弄"或"求分享"关键词
- 延迟3-5分钟后自动回复
- 引导用户加微信
- 飞书实时通知你

---

## 📋 安装依赖

```bash
pip install selenium requests loguru
```

**下载Chrome驱动：**
1. 访问：https://chromedriver.chromium.org/
2. 下载与你的Chrome版本匹配的驱动
3. 放到系统PATH或项目目录

---

## 🎨 Gemini图片生成提示词

脚本已内置3个提示词：

### 图1：凌晨电脑屏幕 + 宿舍环境
```
A realistic photo taken with smartphone at 2:13 AM in a messy college dorm room.
Computer screen showing Boss Zhipin (Boss直聘) job application interface with '已投递217个岗位' displayed.
Visible in frame: half-full water cup, desk lamp turned on, scattered books, charging cables, tissue box.
Dim lighting, only screen glow and desk lamp light.
Slightly tilted angle, looks like casual hand-held shot.
Grainy, slightly blurry, authentic amateur photography style.
Chinese text on screen.
```

### 图2：Offer邮件截图
```
A realistic smartphone photo of computer screen showing email inbox.
5-8 unread emails with subjects like '面试邀请' and 'Offer通知'.
Email interface in Chinese (QQ Mail or 163 Mail style).
Timestamps showing recent 3 days.
Slight screen reflection visible.
Photo taken with phone camera, not screenshot.
Authentic amateur photography, slightly blurry.
```

### 图3：后台运行界面
```
A screen recording screenshot showing automated job application software running.
Interface shows: job listings scrolling quickly, progress bar '正在投递... 已投递32/100'.
Clean modern UI with Chinese text.
Dark theme interface.
Professional software appearance.
```

---

## 💬 自动回复话术

脚本会自动回复：

```
看到你的评论啦！
这边不能发链接（会被封号）
加我微 [你的微信号]
我把工具和教程都发你
```

**注意：** 需要在 `auto_xiaohongshu_agent.py` 中修改 `[你的微信号]` 为你的真实微信号

---

## 📊 飞书通知

脚本会自动发送飞书通知：

- 💰 新订单通知（有人评论）
- 📊 流量报告（每2小时）
- ⚠️ 警告通知（浏览量过低）

---

## 🔧 配置文件

### 修改微信号

编辑 `auto_xiaohongshu_agent.py`：

```python
reply_text = """看到你的评论啦！
这边不能发链接（会被封号）
加我微 你的微信号
我把工具和教程都发你"""
```

### 修改发布内容

编辑 `auto_xiaohongshu_agent.py`：

```python
title = "凌晨2点还在手动投简历？我3天拿到200+面试邀请😭"
content = """凌晨2点还在手动投简历？
我用了个工具，3天自动投了200+
现在每天都有面试邀请...
太爽了😭

想知道怎么弄的评论区说一声"""
```

---

## 🎯 完整工作流程

```
1. 运行 gemini_image_generator.py
   ↓
2. Gemini自动生成3张图片
   ↓
3. 运行 auto_xiaohongshu_agent.py
   ↓
4. 自动发布到小红书
   ↓
5. 自动监控评论（24小时运行）
   ↓
6. 发现关键词 → 延迟3-5分钟 → 自动回复
   ↓
7. 飞书通知你 → 用户加微信
   ↓
8. 你发送定价话术（¥19.9）
   ↓
9. 用户转账 → 后台运行工具 → 交付PDF
   ↓
10. 要求用户回评 → 算法推高 → 更多流量
```

---

## ⚠️ 注意事项

### 1. 首次运行需要手动登录
- 小红书创作者平台需要手动登录一次
- 之后浏览器会保持登录状态

### 2. 监控脚本需要持续运行
- 建议在服务器或云主机上运行
- 或者使用 `nohup` 后台运行

### 3. 延迟回复很重要
- 脚本会自动延迟3-5分钟回复
- 模拟真人行为，避免被判定为机器人

### 4. 定期检查脚本状态
- 飞书会实时通知你
- 建议每天检查一次脚本运行状态

---

## 🚀 立刻执行

```bash
# 步骤1：生成图片
python gemini_image_generator.py

# 步骤2：发布到小红书
python auto_xiaohongshu_agent.py

# 完成！脚本会自动监控并回复
```

---

## 💰 预期收益

### 第一天
- 发布：1条笔记
- 加微信：1-2人
- 收入：¥0-19.9

### 第一周
- 发布：5条笔记
- 加微信：5-10人
- 收入：¥40-100

### 第一月
- 发布：20条笔记
- 加微信：20-50人
- 收入：¥200-500

---

## 🎉 开始赚钱

**现在就运行脚本，让AI员工24小时为你工作！**

```bash
python gemini_image_generator.py
```


