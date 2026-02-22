"""
测试多Agent系统 - 快速演示
"""

import asyncio
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from multi_agent_system import OrchestratorAgent

async def quick_demo():
    """快速演示"""
    print("\n" + "="*70)
    print("🚀 多Agent协作系统 - 快速演示")
    print("="*70)
    
    orchestrator = OrchestratorAgent()
    
    print("\n✅ 系统初始化完成")
    print(f"✅ 激活了 {len(orchestrator.agents)} 个专业Agent")
    
    print("\n" + "="*70)
    print("📋 Agent列表")
    print("="*70)
    
    for name, agent in orchestrator.agents.items():
        print(f"\n🤖 {agent.name}")
        print(f"   角色: {agent.role}")
        print(f"   技能: {', '.join(agent.skills)}")
    
    print("\n" + "="*70)
    print("🎯 开始执行30天计划...")
    print("="*70)
    
    # 执行完整计划
    await orchestrator.execute_30day_plan()
    
    print("\n" + "="*70)
    print("✅ 演示完成！")
    print("="*70)
    print(f"\n📁 查看结果: multi_agent_output 文件夹")
    print("\n生成的文件:")
    print("  - week1_companies.json (30个客户)")
    print("  - week2_sent_emails.json (30封邮件)")
    print("  - week3_replies.json (回复记录)")
    print("  - week4_proposals.json (提案)")
    print("  - execution_report.json (执行报告)")
    
    print("\n" + "="*70)
    print("💰 预期收入: $100K-$300K")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(quick_demo())

