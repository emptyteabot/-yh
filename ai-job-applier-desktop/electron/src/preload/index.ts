import { contextBridge, ipcRenderer } from 'electron';

// 暴露安全的 API 给渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  // 调用 Python 后端
  pythonCall: (endpoint: string, data: any) =>
    ipcRenderer.invoke('python-call', endpoint, data),

  // 其他可能需要的 API
  platform: process.platform,
});

// TypeScript 类型定义
export interface ElectronAPI {
  pythonCall: (endpoint: string, data: any) => Promise<any>;
  platform: string;
}

declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}
