import { app, BrowserWindow, ipcMain } from 'electron';
import * as path from 'path';
import { PythonBridge } from './python-bridge';

let mainWindow: BrowserWindow | null = null;
let pythonBridge: PythonBridge | null = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, '../preload/index.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  // 开发环境加载 Vite 服务器
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(async () => {
  // 启动 Python 后端
  pythonBridge = new PythonBridge();
  await pythonBridge.start();

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (pythonBridge) {
    pythonBridge.stop();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC 通信处理
ipcMain.handle('python-call', async (_event, endpoint: string, data: any) => {
  if (!pythonBridge) {
    throw new Error('Python backend not initialized');
  }
  return await pythonBridge.call(endpoint, data);
});
