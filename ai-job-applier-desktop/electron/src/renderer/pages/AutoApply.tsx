import React from 'react';
import { Button, Progress, Card, Input, message, Switch, Space } from 'antd';

const { TextArea } = Input;

const AutoApply: React.FC = () => {
  const [progress, setProgress] = React.useState(0);
  const [logs, setLogs] = React.useState<string[]>([]);
  const [isRunning, setIsRunning] = React.useState(false);
  const [resumeText, setResumeText] = React.useState('');
  const [useAI, setUseAI] = React.useState(true);
  const [selectedJobs, setSelectedJobs] = React.useState<string[]>([]);

  React.useEffect(() => {
    // 从 localStorage 获取选中的岗位
    const jobs = localStorage.getItem('selectedJobs');
    if (jobs) {
      setSelectedJobs(JSON.parse(jobs));
    }
  }, []);

  const startApply = async () => {
    if (selectedJobs.length === 0) {
      message.warning('请先在岗位搜索页面选择要投递的岗位');
      return;
    }

    if (!resumeText.trim()) {
      message.warning('请输入简历内容');
      return;
    }

    setIsRunning(true);
    setProgress(0);
    setLogs([]);

    try {
      // 获取后端端口
      const backendPort = 8000; // 根据实际情况调整
      const ws = new WebSocket(`ws://localhost:${backendPort}/api/apply/ws/apply`);

      ws.onopen = () => {
        // 发送投递任务
        ws.send(JSON.stringify({
          job_ids: selectedJobs,
          resume_text: resumeText,
          use_ai_cover_letter: useAI
        }));
        setLogs((prev) => [...prev, '开始批量投递...']);
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.error) {
          message.error(data.message);
          setLogs((prev) => [...prev, `❌ 错误: ${data.message}`]);
          setIsRunning(false);
          return;
        }

        if (data.completed) {
          message.success(data.message);
          setLogs((prev) => [...prev, `✅ ${data.message}`]);
          setIsRunning(false);
          // 清除已投递的岗位
          localStorage.removeItem('selectedJobs');
          return;
        }

        // 更新进度
        if (data.progress !== undefined) {
          setProgress(data.progress * 100);
          const status = data.success ? '✅ 成功' : '❌ 失败';
          setLogs((prev) => [
            ...prev,
            `[${data.current}/${data.total}] ${data.company} - ${data.job} ${status}`
          ]);
        }
      };

      ws.onclose = () => {
        setIsRunning(false);
        setLogs((prev) => [...prev, '连接已关闭']);
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        message.error('连接失败，请检查后端是否运行');
        setIsRunning(false);
        setLogs((prev) => [...prev, '❌ 连接失败']);
      };
    } catch (error) {
      console.error('投递失败', error);
      message.error('投递失败');
      setIsRunning(false);
    }
  };

  return (
    <div>
      <h1>自动投递</h1>
      
      <Card style={{ marginBottom: 16 }}>
        <Space direction="vertical" style={{ width: '100%' }}>
          <div>
            <strong>已选择岗位：</strong> {selectedJobs.length} 个
          </div>
          
          <div>
            <strong>简历内容：</strong>
            <TextArea
              rows={6}
              placeholder="请输入或粘贴您的简历内容，用于 AI 生成个性化求职信"
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              disabled={isRunning}
            />
          </div>

          <div>
            <Space>
              <strong>使用 AI 生成求职信：</strong>
              <Switch checked={useAI} onChange={setUseAI} disabled={isRunning} />
            </Space>
          </div>
        </Space>
      </Card>

      <Card style={{ marginBottom: 16 }}>
        <Progress percent={Math.round(progress)} status={isRunning ? 'active' : 'normal'} />
        <Button
          type="primary"
          onClick={startApply}
          disabled={isRunning || selectedJobs.length === 0}
          style={{ marginTop: 16 }}
          size="large"
        >
          {isRunning ? '投递中...' : `开始投递 (${selectedJobs.length} 个岗位)`}
        </Button>
      </Card>

      <Card title="投递日志">
        <div style={{ maxHeight: 400, overflow: 'auto', fontFamily: 'monospace' }}>
          {logs.length === 0 ? (
            <div style={{ color: '#999' }}>暂无日志</div>
          ) : (
            logs.map((log, i) => (
              <div key={i} style={{ padding: '4px 0' }}>{log}</div>
            ))
          )}
        </div>
      </Card>
    </div>
  );
};

export default AutoApply;
