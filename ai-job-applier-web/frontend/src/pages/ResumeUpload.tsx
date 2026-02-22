import React, { useState, useEffect } from 'react';
import { Upload, Button, message, Card, List, Typography, Popconfirm } from 'antd';
import { UploadOutlined, DeleteOutlined, FileTextOutlined } from '@ant-design/icons';

const { Text, Paragraph } = Typography;

interface Resume {
  filename: string;
  size: number;
  path: string;
}

const ResumeUpload: React.FC = () => {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedResume, setSelectedResume] = useState<string>('');
  const [resumeText, setResumeText] = useState<string>('');

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
      console.error('加载简历列表失败', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (file: File) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      // 直接使用 fetch 上传文件
      const response = await fetch('http://localhost:8765/api/resume/upload', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      if (result.success) {
        message.success('简历上传成功');
        loadResumes();
      } else {
        message.error(result.detail || '简历上传失败');
      }
    } catch (error) {
      console.error('上传错误:', error);
      message.error('简历上传失败');
    } finally {
      setLoading(false);
    }
    return false;
  };

  const handleDelete = async (filename: string) => {
    try {
      const response = await fetch(`http://localhost:8765/api/resume/${filename}`, {
        method: 'DELETE'
      });

      const result = await response.json();

      if (result.success) {
        message.success('简历删除成功');
        loadResumes();
        if (selectedResume === filename) {
          setSelectedResume('');
          setResumeText('');
        }
      } else {
        message.error('简历删除失败');
      }
    } catch (error) {
      message.error('简历删除失败');
    }
  };

  const handleView = async (filename: string) => {
    try {
      const response = await fetch(`http://localhost:8765/api/resume/text/${filename}`);
      const result = await response.json();

      if (result.success) {
        setSelectedResume(filename);
        setResumeText(result.text || '');
      } else {
        message.error('加载简历内容失败');
      }
    } catch (error) {
      message.error('加载简历内容失败');
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  return (
    <div>
      <h1>简历管理</h1>

      <Card style={{ marginBottom: 16 }}>
        <Upload
          beforeUpload={handleUpload}
          accept=".pdf,.doc,.docx"
          maxCount={1}
          showUploadList={false}
        >
          <Button icon={<UploadOutlined />} type="primary" size="large">
            上传简历
          </Button>
        </Upload>
        <Text type="secondary" style={{ marginLeft: 16 }}>
          支持 PDF、Word 格式，最大 10MB
        </Text>
      </Card>

      <Card title="我的简历" loading={loading}>
        <List
          dataSource={resumes}
          renderItem={(resume) => (
            <List.Item
              actions={[
                <Button
                  type="link"
                  icon={<FileTextOutlined />}
                  onClick={() => handleView(resume.filename)}
                >
                  查看
                </Button>,
                <Popconfirm
                  title="确定删除这份简历吗？"
                  onConfirm={() => handleDelete(resume.filename)}
                  okText="确定"
                  cancelText="取消"
                >
                  <Button type="link" danger icon={<DeleteOutlined />}>
                    删除
                  </Button>
                </Popconfirm>
              ]}
            >
              <List.Item.Meta
                avatar={<FileTextOutlined style={{ fontSize: 24 }} />}
                title={resume.filename}
                description={`大小: ${formatFileSize(resume.size)}`}
              />
            </List.Item>
          )}
        />
      </Card>

      {selectedResume && (
        <Card title={`简历内容 - ${selectedResume}`} style={{ marginTop: 16 }}>
          <Paragraph
            ellipsis={{ rows: 10, expandable: true, symbol: '展开' }}
            style={{ whiteSpace: 'pre-wrap' }}
          >
            {resumeText}
          </Paragraph>
        </Card>
      )}
    </div>
  );
};

export default ResumeUpload;
