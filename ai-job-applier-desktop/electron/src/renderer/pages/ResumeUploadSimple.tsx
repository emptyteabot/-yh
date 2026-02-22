import React, { useState, useEffect } from 'react';
import { Upload, Button, message, Card, Spin, Typography, Space, Divider } from 'antd';
import { UploadOutlined, FileTextOutlined, CheckCircleOutlined } from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;

interface Resume {
  filename: string;
  size: number;
}

const ResumeUploadSimple: React.FC = () => {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    loadResumes();
  }, []);

  const loadResumes = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8765/api/resume/list');
      const result = await response.json();
      if (result.success) {
        setResumes(result.resumes || []);
      }
    } catch (error) {
      console.error('加载失败', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (file: File) => {
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8765/api/resume/upload', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      if (result.success) {
        message.success('✅ 简历上传成功');
        loadResumes();
      } else {
        message.error(result.detail || '上传失败');
      }
    } catch (error) {
      console.error('上传错误:', error);
      message.error('上传失败，请重试');
    } finally {
      setUploading(false);
    }
    return false;
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '20px' }}>
      {/* 标题 */}
      <Title level={2}>📄 简历管理</Title>
      <Divider />

      {/* 上传区域 */}
      <Card
        style={{
          marginBottom: 24,
          background: '#f8f9fa',
          border: '2px dashed #d9d9d9'
        }}
      >
        <Space direction="vertical" size="middle" style={{ width: '100%', textAlign: 'center' }}>
          <FileTextOutlined style={{ fontSize: 48, color: '#1890ff' }} />

          <Upload
            beforeUpload={handleUpload}
            accept=".pdf,.doc,.docx"
            maxCount={1}
            showUploadList={false}
            disabled={uploading}
          >
            <Button
              icon={<UploadOutlined />}
              type="primary"
              size="large"
              loading={uploading}
              style={{ minWidth: 200 }}
            >
              {uploading ? '上传中...' : '上传简历'}
            </Button>
          </Upload>

          <Text type="secondary">
            支持 PDF、Word 格式 | 最大 10MB
          </Text>
        </Space>
      </Card>

      {/* 已上传的简历列表 */}
      <Card title="📋 我的简历" loading={loading}>
        {resumes.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px 0' }}>
            <Text type="secondary">还没有上传简历</Text>
          </div>
        ) : (
          <Space direction="vertical" size="middle" style={{ width: '100%' }}>
            {resumes.map((resume, index) => (
              <Card
                key={index}
                size="small"
                style={{ background: '#fafafa' }}
              >
                <Space>
                  <CheckCircleOutlined style={{ color: '#52c41a', fontSize: 20 }} />
                  <div>
                    <Text strong>{resume.filename}</Text>
                    <br />
                    <Text type="secondary" style={{ fontSize: 12 }}>
                      {formatFileSize(resume.size)}
                    </Text>
                  </div>
                </Space>
              </Card>
            ))}
          </Space>
        )}
      </Card>

      {/* 提示信息 */}
      {resumes.length > 0 && (
        <Card
          style={{
            marginTop: 24,
            background: '#e6f7ff',
            border: '1px solid #91d5ff'
          }}
        >
          <Space>
            <CheckCircleOutlined style={{ color: '#1890ff' }} />
            <Text>
              简历已上传成功！现在可以进行 <Text strong>AI 分析</Text> 或 <Text strong>自动投递</Text>
            </Text>
          </Space>
        </Card>
      )}
    </div>
  );
};

export default ResumeUploadSimple;
