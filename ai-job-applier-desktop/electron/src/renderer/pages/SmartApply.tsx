import React, { useState } from 'react';
import { Card, Form, Button, Select, InputNumber, Progress, List, Tag, Alert } from 'antd';
import { ThunderboltOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';

const { Option } = Select;

interface ApplyLog {
  job: string;
  company: string;
  success: boolean;
  message: string;
}

const SmartApply: React.FC = () => {
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
      const resumeResult = await window.electronAPI.pythonCall('/api/resume/list', {});
      if (!resumeResult.resumes || resumeResult.resumes.length === 0) {
        alert('请先上传简历');
        return;
      }

      const firstResume = resumeResult.resumes[0];
      const textResult = await window.electronAPI.pythonCall(
        `/api/resume/text/${firstResume.filename}`,
        {}
      );

      // WebSocket 连接
      const ws = new WebSocket('ws://localhost:8765/api/smart-apply/ws/smart-apply');

      ws.onopen = () => {
        ws.send(JSON.stringify({
          resume_text: textResult.text,
          target_positions: values.positions,
          target_locations: values.locations,
          salary_min: values.salary_min,
          max_applications: values.max_applications
        }));
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

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
          setLoading(false);
          ws.close();
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setLoading(false);
      };

      ws.onclose = () => {
        setLoading(false);
      };
    } catch (error) {
      console.error('智能投递失败', error);
      alert('智能投递失败: ' + error);
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>智能投递</h1>

      <Alert
        message="智能投递说明"
        description="系统会自动搜索匹配岗位、分析简历、生成个性化求职信并批量投递"
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      <Card style={{ marginBottom: 16 }}>
        <Form layout="vertical" onFinish={onSubmit}>
          <Form.Item
            label="目标岗位"
            name="positions"
            rules={[{ required: true, message: '请输入目标岗位' }]}
          >
            <Select mode="tags" placeholder="例如：Python工程师、后端开发">
              <Option value="Python工程师">Python工程师</Option>
              <Option value="后端开发">后端开发</Option>
              <Option value="全栈工程师">全栈工程师</Option>
              <Option value="AI工程师">AI工程师</Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="目标城市"
            name="locations"
            rules={[{ required: true, message: '请选择目标城市' }]}
          >
            <Select mode="tags" placeholder="例如：北京、上海">
              <Option value="北京">北京</Option>
              <Option value="上海">上海</Option>
              <Option value="深圳">深圳</Option>
              <Option value="杭州">杭州</Option>
              <Option value="广州">广州</Option>
            </Select>
          </Form.Item>

          <Form.Item label="最低薪资（K）" name="salary_min">
            <InputNumber min={0} max={100} style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            label="最大投递数"
            name="max_applications"
            initialValue={50}
          >
            <InputNumber min={1} max={200} style={{ width: '100%' }} />
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
              {loading ? '投递中...' : '开始智能投递'}
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

export default SmartApply;
