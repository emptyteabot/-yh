import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Button, Progress, List, Tag, message, Statistic, Row, Col, Alert, Modal } from 'antd';
import { ThunderboltOutlined, CheckCircleOutlined, CloseCircleOutlined, UserOutlined, CrownOutlined } from '@ant-design/icons';

interface User {
  id: string;
  phone: string;
  nickname: string;
  plan: string;
  remaining_quota: number;
}

interface ApplyLog {
  job: string;
  company: string;
  greeting: string;
  success: boolean;
}

const SmartApply: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState('');
  const [logs, setLogs] = useState<ApplyLog[]>([]);
  const [stats, setStats] = useState({ success: 0, failed: 0 });
  const [showLogin, setShowLogin] = useState(false);
  const [showUpgrade, setShowUpgrade] = useState(false);

  // 登录表单
  const [loginForm] = Form.useForm();
  const [resumeText, setResumeText] = useState('');

  useEffect(() => {
    // 从 localStorage 读取 token
    const savedToken = localStorage.getItem('token');
    if (savedToken) {
      setToken(savedToken);
      loadUserInfo(savedToken);
    } else {
      setShowLogin(true);
    }
  }, []);

  const loadUserInfo = async (authToken: string) => {
    try {
      const response = await fetch('http://localhost:8765/api/user/info', {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      });
      const data = await response.json();
      if (data.success) {
        setUser(data.user);
      }
    } catch (error) {
      console.error('加载用户信息失败', error);
    }
  };

  const handleLogin = async (values: any) => {
    try {
      // 先发送验证码
      await fetch(`http://localhost:8765/api/auth/send-code?phone=${values.phone}`, {
        method: 'POST'
      });

      // 登录
      const response = await fetch('http://localhost:8765/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          phone: values.phone,
          code: values.code || '123456'
        })
      });

      const data = await response.json();

      if (data.success) {
        setToken(data.token);
        setUser(data.user);
        localStorage.setItem('token', data.token);
        setShowLogin(false);
        message.success('登录成功！');
      } else {
        // 如果用户不存在，自动注册
        const registerResponse = await fetch('http://localhost:8765/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            phone: values.phone,
            code: values.code || '123456',
            nickname: values.phone
          })
        });

        const registerData = await registerResponse.json();
        if (registerData.success) {
          setToken(registerData.token);
          setUser(registerData.user);
          localStorage.setItem('token', registerData.token);
          setShowLogin(false);
          message.success('注册成功！赠送 5 次免费投递');
        }
      }
    } catch (error) {
      message.error('登录失败，请重试');
    }
  };

  const handleUpgrade = async (plan: string) => {
    try {
      const response = await fetch('http://localhost:8765/api/user/upgrade', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ plan })
      });

      const data = await response.json();
      if (data.success) {
        setUser(data.user);
        setShowUpgrade(false);
        message.success(data.message);
      }
    } catch (error) {
      message.error('升级失败');
    }
  };

  const onSubmit = async (values: any) => {
    if (!user) {
      message.warning('请先登录');
      setShowLogin(true);
      return;
    }

    if (user.remaining_quota <= 0) {
      message.warning('投递次数已用完，请升级套餐');
      setShowUpgrade(true);
      return;
    }

    if (!resumeText.trim()) {
      message.warning('请输入简历内容');
      return;
    }

    setLoading(true);
    setProgress(0);
    setLogs([]);
    setStats({ success: 0, failed: 0 });

    try {
      const ws = new WebSocket('ws://localhost:8765/api/apply/ws');

      ws.onopen = () => {
        ws.send(JSON.stringify({
          token: token,
          keyword: values.keyword,
          city: values.city || '全国',
          max_count: values.max_count || 10,
          resume_text: resumeText
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
              greeting: data.greeting,
              success: data.success
            }
          ]);

          setStats({
            success: data.success_count || 0,
            failed: data.failed_count || 0
          });

          // 更新用户剩余次数
          if (user) {
            setUser({ ...user, remaining_quota: data.remaining_quota });
          }
        }

        if (data.stage === 'completed') {
          message.success(data.message);
          setLoading(false);
          ws.close();
        }
      };

      ws.onerror = () => {
        message.error('连接失败');
        setLoading(false);
      };

      ws.onclose = () => {
        setLoading(false);
      };
    } catch (error) {
      message.error('投递失败');
      setLoading(false);
    }
  };

  const getPlanName = (plan: string) => {
    const names: any = {
      'free': '免费版',
      'basic': '基础版',
      'pro': '专业版',
      'yearly': '年费版'
    };
    return names[plan] || plan;
  };

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: '20px' }}>
      {/* 顶部用户信息 */}
      {user && (
        <Card style={{ marginBottom: 16, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
          <Row gutter={16}>
            <Col span={6}>
              <Statistic
                title={<span style={{ color: '#fff' }}>当前套餐</span>}
                value={getPlanName(user.plan)}
                prefix={<CrownOutlined />}
                valueStyle={{ color: '#fff' }}
              />
            </Col>
            <Col span={6}>
              <Statistic
                title={<span style={{ color: '#fff' }}>剩余次数</span>}
                value={user.remaining_quota}
                suffix="次"
                valueStyle={{ color: '#fff' }}
              />
            </Col>
            <Col span={6}>
              <Statistic
                title={<span style={{ color: '#fff' }}>今日成功</span>}
                value={stats.success}
                suffix="个"
                valueStyle={{ color: '#52c41a' }}
              />
            </Col>
            <Col span={6}>
              <Button
                type="primary"
                size="large"
                onClick={() => setShowUpgrade(true)}
                style={{ marginTop: 20 }}
              >
                升级套餐
              </Button>
            </Col>
          </Row>
        </Card>
      )}

      <h1 style={{ fontSize: 28, marginBottom: 8 }}>🚀 AI 求职助手 - 云端版</h1>
      <p style={{ color: '#666', marginBottom: 24 }}>自动搜索岗位并批量投递，AI 生成个性化求职信</p>

      <Alert
        message="使用说明"
        description="输入关键词和城市，系统会自动搜索岗位、生成打招呼消息并投递。每次投递消耗 1 次额度。"
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      {/* 投递表单 */}
      <Card style={{ marginBottom: 16 }}>
        <Form layout="vertical" onFinish={onSubmit}>
          <Form.Item
            label="搜索关键词"
            name="keyword"
            rules={[{ required: true, message: '请输入搜索关键词' }]}
          >
            <Input placeholder="例如：Python实习、前端开发" size="large" />
          </Form.Item>

          <Form.Item label="城市" name="city">
            <Input placeholder="例如：北京、上海、全国" size="large" />
          </Form.Item>

          <Form.Item
            label="投递数量"
            name="max_count"
            initialValue={10}
          >
            <Input type="number" min={1} max={50} size="large" />
          </Form.Item>

          <Form.Item label="简历内容" required>
            <Input.TextArea
              rows={6}
              placeholder="粘贴你的简历内容..."
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
            />
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

      {/* 进度显示 */}
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

      {/* 投递日志 */}
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
                  title={`${log.job} - ${log.company}`}
                  description={
                    <>
                      <div style={{ color: '#666', marginTop: 4 }}>
                        打招呼消息：{log.greeting}
                      </div>
                      <Tag color={log.success ? 'success' : 'error'} style={{ marginTop: 4 }}>
                        {log.success ? '投递成功' : '投递失败'}
                      </Tag>
                    </>
                  }
                />
              </List.Item>
            )}
          />
        </Card>
      )}

      {/* 登录弹窗 */}
      <Modal
        title="登录 / 注册"
        open={showLogin}
        footer={null}
        onCancel={() => setShowLogin(false)}
      >
        <Form form={loginForm} onFinish={handleLogin} layout="vertical">
          <Form.Item
            label="手机号"
            name="phone"
            rules={[{ required: true, message: '请输入手机号' }]}
          >
            <Input placeholder="请输入手机号" size="large" />
          </Form.Item>

          <Form.Item
            label="验证码"
            name="code"
          >
            <Input placeholder="开发环境自动填充" size="large" />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" size="large" block>
              登录 / 注册
            </Button>
          </Form.Item>

          <Alert
            message="开发环境提示"
            description="验证码已自动填充为 123456，直接点击登录即可"
            type="info"
            showIcon
          />
        </Form>
      </Modal>

      {/* 升级套餐弹窗 */}
      <Modal
        title="升级套餐"
        open={showUpgrade}
        footer={null}
        onCancel={() => setShowUpgrade(false)}
        width={800}
      >
        <Row gutter={16}>
          <Col span={8}>
            <Card
              hoverable
              onClick={() => handleUpgrade('basic')}
              style={{ textAlign: 'center' }}
            >
              <h3>基础版</h3>
              <div style={{ fontSize: 32, color: '#1890ff', margin: '20px 0' }}>
                ¥19.9<span style={{ fontSize: 14 }}>/月</span>
              </div>
              <div>每天 30 次投递</div>
              <div>AI 生成求职信</div>
              <div>投递记录管理</div>
              <Button type="primary" style={{ marginTop: 20 }}>
                立即升级
              </Button>
            </Card>
          </Col>

          <Col span={8}>
            <Card
              hoverable
              onClick={() => handleUpgrade('pro')}
              style={{ textAlign: 'center', borderColor: '#1890ff' }}
            >
              <Tag color="blue">推荐</Tag>
              <h3>专业版</h3>
              <div style={{ fontSize: 32, color: '#1890ff', margin: '20px 0' }}>
                ¥39.9<span style={{ fontSize: 14 }}>/月</span>
              </div>
              <div>每天 100 次投递</div>
              <div>优先投递</div>
              <div>简历优化建议</div>
              <div>数据分析报告</div>
              <Button type="primary" style={{ marginTop: 20 }}>
                立即升级
              </Button>
            </Card>
          </Col>

          <Col span={8}>
            <Card
              hoverable
              onClick={() => handleUpgrade('yearly')}
              style={{ textAlign: 'center' }}
            >
              <Tag color="gold">超值</Tag>
              <h3>年费版</h3>
              <div style={{ fontSize: 32, color: '#1890ff', margin: '20px 0' }}>
                ¥199<span style={{ fontSize: 14 }}>/年</span>
              </div>
              <div>无限次投递</div>
              <div>所有功能</div>
              <div>专属客服</div>
              <div>优先更新</div>
              <Button type="primary" style={{ marginTop: 20 }}>
                立即升级
              </Button>
            </Card>
          </Col>
        </Row>

        <Alert
          message="开发环境提示"
          description="点击套餐卡片即可模拟升级，无需实际支付"
          type="info"
          showIcon
          style={{ marginTop: 16 }}
        />
      </Modal>
    </div>
  );
};

export default SmartApply;
