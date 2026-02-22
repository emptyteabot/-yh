import React, { useState, useEffect } from 'react';
import { Form, Input, Button, Card, List, Tag, Space, Checkbox, message, Alert, Badge } from 'antd';
import { SearchOutlined, EnvironmentOutlined, DollarOutlined, ThunderboltOutlined } from '@ant-design/icons';

interface Job {
  job_id: string;
  title: string;
  company: string;
  salary: string;
  location: string;
  experience: string;
  education: string;
  description: string;
  skills: string[];
  welfare: string[];
}

const OpenClawSearch: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedJobs, setSelectedJobs] = useState<string[]>([]);
  const [openclawAvailable, setOpenclawAvailable] = useState(false);
  const [source, setSource] = useState('');

  useEffect(() => {
    checkOpenClawStatus();
  }, []);

  const checkOpenClawStatus = async () => {
    try {
      const result = await window.electronAPI.pythonCall('/api/openclaw/status', {});
      setOpenclawAvailable(result.available);
    } catch (error) {
      console.error('检查 OpenClaw 状态失败', error);
    }
  };

  const onSearch = async (values: any) => {
    setLoading(true);
    try {
      const result = await window.electronAPI.pythonCall('/api/openclaw/search', values);
      setJobs(result.jobs || []);
      setSource(result.source);
      setSelectedJobs([]);

      if (result.jobs && result.jobs.length > 0) {
        message.success(`找到 ${result.jobs.length} 个岗位（${result.source === 'openclaw' ? '真实数据' : '模拟数据'}）`);
      } else {
        message.info('未找到匹配的岗位');
      }
    } catch (error) {
      console.error('搜索失败', error);
      message.error('搜索失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectJob = (jobId: string, checked: boolean) => {
    if (checked) {
      setSelectedJobs([...selectedJobs, jobId]);
    } else {
      setSelectedJobs(selectedJobs.filter(id => id !== jobId));
    }
  };

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedJobs(jobs.map(job => job.job_id));
    } else {
      setSelectedJobs([]);
    }
  };

  return (
    <div>
      <h1>
        OpenClaw 岗位搜索
        <Badge
          count={openclawAvailable ? '可用' : '不可用'}
          style={{
            backgroundColor: openclawAvailable ? '#52c41a' : '#ff4d4f',
            marginLeft: 16
          }}
        />
      </h1>

      <Alert
        message={openclawAvailable ? 'OpenClaw 已连接' : 'OpenClaw 未连接'}
        description={
          openclawAvailable
            ? '将搜索 Boss直聘真实岗位数据'
            : '将使用模拟数据，请安装 OpenClaw 以获取真实数据'
        }
        type={openclawAvailable ? 'success' : 'warning'}
        showIcon
        style={{ marginBottom: 24 }}
      />

      <Card style={{ marginBottom: 16 }}>
        <Form layout="inline" onFinish={onSearch}>
          <Form.Item
            name="keywords"
            label="关键词"
            rules={[{ required: true, message: '请输入关键词' }]}
          >
            <Input
              placeholder="例如：Python工程师"
              prefix={<SearchOutlined />}
              style={{ width: 200 }}
            />
          </Form.Item>

          <Form.Item name="location" label="地点" initialValue="全国">
            <Input
              placeholder="例如：北京"
              prefix={<EnvironmentOutlined />}
              style={{ width: 150 }}
            />
          </Form.Item>

          <Form.Item name="salary_min" label="最低薪资">
            <Input
              placeholder="例如：15"
              prefix={<DollarOutlined />}
              suffix="K"
              type="number"
              style={{ width: 120 }}
            />
          </Form.Item>

          <Form.Item name="limit" label="数量" initialValue={50}>
            <Input type="number" style={{ width: 80 }} />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>
              搜索
            </Button>
          </Form.Item>
        </Form>
      </Card>

      {jobs.length > 0 && (
        <>
          <Card style={{ marginBottom: 16 }}>
            <Space>
              <Checkbox
                checked={selectedJobs.length === jobs.length}
                indeterminate={selectedJobs.length > 0 && selectedJobs.length < jobs.length}
                onChange={(e) => handleSelectAll(e.target.checked)}
              >
                全选
              </Checkbox>
              <Button
                type="primary"
                icon={<ThunderboltOutlined />}
                disabled={selectedJobs.length === 0}
                onClick={() => {
                  message.info('请前往"智能投递"页面进行批量投递');
                  window.location.hash = '/smart-apply';
                }}
              >
                批量投递 ({selectedJobs.length})
              </Button>
              {source && (
                <Tag color={source === 'openclaw' ? 'green' : 'orange'}>
                  {source === 'openclaw' ? '真实数据' : '模拟数据'}
                </Tag>
              )}
            </Space>
          </Card>

          <List
            dataSource={jobs}
            renderItem={(job) => (
              <List.Item>
                <Card
                  style={{ width: '100%' }}
                  hoverable
                  extra={
                    <Checkbox
                      checked={selectedJobs.includes(job.job_id)}
                      onChange={(e) => handleSelectJob(job.job_id, e.target.checked)}
                    />
                  }
                >
                  <h3>{job.title}</h3>
                  <Space size="large" style={{ marginBottom: 8 }}>
                    <span>{job.company}</span>
                    <Tag color="blue">{job.salary}</Tag>
                    <Tag icon={<EnvironmentOutlined />}>{job.location}</Tag>
                  </Space>
                  <div style={{ marginTop: 8 }}>
                    <Tag>{job.experience}</Tag>
                    <Tag>{job.education}</Tag>
                    {job.skills.map((skill, i) => (
                      <Tag key={i} color="cyan">{skill}</Tag>
                    ))}
                  </div>
                  {job.welfare.length > 0 && (
                    <div style={{ marginTop: 8 }}>
                      {job.welfare.map((w, i) => (
                        <Tag key={i} color="green">{w}</Tag>
                      ))}
                    </div>
                  )}
                  <p style={{ marginTop: 12, color: '#666' }}>
                    {job.description.substring(0, 150)}...
                  </p>
                </Card>
              </List.Item>
            )}
          />
        </>
      )}
    </div>
  );
};

export default OpenClawSearch;
