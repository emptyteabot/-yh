# 🛠️ 开发指南

## 📌 重要提示

**在开发阶段，不要频繁打包！**

打包 exe 只在最后发布时做一次。开发过程中使用开发模式，可以：
- ✅ 实时修改代码
- ✅ 立即看到效果
- ✅ 快速调试
- ✅ 不需要等待打包

---

## 🚀 开发模式启动

### 方式 1：一键启动（推荐）

```bash
# 双击运行
start-dev.bat
```

这会自动启动：
1. Python 后端（端口 8765）
2. Electron 前端（端口 5173）

### 方式 2：手动启动

**终端 1 - 启动后端：**
```bash
cd backend
python main.py --port 8765
```

**终端 2 - 启动前端：**
```bash
cd electron
npm run dev
```

**终端 3 - 启动 Electron：**
```bash
cd electron
npm run electron:dev
```

---

## 📝 开发流程

### 1. 修改代码

**后端代码：**
- 修改 `backend/` 下的任何 Python 文件
- 保存后，手动重启后端服务（Ctrl+C 然后重新运行）

**前端代码：**
- 修改 `electron/src/` 下的任何 TypeScript/React 文件
- 保存后，Vite 会自动热重载，立即看到效果

### 2. 测试功能

在开发模式下测试所有功能：
- ✅ 简历上传
- ✅ AI 分析
- ✅ 岗位搜索
- ✅ 自动投递
- ✅ 记录管理

### 3. 调试

**后端调试：**
```python
# 在代码中添加打印
print(f"调试信息: {变量}")

# 或使用 logging
import logging
logging.info("调试信息")
```

**前端调试：**
- 打开 Chrome DevTools（F12）
- 查看 Console 输出
- 使用 React DevTools

### 4. 修复 Bug

发现 Bug → 修改代码 → 保存 → 立即测试 → 继续开发

**不需要重新打包！**

---

## 🎯 什么时候打包？

### ❌ 不要打包的情况

- 正在开发新功能
- 正在修复 Bug
- 正在测试
- 代码还不稳定

### ✅ 应该打包的情况

- 所有功能都开发完成
- 所有 Bug 都修复
- 充分测试过
- 准备发布给用户

---

## 📦 打包流程（最后才做）

### 1. 确认代码稳定

```bash
# 在开发模式下充分测试
# 确保所有功能正常
```

### 2. 执行打包

```bash
# 双击运行
build-all.bat
```

### 3. 测试安装包

```bash
# 安装并测试
build\AI求职助手 Setup 1.0.0.exe
```

### 4. 发布

如果测试通过，就可以分发给用户了。

---

## 🔄 更新流程

### 开发阶段更新

```
修改代码 → 保存 → 自动重载 → 测试
（循环往复，不需要打包）
```

### 发布阶段更新

```
1. 在开发模式下完成所有修改
2. 充分测试
3. 修改版本号（package.json）
4. 执行 build-all.bat
5. 测试新的安装包
6. 发布给用户
```

---

## 💡 开发技巧

### 1. 使用热重载

前端代码修改后会自动重载，不需要手动刷新。

### 2. 后端自动重启

可以使用 `uvicorn` 的 `--reload` 参数：

```bash
cd backend
uvicorn main:app --reload --port 8765
```

但需要修改 `main.py`：

```python
# 在 main.py 最后
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8765, reload=True)
```

### 3. 使用 Git

```bash
# 每次修改后提交
git add .
git commit -m "修复了某个 Bug"

# 如果改坏了，可以回退
git checkout -- .
```

### 4. 分支开发

```bash
# 开发新功能时创建分支
git checkout -b feature-new-function

# 开发完成后合并
git checkout main
git merge feature-new-function
```

---

## 🐛 常见问题

### Q1: 修改代码后没有效果？

**后端：**
- 需要手动重启后端服务
- 或使用 `--reload` 参数

**前端：**
- 检查是否保存了文件
- 检查浏览器是否自动刷新
- 手动刷新页面（Ctrl+R）

### Q2: 端口被占用？

```bash
# 查看端口占用
netstat -ano | findstr 8765

# 杀死进程
taskkill /PID <进程ID> /F
```

### Q3: 依赖安装失败？

```bash
# 后端
cd backend
pip install -r requirements.txt --upgrade

# 前端
cd electron
npm install --force
```

### Q4: 打包失败？

- 先在开发模式下确保代码能正常运行
- 检查是否有语法错误
- 查看打包日志找出错误原因

---

## 📊 开发 vs 打包对比

| 操作 | 开发模式 | 打包模式 |
|------|---------|---------|
| 启动速度 | 快（几秒） | 慢（几分钟） |
| 修改代码 | 立即生效 | 需要重新打包 |
| 调试 | 容易 | 困难 |
| 适用场景 | 开发、测试 | 发布 |
| 频率 | 每天多次 | 发布时一次 |

---

## 🎯 推荐工作流程

### 每日开发

```
1. 启动开发模式（start-dev.bat）
2. 修改代码
3. 测试功能
4. 修复 Bug
5. 提交代码（git commit）
6. 关闭开发环境
```

### 发布版本

```
1. 确认所有功能正常
2. 更新版本号
3. 执行打包（build-all.bat）
4. 测试安装包
5. 发布
6. 打 Git 标签（git tag v1.0.0）
```

---

## 📚 相关文档

- `README.md` - 项目说明
- `BUILD_GUIDE.md` - 打包指南
- `INSTALLATION_GUIDE.md` - 安装说明
- `start-dev.bat` - 开发启动脚本
- `build-all.bat` - 打包脚本

---

## 🎉 总结

**记住：**
- 开发阶段 = 开发模式（快速迭代）
- 发布阶段 = 打包模式（一次性）

不要在开发过程中频繁打包，这会浪费大量时间！

先把功能做好，测试充分，最后再打包一次就行了。
