# 🌐 ngrok 内网穿透使用说明

## 什么是 ngrok？

ngrok 可以让你的本地服务（运行在 localhost:8765）通过一个公网地址访问。

这样 Streamlit Cloud 就能访问你电脑上的后端服务了。

---

## 📥 下载和安装

### 第一步：下载 ngrok

访问：https://ngrok.com/download

选择 Windows 版本下载。

### 第二步：解压

下载后得到 `ngrok.exe`，解压到任意文件夹（建议放在桌面）。

### 第三步：注册账号（免费）

1. 访问：https://dashboard.ngrok.com/signup
2. 注册一个免费账号
3. 登录后进入：https://dashboard.ngrok.com/get-started/your-authtoken
4. 复制你的 authtoken

### 第四步：配置 authtoken

打开命令行（CMD），运行：

```bash
cd Desktop
ngrok config add-authtoken 你的authtoken
```

---

## 🚀 使用方法

### 启动 ngrok

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
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:8765

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

### 重要信息

**Forwarding 这一行就是你的公网地址！**

例如：`https://abc123.ngrok.io`

这个地址就是你要填到 Streamlit 代码中的 API_URL。

---

## 📝 完整流程

### 1. 启动后端服务

双击 `启动云端后端.bat`

看到：
```
INFO:     Uvicorn running on http://127.0.0.1:8765
```

### 2. 启动 ngrok

打开新的命令行窗口：

```bash
cd Desktop
ngrok http 8765
```

看到：
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8765
```

### 3. 测试是否可访问

打开浏览器访问：`https://abc123.ngrok.io`

应该看到：
```json
{
  "name": "AI Job Applier Desktop Backend",
  "version": "2.0.0",
  "status": "running"
}
```

### 4. 复制公网地址

复制 `https://abc123.ngrok.io` 这个地址。

---

## 🔧 修改 Streamlit 代码

在你的 GitHub 项目中，修改 Streamlit 代码：

```python
# 在文件开头添加
API_URL = "https://abc123.ngrok.io"  # 替换成你的 ngrok 地址

# 调用投递 API
response = requests.post(
    f"{API_URL}/api/apply/ws/boss-apply",
    json={
        "keyword": keyword,
        "city": city,
        "max_count": max_count,
        "resume_text": resume_text
    }
)
```

---

## ⚠️ 注意事项

### 1. 保持窗口打开

- 后端服务窗口要一直开着
- ngrok 窗口也要一直开着
- 关闭任何一个，服务就会中断

### 2. ngrok 地址会变

免费版 ngrok 每次重启地址都会变。

如果重启了 ngrok，需要：
1. 复制新的地址
2. 更新 Streamlit 代码中的 API_URL
3. 推送到 GitHub

### 3. 升级到付费版（可选）

ngrok 付费版（$8/月）可以：
- 固定域名（不会变）
- 更快的速度
- 更多并发连接

---

## 🎯 快速启动脚本

创建 `启动云端服务.bat`：

```batch
@echo off
echo 正在启动云端服务...
echo.

echo [1/2] 启动后端服务...
start "后端服务" cmd /k "cd /d %~dp0backend && python main.py --port 8765"

timeout /t 5 /nobreak

echo [2/2] 启动 ngrok...
start "ngrok" cmd /k "cd /d %USERPROFILE%\Desktop && ngrok http 8765"

echo.
echo ========================================
echo 云端服务启动完成！
echo ========================================
echo.
echo 请在 ngrok 窗口中复制公网地址
echo 格式：https://abc123.ngrok.io
echo.
echo 然后填到 Streamlit 代码的 API_URL 中
echo ========================================
pause
```

---

## 📊 监控和调试

### 查看 ngrok 请求日志

访问：http://127.0.0.1:4040

可以看到所有通过 ngrok 的请求。

### 查看后端日志

在后端服务窗口中可以看到所有 API 请求日志。

---

## 🚀 下一步

1. ✅ 下载并配置 ngrok
2. ✅ 启动后端服务
3. ✅ 启动 ngrok
4. ✅ 测试公网地址是否可访问
5. ✅ 修改 Streamlit 代码
6. ✅ 推送到 GitHub
7. ✅ 测试完整流程

---

## 💡 常见问题

### Q: ngrok 连接失败？

A: 检查：
1. 后端服务是否启动（访问 http://localhost:8765）
2. authtoken 是否配置正确
3. 防火墙是否拦截

### Q: Streamlit 无法访问 ngrok 地址？

A: 检查：
1. ngrok 是否在运行
2. 地址是否正确（https 开头）
3. 后端服务是否正常

### Q: 免费版够用吗？

A: 免费版限制：
- 每分钟 40 个请求
- 每月 20,000 个请求
- 对于初期测试完全够用

---

**准备好了就开始吧！** 🚀

