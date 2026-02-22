import React, { useState } from 'react';
import { Form, Input, Button, Card, message, Switch, Alert } from 'antd';
import { PhoneOutlined, LoginOutlined } from '@ant-design/icons';

const Login: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);

  const onLogin = async (values: any) => {
    setLoading(true);
    try {
      const result = await window.electronAPI.pythonCall('/api/auth/login', {
        phone: values.phone,
        headless: values.headless || false
      });

      if (result.success) {
        message.success('登录成功！');
        setLoggedIn(true);
      } else {
        message.error(result.message || '登录失败');
      }
    } catch (error: any) {
      console.error('登录失败', error);
      message.error('登录失败: ' + (error.message || '未知错误'));
    } finally {
      setLoading(false);
    }
  };

  const onLogout = async () => {
    try {
      await window.electronAPI.pythonCall('/api/auth/logout', {});
      message.success('登出成功');
      setLoggedIn(false);
    } catch (error) {
      message.error('登出失败');
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: '50px auto' }}>
      <Card title="Boss直聘登录" bordered={false}>
        {!loggedIn ? (
          <>
            <Alert
              message="登录说明"
              description="请输入手机号，系统会打开浏览器窗口，请在浏览器中完成验证码验证。"
              type="info"
              showIcon
              style={{ marginBottom: 24 }}
            />

            <Form
              name="login"
              onFinish={onLogin}
              layout="vertical"
              initialValues={{ headless: false }}
            >
              <Form.Item
                label="手机号"
                name="phone"
                rules={[
                  { required: true, message: '请输入手机号' },
                  { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号' }
                ]}
              >
                <Input
                  prefix={<PhoneOutlined />}
                  placeholder="请输入手机号"
                  size="large"
                />
              </Form.Item>

              <Form.Item
                label="无头模式"
                name="headless"
                valuePropName="checked"
                tooltip="开启后浏览器将在后台运行（不推荐，可能被检测）"
              >
                <Switch />
              </Form.Item>

              <Form.Item>
                <Button
                  type="primary"
                  htmlType="submit"
                  icon={<LoginOutlined />}
                  loading={loading}
                  size="large"
                  block
                >
                  登录
                </Button>
              </Form.Item>
            </Form>
          </>
        ) : (
          <>
            <Alert
              message="已登录"
              description="您已成功登录 Boss直聘，可以开始搜索和投递岗位了。"
              type="success"
              showIcon
              style={{ marginBottom: 24 }}
            />

            <Button
              danger
              onClick={onLogout}
              size="large"
              block
            >
              登出
            </Button>
          </>
        )}
      </Card>
    </div>
  );
};

export default Login;
