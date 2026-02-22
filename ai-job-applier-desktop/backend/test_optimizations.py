"""
测试优化功能
"""

import asyncio
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def test_retry_manager():
    """测试重试机制"""
    print("\n" + "=" * 50)
    print("测试 1: 智能重试机制")
    print("=" * 50)

    from automation.retry_manager import retry_on_error, RetryableError

    attempt_count = 0

    @retry_on_error(max_retries=3, base_delay=1.0)
    async def flaky_function():
        nonlocal attempt_count
        attempt_count += 1
        print(f"尝试 #{attempt_count}")

        if attempt_count < 3:
            raise RetryableError("模拟失败")

        return "成功"

    try:
        result = await flaky_function()
        print(f"✅ 结果: {result}")
        print(f"✅ 总共尝试了 {attempt_count} 次")
    except Exception as e:
        print(f"❌ 失败: {e}")


async def test_rate_limiter():
    """测试限流器"""
    print("\n" + "=" * 50)
    print("测试 2: 智能限流器")
    print("=" * 50)

    from automation.rate_limiter import SmartThrottler
    import time

    throttler = SmartThrottler(
        per_minute=5,
        per_hour=20,
        per_day=50,
        adaptive=True
    )

    print("开始投递测试...")
    start_time = time.time()

    for i in range(10):
        if await throttler.acquire():
            print(f"✅ 投递 #{i+1}")

            # 模拟投递结果
            import random
            success = random.random() > 0.3
            throttler.record_result(success)

            # 显示统计
            stats = throttler.get_stats()
            print(f"   统计: 今日剩余 {stats['remaining_today']}, 当前速率 {stats['current_rate']}/分钟")
        else:
            print(f"❌ 投递 #{i+1} 被限流")

    elapsed = time.time() - start_time
    print(f"\n✅ 完成! 耗时 {elapsed:.1f} 秒")


async def test_job_filter():
    """测试去重器"""
    print("\n" + "=" * 50)
    print("测试 3: 投递去重器")
    print("=" * 50)

    from automation.job_filter import JobFilter

    job_filter = JobFilter()

    # 添加黑名单
    job_filter.blacklist_manager.add_company("测试外包公司", "外包")
    job_filter.blacklist_manager.add_keyword("996", "工作制度")

    # 测试岗位
    test_jobs = [
        {'job_id': '1', 'company': 'A公司', 'job_title': 'Python开发', 'description': '弹性工作'},
        {'job_id': '2', 'company': '测试外包公司', 'job_title': 'Java开发', 'description': ''},
        {'job_id': '3', 'company': 'B公司', 'job_title': 'Go开发', 'description': '996工作制'},
        {'job_id': '1', 'company': 'A公司', 'job_title': 'Python开发', 'description': '弹性工作'},  # 重复
        {'job_id': '4', 'company': 'C公司', 'job_title': 'Rust开发', 'description': '双休'},
    ]

    print(f"原始岗位数: {len(test_jobs)}")

    # 过滤
    filtered = job_filter.filter_jobs(test_jobs)
    print(f"过滤后岗位数: {len(filtered)}")

    # 标记投递
    for job in filtered:
        job_filter.mark_applied(job)
        print(f"✅ 已标记: {job['company']} - {job['job_title']}")

    # 再次过滤（应该全部被过滤）
    filtered_again = job_filter.filter_jobs(test_jobs)
    print(f"\n再次过滤后: {len(filtered_again)} 个岗位（应该为0）")

    # 统计
    stats = job_filter.get_stats()
    print(f"\n统计信息:")
    print(f"  总投递数: {stats['total_applied']}")
    print(f"  今日投递: {stats['applied_today']}")
    print(f"  投递公司数: {stats['applied_companies']}")
    print(f"  黑名单公司: {stats['blacklisted_companies']}")
    print(f"  黑名单关键词: {stats['blacklisted_keywords']}")


async def test_human_simulator():
    """测试人类行为模拟"""
    print("\n" + "=" * 50)
    print("测试 4: 人类行为模拟")
    print("=" * 50)

    from automation.human_simulator import HumanBehaviorSimulator

    # 测试贝塞尔曲线
    path = HumanBehaviorSimulator.bezier_curve(
        start=(100, 100),
        end=(500, 500),
        control_points=2
    )

    print(f"✅ 生成贝塞尔曲线路径: {len(path)} 个点")
    print(f"   起点: {path[0]}")
    print(f"   终点: {path[-1]}")
    print(f"   中间点示例: {path[len(path)//2]}")


async def test_checkpoint():
    """测试断点续传"""
    print("\n" + "=" * 50)
    print("测试 5: 断点续传")
    print("=" * 50)

    from automation.retry_manager import CheckpointManager

    manager = CheckpointManager()

    # 保存断点
    manager.save_checkpoint("test_task", {
        'current_index': 5,
        'total': 10,
        'results': {'success': 3, 'failed': 2}
    })
    print("✅ 断点已保存")

    # 加载断点
    state = manager.load_checkpoint("test_task")
    print(f"✅ 断点已加载: {state}")

    # 列出所有断点
    checkpoints = manager.list_checkpoints()
    print(f"✅ 所有断点: {checkpoints}")

    # 删除断点
    manager.delete_checkpoint("test_task")
    print("✅ 断点已删除")


async def main():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("🚀 开始测试优化功能")
    print("=" * 50)

    try:
        await test_retry_manager()
        await test_rate_limiter()
        await test_job_filter()
        await test_human_simulator()
        await test_checkpoint()

        print("\n" + "=" * 50)
        print("✅ 所有测试完成！")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
