import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic, Table, Tag, Spin } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined, SendOutlined, ClockCircleOutlined } from '@ant-design/icons';

interface Stats {
  total: number;
  success: number;
  failed: number;
  pending: number;
  success_rate: number;
}

interface Record {
  id: string;
  job_title: string;
  company: string;
  status: string;
  applied_at: string;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<Stats>({
    total: 0,
    success: 0,
    failed: 0,
    pending: 0,
    success_rate: 0
  });
  const [recentRecords, setRecentRecords] = useState<Record[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      // 加载统计数据
      const statsResult = await window.electronAPI.pythonCall('/api/records/stats', {});
      setStats(statsResult);

      // 加载最近记录
      const recordsResult = await window.electronAPI.pythonCall('/api/records', { limit: 5 });
      setRecentRecords(recordsResult.records || []);
    } catch (error) {
      console.error('加载数据失败', error);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: '岗位',
      dataIndex: 'job_title',
      key: 'job_title',
    },
    {
      title: '公司',
      dataIndex: 'company',
      key: 'company',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const colorMap: any = {
          success: 'green',
          failed: 'red',
          pending: 'orange'
        };
        const textMap: any = {
          success: '成功',
          failed: '失败',
          pending: '待处理'
        };
        return <Tag color={colorMap[status]}>{textMap[status]}</Tag>;
      }
    },
    {
      title: '投递时间',
      dataIndex: 'applied_at',
      key: 'applied_at',
      render: (time: string) => new Date(time).toLocaleString('zh-CN')
    }
  ];

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '100px' }}>
        <Spin size="large" tip="加载中..." />
      </div>
    );
  }

  return (
    <div>
      <h1>仪表盘</h1>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总投递数"
              value={stats.total}
              prefix={<SendOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="成功投递"
              value={stats.success}
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="失败投递"
              value={stats.failed}
              prefix={<CloseCircleOutlined />}
              valueStyle={{ color: '#ff4d4f' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="成功率"
              value={stats.success_rate}
              suffix="%"
              prefix={<ClockCircleOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
      </Row>

      <Card title="最近投递记录" style={{ marginTop: 24 }}>
        <Table
          dataSource={recentRecords}
          columns={columns}
          rowKey="id"
          pagination={false}
        />
      </Card>
    </div>
  );
};

export default Dashboard;
