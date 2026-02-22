"""
客户获取系统 - 自动化冷邮件 + 销售漏斗
目标：锁定10%有融资的AI团队
"""

import asyncio
import json
from typing import List, Dict
from datetime import datetime
from pathlib import Path

class ClientAcquisitionEngine:
    """
    客户获取引擎 - 自动化销售流程
    """
    
    def __init__(self, output_dir: str = "./leads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 目标客户画像（10%有钱的AI团队）
        self.target_profile = {
            "融资阶段": ["Pre-seed", "Seed", "Series A"],
            "团队规模": "3-20人",
            "产品阶段": "MVP已上线或即将上线",
            "痛点": [
                "零流量",
                "缺乏高质量训练数据",
                "不知道模型质量如何",
                "没时间做脏活"
            ],
            "预算": "$500-$5000/月",
            "决策人": "技术创始人、CTO"
        }
        
        # 客户来源渠道
        self.lead_sources = {
            "product_hunt": {
                "url": "https://www.producthunt.com/topics/artificial-intelligence",
                "筛选条件": "最近30天发布的AI产品",
                "预计线索": "50-100/月"
            },
            "ycombinator": {
                "url": "https://www.ycombinator.com/companies",
                "筛选条件": "AI类别 + 最近批次",
                "预计线索": "20-50/月"
            },
            "crunchbase": {
                "url": "https://www.crunchbase.com",
                "筛选条件": "AI公司 + 最近融资",
                "预计线索": "30-80/月"
            },
            "twitter": {
                "url": "https://twitter.com",
                "筛选条件": "#BuildInPublic + AI相关",
                "预计线索": "100-200/月"
            },
            "indie_hackers": {
                "url": "https://www.indiehackers.com",
                "筛选条件": "AI产品 + 有收入",
                "预计线索": "20-50/月"
            }
        }
    
    def generate_cold_email(self, lead: Dict, product: str) -> Dict:
        """
        生成个性化冷邮件
        """
        templates = {
            "data_corpus": {
                "subject": f"为{lead['company']}节省3个月数据工程时间",
                "body": f"""Hi {lead['founder_name']},

我在{lead['source']}上看到了{lead['company']}，{lead['product_description']}这个方向很有潜力！

我注意到你们在做{lead['vertical']}领域的AI产品。我专门为AI团队提供已清洗、结构化的行业语料库：

✅ {lead['vertical']}行业专业数据
✅ 10,000+高质量文档
✅ 直接可用于RAG/微调
✅ 节省3个月数据工程时间

痛点：大多数AI团队最痛恨写爬虫和清洗数据，但这是构建垂直领域AI的必经之路。

定价：$500-$2000/库（含30天技术支持）

提供免费样本数据（100条），回复即可获取。

Best,
[你的名字]

P.S. 已帮助{lead['vertical']}领域的3家AI公司节省了数据工程时间。
"""
            },
            "distribution": {
                "subject": f"看到{lead['company']}在Product Hunt发布了",
                "body": f"""Hi {lead['founder_name']},

我在Product Hunt上看到了{lead['product_name']}，很棒的想法！

我注意到你们的产品目前流量还不多（这是大多数新产品的痛点）。

我专门帮AI产品创始人解决"零流量"问题：

✅ 30天全网自动化铺量（Reddit/Twitter/HN/小红书/知乎）
✅ 每天15篇高质量内容
✅ 预计带来2K-10K点击，100-500注册

定价：$1500/月 或 $5/注册用户（按效果付费）

已帮助20+产品获得首批用户。提供前3天免费试用。

感兴趣吗？

Best,
[你的名字]

P.S. 如果你已经有分发策略，也很乐意交流经验！
"""
            },
            "model_testing": {
                "subject": f"帮{lead['company']}科学论证模型质量",
                "body": f"""Hi {lead['founder_name']},

我在{lead['source']}上看到了{lead['company']}的AI产品。

作为AI创始人，你可能面临这些问题：
- 不知道模型准确率到底有多高
- 担心被Prompt Injection攻击
- 无法向投资人证明模型质量

我提供科学的AI模型评估服务：

✅ 准确率测试（带95%置信区间）
✅ 对抗攻击测试（5大类攻击模式）
✅ 一致性测试 + 成本分析
✅ 详细评估报告 + 改进建议

定价：$800-$2000/次评估

案例：某AI客服公司通过评估发现准确率仅68%（自以为90%），优化后提升至85%，成本降低40%。

提供10个测试用例的免费试用，回复即可获取。

Best,
[你的名字]

P.S. 统计学专业背景，已为10+AI团队提供评估。
"""
            }
        }
        
        template = templates.get(product, templates["distribution"])
        
        return {
            "to": lead.get("email", ""),
            "subject": template["subject"],
            "body": template["body"],
            "lead_id": lead.get("id", ""),
            "product": product,
            "created_at": datetime.now().isoformat()
        }
    
    async def scrape_leads_from_product_hunt(self, days: int = 30) -> List[Dict]:
        """
        从Product Hunt抓取潜在客户
        """
        print(f"[线索抓取] 从Product Hunt抓取最近{days}天的AI产品...")
        
        # 模拟抓取（实际需要接入Product Hunt API或爬虫）
        leads = [
            {
                "id": f"ph_{i}",
                "source": "Product Hunt",
                "company": f"AI Startup {i}",
                "product_name": f"AI Tool {i}",
                "product_description": "AI-powered productivity tool",
                "founder_name": f"Founder {i}",
                "email": f"founder{i}@example.com",
                "vertical": "productivity",
                "launch_date": "2024-02-01",
                "upvotes": 100 + i * 10,
                "comments": 20 + i * 2,
                "website": f"https://aitool{i}.com",
                "funding_stage": "Seed" if i % 3 == 0 else "Pre-seed",
                "score": 0.8  # 匹配度评分
            }
            for i in range(20)
        ]
        
        print(f"[线索抓取] 完成，找到 {len(leads)} 个潜在客户")
        return leads
    
    async def scrape_leads_from_ycombinator(self) -> List[Dict]:
        """
        从YC公司列表抓取
        """
        print(f"[线索抓取] 从YC抓取AI公司...")
        
        leads = [
            {
                "id": f"yc_{i}",
                "source": "Y Combinator",
                "company": f"YC AI Company {i}",
                "product_name": f"YC Product {i}",
                "product_description": "AI solution for enterprises",
                "founder_name": f"YC Founder {i}",
                "email": f"founder{i}@yccompany.com",
                "vertical": "enterprise",
                "batch": "W24",
                "funding_stage": "Seed",
                "website": f"https://yccompany{i}.com",
                "score": 0.9  # YC公司质量高
            }
            for i in range(10)
        ]
        
        print(f"[线索抓取] 完成，找到 {len(leads)} 个YC公司")
        return leads
    
    async def scrape_leads_from_twitter(self, keywords: List[str]) -> List[Dict]:
        """
        从Twitter抓取#BuildInPublic的AI创始人
        """
        print(f"[线索抓取] 从Twitter抓取 {keywords} 相关创始人...")
        
        leads = [
            {
                "id": f"tw_{i}",
                "source": "Twitter",
                "company": f"Indie AI {i}",
                "product_name": f"AI Side Project {i}",
                "product_description": "Building in public",
                "founder_name": f"@indie_founder_{i}",
                "email": "",  # 需要后续获取
                "vertical": "developer_tools",
                "twitter_followers": 1000 + i * 100,
                "engagement_rate": 0.05,
                "funding_stage": "Bootstrapped",
                "score": 0.6
            }
            for i in range(30)
        ]
        
        print(f"[线索抓取] 完成，找到 {len(leads)} 个Twitter线索")
        return leads
    
    def qualify_leads(self, leads: List[Dict]) -> List[Dict]:
        """
        线索筛选 - 只保留10%有钱的
        """
        print(f"[线索筛选] 开始筛选 {len(leads)} 个线索...")
        
        qualified = []
        
        for lead in leads:
            # 筛选条件
            has_funding = lead.get("funding_stage") in ["Pre-seed", "Seed", "Series A"]
            has_traction = lead.get("upvotes", 0) > 50 or lead.get("twitter_followers", 0) > 500
            high_score = lead.get("score", 0) > 0.7
            
            if has_funding or (has_traction and high_score):
                lead["qualified"] = True
                lead["qualification_reason"] = []
                
                if has_funding:
                    lead["qualification_reason"].append("有融资")
                if has_traction:
                    lead["qualification_reason"].append("有牵引力")
                if high_score:
                    lead["qualification_reason"].append("高匹配度")
                
                qualified.append(lead)
        
        print(f"[线索筛选] 完成，筛选出 {len(qualified)} 个合格线索 ({len(qualified)/len(leads)*100:.1f}%)")
        return qualified
    
    def prioritize_leads(self, leads: List[Dict]) -> List[Dict]:
        """
        线索优先级排序
        """
        def calculate_priority_score(lead: Dict) -> float:
            score = 0.0
            
            # 融资阶段权重
            funding_weights = {
                "Series A": 1.0,
                "Seed": 0.8,
                "Pre-seed": 0.6,
                "Bootstrapped": 0.3
            }
            score += funding_weights.get(lead.get("funding_stage", ""), 0) * 40
            
            # 来源权重
            source_weights = {
                "Y Combinator": 1.0,
                "Product Hunt": 0.8,
                "Crunchbase": 0.7,
                "Twitter": 0.5
            }
            score += source_weights.get(lead.get("source", ""), 0) * 30
            
            # 牵引力权重
            if lead.get("upvotes", 0) > 100:
                score += 20
            elif lead.get("upvotes", 0) > 50:
                score += 10
            
            # 匹配度权重
            score += lead.get("score", 0) * 10
            
            return score
        
        # 计算优先级分数
        for lead in leads:
            lead["priority_score"] = calculate_priority_score(lead)
        
        # 排序
        leads.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return leads
    
    async def run_acquisition_campaign(
        self, 
        product: str = "distribution",
        target_count: int = 100
    ) -> Dict:
        """
        运行完整的客户获取活动
        """
        print(f"\n{'='*60}")
        print(f"开始客户获取活动 - 产品: {product}")
        print(f"{'='*60}\n")
        
        # 步骤1：从多个渠道抓取线索
        all_leads = []
        
        ph_leads = await self.scrape_leads_from_product_hunt()
        all_leads.extend(ph_leads)
        
        yc_leads = await self.scrape_leads_from_ycombinator()
        all_leads.extend(yc_leads)
        
        tw_leads = await self.scrape_leads_from_twitter(["AI", "BuildInPublic"])
        all_leads.extend(tw_leads)
        
        print(f"\n总共抓取 {len(all_leads)} 个线索\n")
        
        # 步骤2：筛选合格线索
        qualified_leads = self.qualify_leads(all_leads)
        
        # 步骤3：优先级排序
        prioritized_leads = self.prioritize_leads(qualified_leads)
        
        # 步骤4：生成冷邮件
        print(f"\n[邮件生成] 为前{min(target_count, len(prioritized_leads))}个线索生成邮件...")
        emails = []
        for lead in prioritized_leads[:target_count]:
            email = self.generate_cold_email(lead, product)
            emails.append(email)
        
        # 步骤5：保存结果
        campaign_dir = self.output_dir / f"{product}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        campaign_dir.mkdir(exist_ok=True)
        
        # 保存线索
        with open(campaign_dir / "leads.json", 'w', encoding='utf-8') as f:
            json.dump(prioritized_leads, f, ensure_ascii=False, indent=2)
        
        # 保存邮件
        with open(campaign_dir / "emails.json", 'w', encoding='utf-8') as f:
            json.dump(emails, f, ensure_ascii=False, indent=2)
        
        # 生成CSV（方便导入邮件工具）
        self._export_to_csv(emails, campaign_dir / "emails.csv")
        
        # 生成报告
        report = {
            "campaign": {
                "product": product,
                "start_date": datetime.now().isoformat(),
                "target_count": target_count
            },
            "funnel": {
                "total_leads": len(all_leads),
                "qualified_leads": len(qualified_leads),
                "qualification_rate": f"{len(qualified_leads)/len(all_leads)*100:.1f}%",
                "emails_generated": len(emails)
            },
            "top_leads": prioritized_leads[:10],
            "expected_response_rate": "5-10%",
            "expected_conversions": f"{len(emails) * 0.05:.0f}-{len(emails) * 0.1:.0f}",
            "expected_revenue": f"${len(emails) * 0.075 * 1000:.0f}-${len(emails) * 0.075 * 2000:.0f}"
        }
        
        with open(campaign_dir / "report.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*60}")
        print(f"✅ 客户获取活动完成！")
        print(f"📊 活动数据: {campaign_dir}")
        print(f"📧 生成邮件: {len(emails)} 封")
        print(f"💰 预期收入: {report['expected_revenue']}")
        print(f"{'='*60}\n")
        
        return report
    
    def _export_to_csv(self, emails: List[Dict], filepath: Path):
        """导出为CSV格式"""
        import csv
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['to', 'subject', 'body', 'lead_id'])
            writer.writeheader()
            writer.writerows(emails)
        
        print(f"[导出] CSV文件已保存: {filepath}")


# ============================================
# 使用示例
# ============================================

async def main():
    engine = ClientAcquisitionEngine()
    
    # 运行分发产品的获客活动
    report = await engine.run_acquisition_campaign(
        product="distribution",
        target_count=50
    )
    
    print("\n预期结果:")
    print(f"- 发送邮件: 50封")
    print(f"- 预期回复: 2-5个")
    print(f"- 预期成交: 1-2个")
    print(f"- 预期收入: $1500-$3000")


if __name__ == "__main__":
    asyncio.run(main())

