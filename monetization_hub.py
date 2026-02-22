"""
卖铲子变现系统 - 统一启动入口
三大高价值产品 + 自动化客户获取
"""

import asyncio
from monetization_engines.data_corpus_engine import DataCorpusEngine
from monetization_engines.distribution_engine import DistributionEngine
from monetization_engines.model_testing_engine import ModelTestingEngine
from monetization_engines.client_acquisition import ClientAcquisitionEngine

class MonetizationHub:
    """
    变现中枢 - 统一管理三大铲子产品
    """
    
    def __init__(self):
        self.data_engine = DataCorpusEngine()
        self.distribution_engine = DistributionEngine()
        self.testing_engine = ModelTestingEngine()
        self.acquisition_engine = ClientAcquisitionEngine()
        
        self.products = {
            "1": {
                "name": "数据语料库",
                "engine": self.data_engine,
                "price": "$500-$2000/库",
                "target": "开发RAG/微调的AI团队",
                "margin": "90%（几乎零成本）"
            },
            "2": {
                "name": "自动化分发",
                "engine": self.distribution_engine,
                "price": "$1500/月 或 $5/用户",
                "target": "零流量的AI产品创始人",
                "margin": "80%（自动化执行）"
            },
            "3": {
                "name": "模型评测",
                "engine": self.testing_engine,
                "price": "$800-$2000/次",
                "target": "需要论证质量的AI团队",
                "margin": "95%（统计学护城河）"
            }
        }
    
    def show_menu(self):
        """显示主菜单"""
        print("\n" + "="*70)
        print("🚀 卖铲子变现系统 - 在淘金热中赚真金白银")
        print("="*70)
        print("\n【三大高价值产品】")
        
        for key, product in self.products.items():
            print(f"\n{key}. {product['name']}")
            print(f"   定价: {product['price']}")
            print(f"   目标: {product['target']}")
            print(f"   毛利: {product['margin']}")
        
        print("\n【客户获取】")
        print("4. 运行客户获取活动（自动化冷邮件）")
        
        print("\n【演示模式】")
        print("5. 完整演示（生成样品 + 获客）")
        
        print("\n【退出】")
        print("0. 退出系统")
        
        print("\n" + "="*70)
    
    async def demo_data_corpus(self):
        """演示数据语料库生成"""
        print("\n【演示：数据语料库生成】")
        print("场景：为医疗AI团队生成FDA合规数据库\n")
        
        # 生成产品
        product_path = await self.data_engine.generate_full_product(
            industry="medical_compliance",
            max_docs=100  # 演示用少量数据
        )
        
        # 显示销售话术
        print("\n【销售话术】")
        print(self.data_engine.get_sales_pitch("medical_compliance"))
        
        return product_path
    
    async def demo_distribution(self):
        """演示自动化分发"""
        print("\n【演示：自动化分发引擎】")
        print("场景：为AI简历生成器做30天全网铺量\n")
        
        product_info = {
            "name": "AI Resume Builder",
            "category": "ai_tools",
            "pain_point": "写简历太费时间",
            "value_prop": "3分钟生成专业简历",
            "differentiation": "AI优化，通过率提升50%",
            "social_proof": "500+用户，4.8分好评"
        }
        
        # 执行分发活动
        report = await self.distribution_engine.execute_campaign(
            product_info, 
            duration_days=30
        )
        
        # 显示客户提案
        print("\n【客户提案】")
        print(self.distribution_engine.generate_client_proposal(product_info))
        
        return report
    
    async def demo_model_testing(self):
        """演示模型评测"""
        print("\n【演示：模型评测系统】")
        print("场景：为AI客服产品做全面质量评估\n")
        
        # 模拟模型API
        async def mock_api(prompt: str) -> str:
            await asyncio.sleep(0.05)
            if "what is" in prompt.lower():
                return "This is a test response."
            elif "ignore" in prompt.lower():
                return "I cannot do that."
            return f"Response to: {prompt[:30]}"
        
        # 准备测试套件
        test_suite = {
            "model_name": "CustomerServiceAI-v1",
            "accuracy_cases": [
                {
                    "prompt": "What is your return policy?",
                    "expected_output": "return policy",
                    "evaluation_method": "contains"
                }
            ] * 20,  # 20个测试用例
            "base_prompts": [
                "Tell me about your service",
                "How can I contact support?"
            ],
            "consistency_prompts": [
                "What are your hours?",
                "Do you offer refunds?"
            ]
        }
        
        # 运行评估
        report_path = await self.testing_engine.run_comprehensive_evaluation(
            mock_api,
            test_suite
        )
        
        # 显示销售提案
        print("\n【销售提案】")
        print(self.testing_engine.get_sales_proposal())
        
        return report_path
    
    async def demo_client_acquisition(self, product: str = "distribution"):
        """演示客户获取"""
        print("\n【演示：客户获取系统】")
        print(f"场景：为'{product}'产品获取50个潜在客户\n")
        
        report = await self.acquisition_engine.run_acquisition_campaign(
            product=product,
            target_count=50
        )
        
        print("\n【获客漏斗】")
        print(f"总线索: {report['funnel']['total_leads']}")
        print(f"合格线索: {report['funnel']['qualified_leads']}")
        print(f"筛选率: {report['funnel']['qualification_rate']}")
        print(f"生成邮件: {report['funnel']['emails_generated']}")
        print(f"预期回复: {report['expected_response_rate']}")
        print(f"预期成交: {report['expected_conversions']}")
        print(f"预期收入: {report['expected_revenue']}")
        
        return report
    
    async def run_full_demo(self):
        """完整演示流程"""
        print("\n" + "="*70)
        print("🎬 完整演示：从产品生成到客户获取")
        print("="*70)
        
        # 1. 生成三个产品样品
        print("\n【第1步】生成产品样品...")
        
        print("\n→ 生成数据语料库样品")
        await self.demo_data_corpus()
        
        print("\n→ 生成分发方案样品")
        await self.demo_distribution()
        
        print("\n→ 生成评测报告样品")
        await self.demo_model_testing()
        
        # 2. 运行客户获取
        print("\n【第2步】运行客户获取活动...")
        
        for product_key in ["data_corpus", "distribution", "model_testing"]:
            print(f"\n→ 为 {product_key} 获取客户")
            await self.demo_client_acquisition(product_key)
        
        # 3. 总结
        print("\n" + "="*70)
        print("✅ 完整演示完成！")
        print("="*70)
        print("\n【下一步行动】")
        print("1. 完善产品样品（提高质量）")
        print("2. 接入真实API（Product Hunt、Twitter等）")
        print("3. 发送冷邮件（每天50封）")
        print("4. 跟进回复（转化为付费客户）")
        print("\n【预期结果（30天）】")
        print("- 发送邮件: 1500封")
        print("- 预期回复: 75-150个")
        print("- 预期成交: 10-20个")
        print("- 预期收入: $10K-$30K")
        print("\n【关键成功因素】")
        print("✅ 只锁定10%有融资的AI团队（避免白嫖党）")
        print("✅ 高价值产品（$500+）+ 高毛利（80%+）")
        print("✅ 自动化执行（降低交付成本）")
        print("✅ 统计学护城河（竞争对手抄不走）")
        print("="*70 + "\n")
    
    async def run(self):
        """运行主程序"""
        while True:
            self.show_menu()
            
            choice = input("请选择操作 (0-5): ").strip()
            
            if choice == "0":
                print("\n👋 退出系统")
                break
            elif choice == "1":
                await self.demo_data_corpus()
            elif choice == "2":
                await self.demo_distribution()
            elif choice == "3":
                await self.demo_model_testing()
            elif choice == "4":
                product = input("选择产品 (data_corpus/distribution/model_testing): ").strip()
                await self.demo_client_acquisition(product)
            elif choice == "5":
                await self.run_full_demo()
            else:
                print("\n❌ 无效选择，请重试")
            
            input("\n按回车键继续...")


async def main():
    """主入口"""
    hub = MonetizationHub()
    
    # 显示欢迎信息
    print("\n" + "="*70)
    print("💰 卖铲子变现系统")
    print("="*70)
    print("\n【核心理念】")
    print("在AI淘金热中，卖铲子比淘金更赚钱")
    print("\n【目标客户】")
    print("10%拿到融资或有现金流的B端AI团队")
    print("（绝对避开90%零收入的独立开发者）")
    print("\n【三大铲子】")
    print("1. 数据语料库 - 解决脏活痛点")
    print("2. 自动化分发 - 解决零流量痛点")
    print("3. 模型评测 - 解决质量论证痛点")
    print("\n【商业模式】")
    print("高价值产品 ($500-$2000) + 高毛利 (80%+) + 自动化交付")
    print("\n【目标】")
    print("30天内获得第一个付费客户")
    print("90天内达到 $10K MRR")
    print("="*70)
    
    # 运行主程序
    await hub.run()


if __name__ == "__main__":
    asyncio.run(main())

