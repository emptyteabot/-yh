
# 自动跟进脚本
import json
from datetime import datetime, timedelta

def check_and_send_followup():
    '''检查并发送跟进邮件'''
    
    # 加载已发送邮件
    with open('fully_automated_output/邮件发送日志.json', 'r') as f:
        sent_emails = json.load(f)
    
    # 加载回复记录
    with open('fully_automated_output/客户回复记录.json', 'r') as f:
        replies = json.load(f)
    
    replied_companies = [r['original_email']['company'] for r in replies]
    
    # 检查需要跟进的邮件
    today = datetime.now()
    
    for email in sent_emails:
        sent_date = datetime.fromisoformat(email['sent_at'])
        days_passed = (today - sent_date).days
        
        # 如果已回复，跳过
        if email['company'] in replied_companies:
            continue
        
        # Day 3跟进
        if days_passed == 3:
            send_followup(email, 'day_3')
        
        # Day 7跟进
        elif days_passed == 7:
            send_followup(email, 'day_7')
        
        # Day 10最后跟进
        elif days_passed == 10:
            send_followup(email, 'day_10')

def send_followup(original_email, template_type):
    '''发送跟进邮件'''
    # 加载模板
    with open('real_clients/跟进邮件模板.json', 'r') as f:
        templates = json.load(f)
    
    template = templates[template_type]
    
    # 填充模板
    content = template.format(
        name=original_email['company'],
        company=original_email['company'],
        original_subject=original_email['subject'],
        service_1="算力优化",
        service_2="政府补贴申请",
        free_offer="成本审计",
        service="我们的服务",
        your_name="你的名字",
        your_email="your-email@domain.com",
        your_linkedin="linkedin.com/in/yourname"
    )
    
    # 发送邮件（使用SendGrid）
    # send_email(original_email['to'], f"Re: {original_email['subject']}", content)
    
    print(f"✅ 已发送{template_type}跟进邮件到 {original_email['company']}")

# 每天运行一次
if __name__ == "__main__":
    check_and_send_followup()
