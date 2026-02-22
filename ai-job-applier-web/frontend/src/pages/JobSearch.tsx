import React, { useState } from 'react';
import { Form, Input, Button, Card, List, Tag, Space, Checkbox, message, Empty } from 'antd';
import { SearchOutlined, EnvironmentOutlined, DollarOutlined } from '@ant-design/icons';

interface Job {
  job_id: string;
  title: string;
  company: string;
  salary: string;
  location: string;
  experience: string;
  education: string;
  description: string;
  url: string;
}

const JobSearch: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedJobs, setSelectedJobs] = useState<string[]>([]);

  const onSearch = async (values: any) => {
    setLoading(true);
    try {
      const result = await window.electronAPI.pythonCall('/api/jobs/search', values);
      setJobs(result.jobs || []);
      setSelectedJobs([]);
      if (result.jobs && result.jobs.length > 0) {
        message.success(`找到 ${result.jobs.length} 个岗位`);
      } else {
        message.info('未找到匹配的岗位');
      }
    } catch (error) {
      console.error('搜索失败', error);
      message.error('搜索失败，请检查是否已登录');
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

  const handleBatchApply = () => {
    if (selectedJobs.length === 0) {
      message.warning('请先选择要投递的岗位');
      return;
    }
    // 保存选中的岗位到 localStorage
    localStorage.setItem('selectedJobs', JSON.stringify(selectedJobs));
    message.success(`已选择 ${selectedJobs.length} 个岗位`);
    // 跳转到投递页面
    window.location.hash = '/apply';
  };

  return (
    <div>
      <h1>岗位搜索</h1>

      <Card style={{ marginBottom: 16 }}>
        <Form layout="inline" onFinish={onSearch}>
          <Form.Item
            name="keywords"
            label="关键词"
            rules={[{ required: true, message: '请输入关键词' }]}
          >
            <Input
              placeholder="例如：Python实习"
              prefix={<SearchOutlined />}
              style={{ width: 200 }}
            />
          </Form.Item>
          <Form.Item name="location" label="地点">
            <Input
              placeholder="例如：北京"
              prefix={<EnvironmentOutlined />}
              style={{ width: 150 }}
            />
          </Form.Item>
          <Form.Item name="salary_min" label="最低薪资">
            <Input
              placeholder="例如：8000"
              prefix={<DollarOutlined />}
              type="number"
              style={{ width: 120 }}
            />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>
              搜索
            </Button>
          </Form.Item>
        </Form>
      </Card>

      {jobs.length > 0 && (
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
              disabled={selectedJobs.length === 0}
              onClick={handleBatchApply}
            >
              批量投递 ({selectedJobs.length})
            </Button>
          </Space>
        </Card>
      )}

      {jobs.length === 0 ? (
        <Empty description="暂无搜索结果" />
      ) : (
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
                </div>
                <p style={{ marginTop: 12, color: '#666' }}>
                  {job.description.substring(0, 100)}...
                </p>
              </Card>
            </List.Item>
          )}
        />
      )}
    </div>
  );
};

export default JobSearch;
