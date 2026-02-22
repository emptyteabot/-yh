"""
简单验证 - 检查系统是否可以运行
"""

print("="*70)
print("🧪 变现系统快速验证")
print("="*70)

# 测试1: 模块导入
print("\n【测试1】检查模块导入...")
try:
    from monetization_engines.data_corpus_engine import DataCorpusEngine
    from monetization_engines.distribution_engine import DistributionEngine
    from monetization_engines.model_testing_engine import ModelTestingEngine
    from monetization_engines.client_acquisition import ClientAcquisitionEngine
    print("✅ 所有模块导入成功")
except Exception as e:
    print(f"❌ 模块导入失败: {e}")
    exit(1)

# 测试2: 依赖检查
print("\n【测试2】检查关键依赖...")
try:
    import numpy
    import scipy
    print("✅ numpy 和 scipy 已安装")
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("请运行: pip install scipy numpy")
    exit(1)

# 测试3: 引擎初始化
print("\n【测试3】初始化引擎...")
try:
    data_engine = DataCorpusEngine()
    dist_engine = DistributionEngine()
    test_engine = ModelTestingEngine()
    acq_engine = ClientAcquisitionEngine()
    print("✅ 所有引擎初始化成功")
except Exception as e:
    print(f"❌ 引擎初始化失败: {e}")
    exit(1)

print("\n" + "="*70)
print("🎉 系统验证通过！")
print("="*70)
print("\n下一步：")
print("1. 运行 python monetization_hub.py 启动系统")
print("2. 或双击 启动变现系统.bat")
print("="*70)

