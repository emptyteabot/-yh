import React, { useState } from 'react';
import { Card, Form, Input, InputNumber, Button, Progress, List, Tag, Alert, message } from 'antd';
import { ThunderboltOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';

interface ApplyLog {
  job: string;
  company: string;
  success: boolean;
  message: string;
}

const BossAutoApply: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState('');
  const [logs, setLogs] = useState<ApplyLog[]>([]);
  const [stats, setStats] = useState({ success: 0, failed: 0 });

  const onSubmit = async (values: any) => {
    setLoading(true);
    setProgress(0);
    setLogs([]);
    setStats({ success: 0, failed: 0 });

    try {
      // 获取简历
      const resumeResult = await fetch('http://localhost:8765/api/resume/list', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });
      const resumeData = await resumeResult.json();

      if (!resumeData.resumes || resumeData.resumes.length === 0) {
        message.error('请先上传简历');
        setLoading(false);
        return;
      }

      const firstResume = resumeData.resumes[0];
      const textResult = await fetch(`http://localhost:8765/api/resume/text/${firstResume.filename}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });
      const textData = await textResult.json();

      // WebSocket 连接
      const ws = new WebSocket('ws://localhost:8765/api/apply/ws/boss-apply');

      ws.onopen = () => {
        ws.send(JSON.stringify({
          keyword: values.keyword,
          city: values.city || '全国',
          max_count: values.max_count || 10,
          resume_text: textData.text
        }));
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.error) {
          message.error(data.message);
          setLoading(false);
          ws.close();
          return;
        }

        if (data.stage) {
          setStage(data.message);
          setProgress(data.progress * 100);
        }

        if (data.job) {
          setLogs((prev) => [
            ...prev,
            {
              job: data.job,
              company: data.company,
              success: data.success,
              message: data.success ? '投递成功' : '投递失败'
            }
          ]);

          setStats({
            success: data.success_count || 0,
            failed: data.failed_count || 0
          });
        }

        if (data.stage === 'completed') {
          message.success(data.message);
          setLoading(false);
          ws.close();
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        message.error('连接失败');
        setLoading(false);
      };

      ws.onclose = () => {
        setLoading(false);
      };
    } catch (error) {
      console.error('自动投递失败', error);
      message.error('自动投递失败: ' + error);
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '20px' }}>
      <h1 style={{ fontSize: 28, marginBottom: 8 }}>🚀 Boss 直聘自动投递</h1>
      <p style={{ color: '#666', marginBottom: 24 }}>自动搜索岗位并批量投递</p>

      <Alert
        message="使用说明"
        description="首次使用需要扫码登录 Boss 直聘,登录后会自动保存状态。系统会自动搜索岗位、生成打招呼消息并投递。"
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      <Card style={{ marginBottom: 16 }}>
        <Form layout="vertical" onFinish={onSubmit}>
          <Form.Item
            label="搜索关键词"
            name="keyword"
            rules={[{ required: true, message: '请输入搜索关键词' }]}
          >
            <Input placeholder="例如：Python工程师" size="large" />
          </Form.Item>

          <Form.Item label="城市" name="city">
            <Input placeholder="例如：北京、上海、全国" size="large" />
          </Form.Item>

          <Form.Item
            label="投递数量"
            name="max_count"
            initialValue={10}
          >
            <InputNumber min={1} max={50} style={{ width: '100%' }} size="large" />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              icon={<ThunderboltOutlined />}
              loading={loading}
              size="large"
              block
            >
              {loading ? '投递中...' : '开始自动投递'}
            </Button>
          </Form.Item>
        </Form>
      </Card>

      {loading && (
        <Card style={{ marginBottom: 16 }}>
          <Progress percent={Math.round(progress)} status="active" />
          <div style={{ textAlign: 'center', marginTop: 8, color: '#666' }}>
            {stage}
          </div>
          <div style={{ textAlign: 'center', marginTop: 8 }}>
            <Tag color="green">成功 {stats.success}</Tag>
            <Tag color="red">失败 {stats.failed}</Tag>
          </div>
        </Card>
      )}

      {logs.length > 0 && (
        <Card title="投递日志">
          <List
            dataSource={logs}
            renderItem={(log) => (
              <List.Item>
                <List.Item.Meta
                  avatar={
                    log.success ? (
                      <CheckCircleOutlined style={{ color: '#52c41a', fontSize: 20 }} />
                    ) : (
                      <CloseCircleOutlined style={{ color: '#ff4d4f', fontSize: 20 }} />
                    )
                  }
                  title={log.job}
                  description={`${log.company} - ${log.message}`}
                />
              </List.Item>
            )}
          />
        </Card>
      )}
    </div>
  );
};

export default BossAutoApply;
