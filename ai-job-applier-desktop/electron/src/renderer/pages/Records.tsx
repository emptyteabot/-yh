import React from 'react';
import { Table, Button } from 'antd';

const Records: React.FC = () => {
  const [records, setRecords] = React.useState([]);
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    loadRecords();
  }, []);

  const loadRecords = async () => {
    setLoading(true);
    try {
      const result = await window.electronAPI.pythonCall('/api/records', {});
      setRecords(result.records);
    } catch (error) {
      console.error('加载记录失败', error);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { title: '岗位名称', dataIndex: 'job_title', key: 'job_title' },
    { title: '公司', dataIndex: 'company', key: 'company' },
    { title: '状态', dataIndex: 'status', key: 'status' },
    { title: '投递时间', dataIndex: 'created_at', key: 'created_at' },
  ];

  return (
    <div>
      <h1>投递记录</h1>
      <Button onClick={loadRecords} style={{ marginBottom: 16 }}>
        刷新
      </Button>
      <Table
        dataSource={records}
        columns={columns}
        loading={loading}
        rowKey="id"
      />
    </div>
  );
};

export default Records;
