# 📦 一键打包指南

## 🎯 目标

生成一个单文件安装包：`AI求职助手 Setup 1.0.0.exe`

用户双击安装后，就能直接使用，无需配置环境。

## 🚀 快速打包（3步）

### 方式 1: 一键打包（推荐）

```bash
# 双击运行
build-all.bat
```

这个脚本会：
1. ✅ 检查环境（Python、Node.js）
2. ✅ 打包 Python 后端为 exe
3. ✅ 安装前端依赖
4. ✅ 构建前端
5. ✅ 打包成安装包

**输出**: `build\AI求职助手 Setup 1.0.0.exe`

### 方式 2: 快速打包（依赖已安装）

```bash
# 双击运行
build-quick.bat
```

适用于已经安装过依赖的情况，速度更快。

## 📋 详细步骤

### 步骤 1: 准备环境

**必需软件：**
- Python 3.10+
- Node.js 18+
- PyInstaller

**安装 PyInstaller：**
```bash
pip install pyinstaller
```

### 步骤 2: 安装依赖

**后端依赖：**
```bash
cd backend
pip install -r requirements.txt
playwright install chromium
```

**前端依赖：**
```bash
cd electron
npm install
```

### 步骤 3: 打包后端

```bash
cd backend
pyinstaller build.spec --clean
```

输出：`backend/dist/ai-job-backend.exe`

### 步骤 4: 构建前端

```bash
cd electron
npm run build
```

输出：`electron/dist/`

### 步骤 5: 打包应用

```bash
cd electron
npm run electron:build
```

输出：`build/AI求职助手 Setup 1.0.0.exe`

## 📦 打包配置

### Python 打包配置

文件：`backend/build.spec`

关键配置：
- 单文件模式：`onefile=True`
- 包含所有模块：`ai/`, `api/`, `automation/`, `data/`
- UPX 压缩：`upx=True`

### Electron 打包配置

文件：`electron/package.json` → `build` 字段

关键配置：
- 目标：NSIS 安装包
- 一键安装：`oneClick=true`
- 包含后端 exe：`extraResources`

## 🎨 自定义图标

1. 准备图标文件：`resources/icon.ico`（256x256）
2. 图标会自动应用到：
   - 安装包
   - 应用程序
   - 桌面快捷方式

## 📊 打包结果

### 文件大小
- Python 后端 exe: ~80 MB
- Electron 前端: ~100 MB
- **最终安装包: ~150-200 MB**

### 安装后目录结构
```
C:\Users\用户名\AppData\Local\Programs\AI求职助手\
├── AI求职助手.exe          # 主程序
├── resources/
│   └── backend/
│       └── ai-job-backend.exe  # Python 后端
└── ...其他文件
```

## 🔧 常见问题

### Q1: 打包失败 - 找不到模块

**解决方案：**
在 `build.spec` 的 `hiddenimports` 中添加缺失的模块：

```python
hiddenimports=[
    'fastapi',
    'uvicorn',
    'playwright',
    # 添加其他模块...
],
```

### Q2: 打包后运行报错

**解决方案：**
1. 检查 `datas` 配置，确保所有必需文件都被包含
2. 使用 `console=True` 查看错误日志
3. 检查 Python 路径配置

### Q3: 安装包太大

**解决方案：**
1. 启用 UPX 压缩：`upx=True`
2. 排除不必要的依赖
3. 使用 `excludes` 排除模块

### Q4: 用户安装后无法运行

**可能原因：**
1. 缺少 .NET Framework（Electron 需要）
2. 缺少 Visual C++ 运行库
3. 杀毒软件拦截

**解决方案：**
在安装包中包含运行时依赖，或提示用户安装。

## 🎯 优化建议

### 减小体积
1. 使用 `--exclude-module` 排除不需要的模块
2. 压缩资源文件
3. 使用 7-Zip 压缩安装包

### 提升性能
1. 使用 `--optimize=2` 优化 Python 字节码
2. 预编译前端资源
3. 启用代码分割

### 提升用户体验
1. 添加启动画面
2. 添加安装向导
3. 自动检查更新

## 📝 发布清单

打包完成后，检查：

- [ ] 安装包能正常安装
- [ ] 应用能正常启动
- [ ] Python 后端能正常运行
- [ ] 所有功能正常工作
- [ ] 图标显示正常
- [ ] 桌面快捷方式正常
- [ ] 卸载功能正常

## 🚀 发布流程

1. **测试打包**
   ```bash
   build-all.bat
   ```

2. **测试安装**
   - 在干净的 Windows 系统上测试
   - 测试所有功能

3. **发布**
   - 上传到 GitHub Releases
   - 或分享给用户

## 📄 用户安装说明

给用户的说明：

```
1. 下载 AI求职助手 Setup 1.0.0.exe
2. 双击运行安装程序
3. 等待安装完成（约 1-2 分钟）
4. 双击桌面快捷方式启动应用
5. 首次使用需要配置 DeepSeek API Key
```

## 🎉 完成

现在你有了一个完整的打包流程！

只需运行 `build-all.bat`，就能生成一个可分发的安装包。

用户安装后，双击就能使用，无需任何配置！
