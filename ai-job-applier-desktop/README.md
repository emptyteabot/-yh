# AI 求职助手 - 桌面版

一个基于 Electron + Python 的桌面应用，实现 Boss直聘自动投递、AI 生成求职信、投递记录管理等功能。

## 项目结构

```
ai-job-applier-desktop/
├── electron/                    # Electron 前端
│   ├── src/
│   │   ├── main/               # 主进程
│   │   │   ├── index.ts        # 入口文件
│   │   │   └── python-bridge.ts # Python 进程管理
│   │   ├── renderer/           # 渲染进程
│   │   │   ├── App.tsx         # 主应用
│   │   │   ├── pages/          # 页面组件
│   │   │   └── components/     # 通用组件
│   │   └── preload/            # 预加载脚本
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── backend/                     # Python 后端
│   ├── main.py                 # FastAPI 入口
│   ├── api/                    # API 路由
│   ├── ai/                     # AI 模块（复用）
│   │   ├── llm_client.py       # DeepSeek 客户端
│   │   └── resume_analyzer.py  # 简历分析
│   ├── automation/             # 自动化模块（复用）
│   │   ├── boss_applier.py     # Boss直聘投递器
│   │   ├── base_applier.py     # 抽象基类
│   │   ├── session_manager.py  # Cookie 管理
│   │   └── config.py           # 配置管理
│   ├── data/                   # 数据模块
│   │   └── application_record_service.py
│   └── requirements.txt
│
├── build/                      # 打包输出
└── resources/                  # 资源文件
```

## 功能特性

### 已实现
- ✅ Electron 前端框架搭建
- ✅ FastAPI 后端框架搭建
- ✅ IPC 通信（Electron ↔ Python）
- ✅ 复用现有 AI 和自动化模块
- ✅ 基础页面组件（仪表盘、简历上传、岗位搜索、自动投递、投递记录）

### 待实现
- ⏳ 后端 API 接口完善
- ⏳ 前端界面美化
- ⏳ 打包配置
- ⏳ 测试与优化

## 开发指南

### 前端开发

1. 安装依赖：
```bash
cd electron
npm install
```

2. 启动开发服务器：
```bash
npm run dev
```

### 后端开发

1. 安装依赖：
```bash
cd backend
pip install -r requirements.txt
```

2. 配置环境变量（创建 `.env` 文件）：
```
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

3. 启动后端服务：
```bash
python main.py --port 8765
```

### 联调测试

1. 先启动后端：
```bash
cd backend
python main.py
```

2. 再启动前端：
```bash
cd electron
npm run electron:dev
```

## 技术栈

### 前端
- Electron 28+
- React 18
- TypeScript
- Ant Design
- Zustand（状态管理）
- Vite（构建工具）

### 后端
- Python 3.10+
- FastAPI
- Playwright + Stealth（浏览器自动化）
- OpenAI SDK（DeepSeek API）
- SQLite（数据存储）

## 核心功能

### 1. 自动登录
- 手机号验证码登录
- Cookie 会话保存
- 自动恢复登录状态

### 2. AI 生成求职信
- 基于 DeepSeek API
- 多 Key 轮换
- 个性化内容生成

### 3. 自动投递
- Playwright Stealth 反检测
- 批量投递
- 实时进度推送（WebSocket）

### 4. 投递记录
- SQLite 存储
- 筛选与导出
- 统计分析

## 下一步计划

1. **完善后端 API**（1天）
   - 实现登录接口
   - 实现岗位搜索接口
   - 实现批量投递接口
   - 实现记录管理接口

2. **优化前端界面**（1天）
   - 美化 UI 设计
   - 添加加载状态
   - 错误处理
   - 响应式布局

3. **打包与测试**（0.5天）
   - 配置 Electron Builder
   - 配置 PyInstaller
   - 完整流程测试
   - Bug 修复

## 注意事项

- 确保已安装 Python 3.10+
- 确保已安装 Node.js 18+
- 需要配置 DeepSeek API Key
- Boss直聘账号需要手动登录一次

## License

MIT
