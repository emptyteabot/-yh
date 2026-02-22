
# SendGrid邮件发送脚本
import sendgrid
from sendgrid.helpers.mail import Mail
import json

# 配置
API_KEY = "YOUR_SENDGRID_API_KEY"  # 替换为你的API Key
FROM_EMAIL = "your-email@your-domain.com"  # 替换为你的邮箱
FROM_NAME = "Your Name"  # 替换为你的名字

def send_email(to_email, subject, content):
    sg = sendgrid.SendGridAPIClient(api_key=API_KEY)
    
    message = Mail(
        from_email=(FROM_EMAIL, FROM_NAME),
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    
    try:
        response = sg.send(message)
        print(f"✅ 邮件已发送到 {to_email}")
        return True
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        return False

# 批量发送
def send_batch_emails(emails_file):
    with open(emails_file, 'r', encoding='utf-8') as f:
        emails = json.load(f)
    
    for email in emails:
        send_email(
            to_email=email['to'],
            subject=email['subject'],
            content=email['body']
        )
        # 延迟避免被限制
        import time
        time.sleep(2)

# 使用
send_batch_emails('auto_execution_output/待发送邮件.json')
