import React, { useState } from 'react';
import { Card, Button, Tabs, Alert, Space, Progress } from 'antd';
import { RobotOutlined, CheckCircleOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';

const { TabPane } = Tabs;

interface AnalysisResults {
  career_analysis?: string;
  job_recommendations?: string;
  interview_preparation?: string;
  skill_gap_analysis?: string;
}

const ResumeAnalysis: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<AnalysisResults | null>(null);
  const [currentStage, setCurrentStage] = useState('');
  const [progress, setProgress] = useState(0);

  const startAnalysis = async () => {
    // 获取简历文本
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

    setLoading(true);
    setResults(null);
    setProgress(0);

    try {
      // 模拟进度更新
      const stages = [
        { name: '职业分析师正在深度思考...', progress: 25 },
        { name: '岗位推荐专家正在匹配...', progress: 50 },
        { name: '面试辅导专家正在准备...', progress: 75 },
        { name: '质量审核官正在检查...', progress: 90 }
      ];

      let currentProgress = 0;
      const progressInterval = setInterval(() => {
        if (currentProgress < stages.length) {
          setCurrentStage(stages[currentProgress].name);
          setProgress(stages[currentProgress].progress);
          currentProgress++;
        }
      }, 5000);

      // 调用分析 API
      const result = await window.electronAPI.pythonCall('/api/analysis/resume', {
        resume_text: textResult.text,
        analysis_type: 'full'
      });

      clearInterval(progressInterval);
      setProgress(100);
      setResults(result.results);
    } catch (error) {
      console.error('分析失败', error);
      alert('分析失败: ' + error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>简历分析 - 4 个 AI Agent</h1>

      <Alert
        message="AI 简历分析"
        description="使用 4 个专业 AI Agent 深度分析您的简历：职业分析师、岗位推荐专家、面试辅导专家、质量审核官"
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      <Card style={{ marginBottom: 16 }}>
        <Space direction="vertical" style={{ width: '100%' }}>
          <Button
            type="primary"
            size="large"
            icon={<RobotOutlined />}
            onClick={startAnalysis}
            loading={loading}
            block
          >
            {loading ? '分析中...' : '开始 AI 分析'}
          </Button>

          {loading && (
            <>
              <Progress percent={progress} status="active" />
              <div style={{ textAlign: 'center', color: '#666' }}>
                {currentStage}
              </div>
            </>
          )}
        </Space>
      </Card>

      {results && (
        <Card title="分析结果">
          <Tabs defaultActiveKey="1">
            {results.career_analysis && (
              <TabPane
                tab={
                  <span>
                    <CheckCircleOutlined /> 职业分析
                  </span>
                }
                key="1"
              >
                <div style={{ padding: 16, background: '#f5f5f5', borderRadius: 8 }}>
                  <ReactMarkdown>{results.career_analysis}</ReactMarkdown>
                </div>
              </TabPane>
            )}

            {results.job_recommendations && (
              <TabPane
                tab={
                  <span>
                    <CheckCircleOutlined /> 岗位推荐
                  </span>
                }
                key="2"
              >
                <div style={{ padding: 16, background: '#f5f5f5', borderRadius: 8 }}>
                  <ReactMarkdown>{results.job_recommendations}</ReactMarkdown>
                </div>
              </TabPane>
            )}

            {results.interview_preparation && (
              <TabPane
                tab={
                  <span>
                    <CheckCircleOutlined /> 面试辅导
                  </span>
                }
                key="3"
              >
                <div style={{ padding: 16, background: '#f5f5f5', borderRadius: 8 }}>
                  <ReactMarkdown>{results.interview_preparation}</ReactMarkdown>
                </div>
              </TabPane>
            )}

            {results.skill_gap_analysis && (
              <TabPane
                tab={
                  <span>
                    <CheckCircleOutlined /> 质量审核
                  </span>
                }
                key="4"
              >
                <div style={{ padding: 16, background: '#f5f5f5', borderRadius: 8 }}>
                  <ReactMarkdown>{results.skill_gap_analysis}</ReactMarkdown>
                </div>
              </TabPane>
            )}
          </Tabs>
        </Card>
      )}
    </div>
  );
};

export default ResumeAnalysis;
