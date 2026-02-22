# 🚀 快速启动指南

## ⚡ 快速开始（推荐）

### 开发模式（日常使用）

```bash
# 双击运行
start-dev.bat
```

**这会自动：**
- ✅ 启动 Python 后端
- ✅ 启动 Electron 前端
- ✅ 支持代码热重载
- ✅ 不需要打包

**适用场景：**
- 开发新功能
- 修复 Bug
- 测试功能
- 日常使用

---

### 打包模式（发布时使用）

```bash
# 双击运行（仅在发布时）
build-all.bat
```

**这会生成：**
- 📦 Windows 安装包
- 📁 位置：`build\AI求职助手 Setup 1.0.0.exe`

**适用场景：**
- 功能开发完成
- 准备发布给用户
- 需要分发安装包

**⚠️ 注意：不要频繁打包！**

---

## 环境要求

- Python 3.10+
- Node.js 18+
- Windows 10/11

## 安装步骤

### 1. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
playwright install chromium
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的配置：

```env
# 必需配置
DEEPSEEK_API_KEY=sk-your-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com
BOSS_PHONE=your_phone_number

# 可选配置
FEISHU_WEBHOOK_URL=https://open.feishu.cn/xxx
```

### 3. 安装前端依赖

```bash
cd electron
npm install
```

## 启动应用

### 方式 1: 使用启动脚本（推荐）

双击运行 `start-dev.bat`

### 方式 2: 手动启动

**终端 1 - 启动后端：**
```bash
cd backend
python main.py --port 8765
```

**终端 2 - 启动前端：**
```bash
cd electron
npm run electron:dev
```

## 首次使用

1. **登录 Boss直聘**
   - 点击左侧菜单"登录"
   - 输入手机号
   - 在弹出的浏览器中完成验证码验证

2. **上传简历**
   - 点击"简历管理"
   - 上传 PDF 或 Word 格式简历

3. **AI 分析简历**
   - 点击"AI 分析"
   - 点击"开始 AI 分析"
   - 等待 4 个 Agent 完成分析

4. **搜索岗位**
   - 方式 A: Boss直聘搜索
   - 方式 B: OpenClaw 搜索（需要安装 OpenClaw）

5. **开始投递**
   - 方式 A: 自动投递（手动选择岗位）
   - 方式 B: 智能投递（全自动）

## 功能说明

### 仪表盘
- 查看投递统计
- 查看最近记录

### 简历管理
- 上传/删除简历
- 查看简历内容

### AI 分析
- 职业分析师
- 岗位推荐专家
- 面试辅导专家
- 质量审核官

### 岗位搜索
- Boss直聘搜索
- OpenClaw 搜索（真实数据）

### 自动投递
- 批量投递选中岗位
- AI 生成求职信
- 实时进度显示

### 智能投递
- 自动搜索匹配岗位
- 自动分析简历
- 自动生成求职信
- 自动批量投递

### 投递记录
- 查看所有记录
- 状态筛选
- 统计分析

## 常见问题

### Q: 登录失败怎么办？
A: 确保手机号正确，在浏览器中完成验证码验证。

### Q: OpenClaw 不可用？
A: OpenClaw 是可选功能，不影响其他功能使用。如需使用，请安装：
```bash
npm install -g @openclaw/cli
```

### Q: AI 分析失败？
A: 检查 DeepSeek API Key 是否配置正确。

### Q: 投递失败？
A: 可能是账号被限制，建议降低投递频率，增加延迟时间。

## 注意事项

1. **投递频率**
   - 建议每次投递间隔 3-5 秒
   - 每天投递不超过 50 个岗位

2. **账号安全**
   - 不要频繁登录/登出
   - 不要在多个设备同时使用

3. **API 限流**
   - DeepSeek API 有调用限制
   - 建议配置多个 API Key 轮换使用

4. **数据备份**
   - 定期导出投递记录
   - 备份简历文件

## 技术支持

如有问题，请查看：
- `README.md` - 项目说明
- `INTEGRATION_COMPLETE.md` - 功能说明
- `DEVELOPMENT_SUMMARY.md` - 开发文档

## 更新日志

### v2.0.0 (2026-02-21)
- ✅ 集成所有 Streamlit 功能
- ✅ 4 个 AI Agent 简历分析
- ✅ OpenClaw 真实数据搜索
- ✅ 智能投递系统
- ✅ 飞书通知集成
- ✅ 完整的前后端架构

### v1.0.0 (2026-02-20)
- ✅ 基础框架搭建
- ✅ Boss直聘自动投递
- ✅ 简历管理
- ✅ 投递记录

---

**祝你求职顺利！🎉**
