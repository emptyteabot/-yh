import { spawn, ChildProcess } from 'child_process';
import axios from 'axios';
import * as path from 'path';

export class PythonBridge {
  private process: ChildProcess | null = null;
  private port = 8765;
  private baseUrl = `http://localhost:${this.port}`;

  async start() {
    console.log('Starting Python backend...');

    // 检查后端是否已经在运行
    try {
      await axios.get(`${this.baseUrl}/health`);
      console.log('Python backend is already running');
      return;
    } catch (error) {
      // 后端未运行，继续启动
    }

    // 开发环境：直接运行 Python 脚本
    // 生产环境：运行打包后的 .exe
    const isDev = process.env.NODE_ENV === 'development' || !process.resourcesPath;

    let pythonPath: string;
    let args: string[];

    if (isDev) {
      // 开发环境 - 使用绝对路径
      pythonPath = 'python';
      const backendPath = path.resolve(__dirname, '../../../backend/main.py');
      args = [backendPath, '--port', String(this.port)];
      console.log('Development mode: Using Python script');
    } else {
      // 生产环境
      pythonPath = path.join(process.resourcesPath, 'backend', 'ai-job-backend.exe');
      args = ['--port', String(this.port)];
      console.log('Production mode: Using packaged exe');
    }

    console.log(`Python path: ${pythonPath}`);
    console.log(`Args: ${args.join(' ')}`);

    this.process = spawn(pythonPath, args, {
      stdio: 'pipe',
      shell: true,  // 使用 shell 执行
    });

    this.process.stdout?.on('data', (data) => {
      console.log(`[Python] ${data.toString()}`);
    });

    this.process.stderr?.on('data', (data) => {
      console.error(`[Python Error] ${data.toString()}`);
    });

    this.process.on('close', (code) => {
      console.log(`Python process exited with code ${code}`);
    });

    this.process.on('error', (error) => {
      console.error(`Failed to start Python process: ${error.message}`);
    });

    // 等待服务器启动
    await this.waitForServer();
    console.log('Python backend started successfully');
  }

  private async waitForServer(maxRetries = 30, interval = 1000): Promise<void> {
    for (let i = 0; i < maxRetries; i++) {
      try {
        await axios.get(`${this.baseUrl}/health`);
        return;
      } catch (error) {
        await new Promise((resolve) => setTimeout(resolve, interval));
      }
    }
    throw new Error('Failed to start Python backend');
  }

  async call(endpoint: string, data: any): Promise<any> {
    try {
      const response = await axios.post(`${this.baseUrl}${endpoint}`, data);
      return response.data;
    } catch (error: any) {
      console.error(`API call failed: ${endpoint}`, error.message);
      throw error;
    }
  }

  stop() {
    if (this.process) {
      console.log('Stopping Python backend...');
      this.process.kill();
      this.process = null;
    }
  }
}
