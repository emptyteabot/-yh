# 🚀 Streamlit 云端版 - 完整部署指南

## 📋 部署步骤总览

1. ✅ 启动本地后端服务
2. ✅ 设置 ngrok 内网穿透
3. ✅ 修改 Streamlit 代码
4. ✅ 推送到 GitHub
5. ✅ 测试完整流程

---

## 第一步：启动本地后端服务

### 方式 1：双击批处理文件（推荐）

双击：`ai-job-applier-desktop/启动云端后端.bat`

### 方式 2：命令行启动

```bash
cd ai-job-applier-desktop/backend
python main.py --port 8765
```

### 验证是否启动成功

打开浏览器访问：http://localhost:8765

应该看到：
```json
{
  "name": "AI Job Applier Desktop Backend",
  "version": "2.0.0",
  "status": "running"
}
```

✅ 看到这个说明后端启动成功！

---

## 第二步：设置 ngrok 内网穿透

### 2.1 下载 ngrok

访问：https://ngrok.com/download

选择 Windows 版本，下载后解压到桌面。

### 2.2 注册账号（免费）

1. 访问：https://dashboard.ngrok.com/signup
2. 注册免费账号
3. 登录后访问：https://dashboard.ngrok.com/get-started/your-authtoken
4. 复制你的 authtoken（类似：2abc123def456...）

### 2.3 配置 authtoken

打开命令行（CMD），运行：

```bash
cd Desktop
ngrok config add-authtoken 你的authtoken
```

### 2.4 启动 ngrok

```bash
cd Desktop
ngrok http 8765
```

会看到类似这样的界面：

```
ngrok

Session Status                online
Account                       你的邮箱
Version                       3.x.x
Region                        Asia Pacific (ap)
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:8765

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

### 2.5 复制公网地址

**重要！** 复制 `Forwarding` 这一行的地址：

```
https://abc123.ngrok.io
```

这就是你的公网地址！

### 2.6 测试公网地址

打开浏览器访问：`https://abc123.ngrok.io`

应该看到和 http://localhost:8765 一样的内容。

✅ 看到这个说明 ngrok 配置成功！

---

## 第三步：修改 Streamlit 代码

### 3.1 复制新的 Streamlit 代码

我已经帮你创建了新的 Streamlit 代码：

```
一人公司260222/streamlit_app.py
```

### 3.2 修改 API_URL

打开 `streamlit_app.py`，找到第 12 行：

```python
API_URL = "https://your-domain.ngrok.io"  # 🔴 替换成你的 ngrok 地址
```

替换成你的 ngrok 地址：

```python
API_URL = "https://abc123.ngrok.io"  # ✅ 你的实际地址
```

### 3.3 复制到你的 GitHub 项目

将 `streamlit_app.py` 复制到你的 GitHub 项目根目录：

```
ai-job-helper/
├── streamlit_app.py  ← 替换这个文件
├── requirements.txt
└── README.md
```

---

## 第四步：推送到 GitHub

### 4.1 打开你的 GitHub 项目

访问：https://github.com/emptyteabot/ai-job-helper

### 4.2 上传新文件

**方式 1：网页上传（最简单）**

1. 点击 `streamlit_app.py` 文件
2. 点击右上角的 ✏️ 编辑按钮
3. 删除所有内容
4. 粘贴新的代码
5. 点击 "Commit changes"

**方式 2：Git 命令行**

```bash
cd ai-job-helper
git add streamlit_app.py
git commit -m "添加自动投递功能"
git push
```

### 4.3 等待 Streamlit 重新部署

推送后，Streamlit Cloud 会自动重新部署（约 1-2 分钟）。

访问：https://ai-job-apper-ibpzap2nnajzrnu8mkthuv.streamlit.app/

看到新界面说明部署成功！

---

## 第五步：测试完整流程

### 5.1 访问 Streamlit 应用

打开：https://ai-job-apper-ibpzap2nnajzrnu8mkthuv.streamlit.app/

### 5.2 登录/注册

1. 输入手机号（随便输入，如 13800138000）
2. 点击"登录/注册"
3. 自动注册并赠送 5 次免费投递

### 5.3 开始投递

1. 关键词：`Python 实习`
2. 城市：`北京`
3. 投递数量：`3`（先测试 3 个）
4. 简历内容：粘贴你的简历
5. 点击"开始自动投递"

### 5.4 查看结果

- 实时显示投递进度
- 显示成功/失败状态
- 显示剩余投递次数

✅ 如果能看到投递结果，说明整个流程打通了！

---

## 🎯 保持服务运行

### 重要提示

要让服务持续可用，需要：

1. **后端服务窗口** - 一直开着
2. **ngrok 窗口** - 一直开着
3. **电脑** - 不要关机或休眠

### 创建自动启动脚本

创建 `启动云端服务.bat`：

```batch
@echo off
echo 正在启动云端服务...
echo.

echo [1/2] 启动后端服务...
start "后端服务" cmd /k "cd /d %~dp0ai-job-applier-desktop\backend && python main.py --port 8765"

timeout /t 5 /nobreak

echo [2/2] 启动 ngrok...
start "ngrok" cmd /k "cd /d %USERPROFILE%\Desktop && ngrok http 8765"

echo.
echo ========================================
echo 云端服务启动完成！
echo ========================================
echo.
echo 请在 ngrok 窗口中复制公网地址
echo 然后更新 Streamlit 代码的 API_URL
echo ========================================
pause
```

以后只需双击这个文件，就能一键启动所有服务！

---

## 📊 监控和调试

### 查看后端日志

在后端服务窗口中可以看到所有请求日志：

```
INFO:     127.0.0.1:12345 - "POST /api/auth/login HTTP/1.1" 200 OK
INFO:     127.0.0.1:12345 - "POST /api/apply/boss/batch HTTP/1.1" 200 OK
```

### 查看 ngrok 请求

访问：http://127.0.0.1:4040

可以看到所有通过 ngrok 的请求详情。

---

## ⚠️ 常见问题

### Q1: Streamlit 显示"后端服务未启动"

**原因**：
- 后端服务没启动
- ngrok 没启动
- API_URL 地址错误

**解决**：
1. 检查后端服务窗口是否在运行
2. 检查 ngrok 窗口是否在运行
3. 检查 API_URL 是否正确

### Q2: ngrok 地址变了怎么办？

**原因**：免费版 ngrok 每次重启地址都会变

**解决**：
1. 复制新的 ngrok 地址
2. 更新 Streamlit 代码的 API_URL
3. 推送到 GitHub
4. 等待重新部署

**避免方法**：
- 升级到 ngrok 付费版（$8/月）
- 可以获得固定域名

### Q3: 投递失败怎么办？

**原因**：
- 当前是模拟投递（90% 成功率）
- 真实投递需要集成 Playwright

**解决**：
- 查看后端日志
- 查看错误信息
- 联系技术支持

### Q4: 免费版 ngrok 够用吗？

**限制**：
- 每分钟 40 个请求
- 每月 20,000 个请求

**够用情况**：
- 初期测试：完全够用
- 10 个用户：够用
- 50 个用户：可能不够

**建议**：
- 初期用免费版
- 有 20+ 付费用户后升级

---

## 💰 成本分析

### 当前方案成本

| 项目 | 费用 | 说明 |
|------|------|------|
| Streamlit Cloud | ¥0 | 免费托管前端 |
| 你的电脑 | ¥0 | 24 小时开机（电费忽略） |
| ngrok 免费版 | ¥0 | 内网穿透 |
| DeepSeek API | ¥50-100/月 | AI 生成求职信 |
| **总成本** | **¥50-100/月** | 非常低！ |

### 升级方案成本

| 项目 | 费用 | 说明 |
|------|------|------|
| Streamlit Cloud | ¥0 | 免费 |
| 云服务器 | ¥100-200/月 | 阿里云轻量服务器 |
| ngrok 付费版 | ¥60/月 | 固定域名 |
| DeepSeek API | ¥100-200/月 | 更多调用 |
| **总成本** | **¥260-460/月** | 适合 50+ 用户 |

---

## 🚀 下一步优化

### 短期（1 周内）

1. ✅ 集成真实投递引擎（Playwright）
2. ✅ 添加投递记录功能
3. ✅ 优化 UI 界面

### 中期（1 个月内）

1. ⏳ 添加支付接口（微信/支付宝）
2. ⏳ 添加数据统计功能
3. ⏳ 优化 AI 求职信质量

### 长期（3 个月内）

1. ⏳ 支持更多平台（拉勾、智联）
2. ⏳ 开发移动端
3. ⏳ 企业版功能

---

## 📣 推广计划

### 第一周

1. ✅ 写第一篇小红书笔记
2. ✅ 录制使用教程视频
3. ✅ 找 10 个学生内测

### 第一个月

1. ⏳ 每周 3 篇小红书笔记
2. ⏳ 每周 5 个知乎回答
3. ⏳ 每周 1 个 B站视频
4. ⏳ 目标：100 个注册用户，10 个付费用户

---

## 🎉 总结

**你现在有了**：
- ✅ Streamlit 云端前端（免费托管）
- ✅ 本地后端服务（完整功能）
- ✅ ngrok 内网穿透（连接前后端）
- ✅ 用户系统（注册/登录/套餐）
- ✅ 自动投递功能（模拟版）

**下一步**：
1. 按照本指南部署
2. 测试完整流程
3. 开始推广
4. 赚第一笔钱！

**预期收入**：
- 第 1 个月：¥199（10 个付费用户）
- 第 3 个月：¥3,600（120 个付费用户）
- 第 6 个月：¥17,500（500 个付费用户）

**立即开始吧！** 🚀

---

**有问题随时问我！**

