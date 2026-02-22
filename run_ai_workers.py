import asyncio
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入自动化引擎
from auto_execution_engine import AutoExecutionEngine

async def main():
    print("\n" + "="*70)
    print("🤖 AI员工自动化执行系统")
    print("="*70)
    print("\n让AI员工自动完成所有工作...")
    print("\n按 Ctrl+C 可以随时停止\n")
    
    engine = AutoExecutionEngine()
    await engine.run_full_automation()
    
    print("\n" + "="*70)
    print("✅ 完成！查看 auto_execution_output 文件夹")
    print("="*70)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

