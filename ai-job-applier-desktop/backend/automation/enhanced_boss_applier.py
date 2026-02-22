"""
增强版 Boss直聘自动投递器
集成所有优化功能
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from .boss_applier import BossApplier
from .retry_manager import RetryManager, RetryConfig, retry_on_error, CheckpointManager
from .rate_limiter import SmartThrottler
from .job_filter import JobFilter
from .human_simulator import HumanBehaviorSimulator, AntiDetectionEnhancer

logger = logging.getLogger(__name__)


class EnhancedBossApplier(BossApplier):
    """增强版 Boss直聘投递器"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

        # 初始化增强功能
        self.retry_manager = RetryManager(RetryConfig(
            max_retries=3,
            base_delay=2.0,
            exponential_base=2.0
        ))

        self.throttler = SmartThrottler(
            per_minute=config.get('per_minute', 5),
            per_hour=config.get('per_hour', 50),
            per_day=config.get('per_day', 200),
            adaptive=True
        )

        self.job_filter = JobFilter()
        self.checkpoint_manager = CheckpointManager()

        # 人类行为模拟器（初始化后设置）
        self.human_simulator: Optional[HumanBehaviorSimulator] = None
        self.anti_detection: Optional[AntiDetectionEnhancer] = None

    async def _init_browser(self):
        """初始化浏览器（增强版）"""
        success = await super()._init_browser()

        if success and self.page:
            # 初始化人类行为模拟器
            self.human_simulator = HumanBehaviorSimulator(self.page)
            self.anti_detection = AntiDetectionEnhancer(self.page)

            # 注入高级反检测脚本
            await self.anti_detection.inject_advanced_scripts()
            await self.anti_detection.randomize_viewport()

            logger.info("增强功能已启用")

        return success

    @retry_on_error(max_retries=3, base_delay=2.0)
    async def search_jobs_enhanced(
        self,
        keywords: str,
        location: str = "全国",
        **filters
    ) -> List[Dict]:
        """搜索岗位（增强版，带重试）"""
        logger.info(f"搜索岗位: {keywords} @ {location}")

        try:
            # 调用原始搜索方法
            jobs = await self._async_search_jobs(keywords, location, **filters)

            # 过滤岗位（去重 + 黑名单）
            filtered_jobs = self.job_filter.filter_jobs(jobs)

            logger.info(f"搜索完成: 找到 {len(jobs)} 个岗位，过滤后 {len(filtered_jobs)} 个")

            return filtered_jobs

        except Exception as e:
            logger.error(f"搜索失败: {e}")
            raise

    async def batch_apply_enhanced(
        self,
        jobs: List[Dict],
        resume_text: str,
        generate_cover_letter: callable = None
    ) -> Dict[str, Any]:
        """批量投递（增强版）"""
        logger.info(f"开始批量投递: {len(jobs)} 个岗位")

        # 检查是否有断点
        checkpoint = self.checkpoint_manager.load_checkpoint("batch_apply")
        start_index = checkpoint.get('current_index', 0) if checkpoint else 0

        if start_index > 0:
            logger.info(f"从断点继续: 第 {start_index + 1} 个岗位")

        results = {
            'total': len(jobs),
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'details': []
        }

        for i in range(start_index, len(jobs)):
            job = jobs[i]

            try:
                # 检查限流
                if not await self.throttler.acquire():
                    logger.warning("达到投递限额，停止投递")
                    results['skipped'] = len(jobs) - i
                    break

                # 模拟阅读岗位详情
                if self.human_simulator:
                    await self.human_simulator.simulate_reading(duration=3)

                # 生成求职信
                cover_letter = ""
                if generate_cover_letter:
                    cover_letter = await generate_cover_letter(job, resume_text)

                # 模拟犹豫
                if self.human_simulator:
                    await self.human_simulator.simulate_hesitation()

                # 投递
                success = await self._apply_single_job_with_retry(job, cover_letter)

                # 记录结果
                self.throttler.record_result(success)

                if success:
                    results['success'] += 1
                    self.job_filter.mark_applied(job)
                    logger.info(f"✅ 投递成功: {job.get('company')} - {job.get('job_title')}")
                else:
                    results['failed'] += 1
                    logger.warning(f"❌ 投递失败: {job.get('company')} - {job.get('job_title')}")

                results['details'].append({
                    'job': job,
                    'success': success,
                    'timestamp': datetime.now().isoformat()
                })

                # 保存断点
                self.checkpoint_manager.save_checkpoint("batch_apply", {
                    'current_index': i + 1,
                    'results': results
                })

                # 随机延迟
                await self._random_delay(3, 6)

            except Exception as e:
                logger.error(f"投递出错: {e}")
                results['failed'] += 1
                results['details'].append({
                    'job': job,
                    'success': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })

        # 完成后删除断点
        self.checkpoint_manager.delete_checkpoint("batch_apply")

        # 统计信息
        logger.info("=" * 50)
        logger.info(f"投递完成!")
        logger.info(f"总数: {results['total']}")
        logger.info(f"成功: {results['success']}")
        logger.info(f"失败: {results['failed']}")
        logger.info(f"跳过: {results['skipped']}")
        logger.info(f"成功率: {results['success'] / results['total'] * 100:.1f}%")
        logger.info("=" * 50)

        # 限流统计
        throttle_stats = self.throttler.get_stats()
        logger.info(f"今日剩余配额: {throttle_stats['remaining_today']}")
        logger.info(f"当前速率: {throttle_stats['current_rate']}/分钟")

        return results

    async def _apply_single_job_with_retry(
        self,
        job: Dict,
        cover_letter: str
    ) -> bool:
        """投递单个岗位（带重试）"""
        task_id = f"apply_{job.get('job_id')}"

        try:
            result = await self.retry_manager.execute_with_retry(
                self._async_apply_job,
                job,
                cover_letter,
                task_id=task_id
            )
            return result

        except Exception as e:
            logger.error(f"投递失败（重试后）: {e}")
            return False

    async def _async_apply_job(self, job: Dict, cover_letter: str) -> bool:
        """异步投递单个岗位"""
        try:
            # 访问岗位详情页
            job_url = job.get('job_url')
            if not job_url:
                raise Exception("岗位 URL 为空")

            await self.page.goto(job_url, wait_until='networkidle')
            await self._random_delay(1, 2)

            # 模拟阅读
            if self.human_simulator:
                await self.human_simulator.simulate_reading(duration=2)

            # 查找"立即沟通"按钮
            apply_button = await self.page.wait_for_selector(
                'button:has-text("立即沟通"), a:has-text("立即沟通")',
                timeout=5000
            )

            if not apply_button:
                raise Exception("未找到投递按钮")

            # 人类般的点击
            if self.human_simulator:
                box = await apply_button.bounding_box()
                if box:
                    await self.human_simulator.click_human_like(
                        box['x'] + box['width'] / 2,
                        box['y'] + box['height'] / 2
                    )
            else:
                await apply_button.click()

            await self._random_delay(1, 2)

            # 如果有求职信输入框，填写求职信
            if cover_letter:
                try:
                    cover_letter_input = await self.page.wait_for_selector(
                        'textarea[placeholder*="打招呼"]',
                        timeout=3000
                    )

                    if cover_letter_input and self.human_simulator:
                        await self.human_simulator.type_human_like(
                            'textarea[placeholder*="打招呼"]',
                            cover_letter
                        )
                        await self._random_delay(0.5, 1)
                except:
                    logger.debug("未找到求职信输入框")

            # 确认投递
            try:
                confirm_button = await self.page.wait_for_selector(
                    'button:has-text("发送"), button:has-text("确认")',
                    timeout=3000
                )

                if confirm_button:
                    await confirm_button.click()
                    await self._random_delay(1, 2)
            except:
                logger.debug("未找到确认按钮，可能已直接投递")

            # 检查是否投递成功
            success = await self._check_apply_success()

            return success

        except Exception as e:
            logger.error(f"投递过程出错: {e}")
            raise

    async def _check_apply_success(self) -> bool:
        """检查投递是否成功"""
        try:
            # 检查成功提示
            success_indicators = [
                'text=已发送',
                'text=发送成功',
                'text=投递成功',
                '.success-toast'
            ]

            for indicator in success_indicators:
                try:
                    element = await self.page.wait_for_selector(indicator, timeout=2000)
                    if element:
                        return True
                except:
                    continue

            # 检查失败提示
            failure_indicators = [
                'text=今日沟通人数已达上限',
                'text=该职位已关闭',
                'text=已投递过',
                '.error-toast'
            ]

            for indicator in failure_indicators:
                try:
                    element = await self.page.wait_for_selector(indicator, timeout=1000)
                    if element:
                        text = await element.inner_text()
                        logger.warning(f"投递失败: {text}")
                        return False
                except:
                    continue

            # 默认认为成功
            return True

        except Exception as e:
            logger.error(f"检查投递结果失败: {e}")
            return False

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'throttle': self.throttler.get_stats(),
            'filter': self.job_filter.get_stats(),
            'retry_history': len(self.retry_manager.retry_history),
            'checkpoints': self.checkpoint_manager.list_checkpoints()
        }


# 使用示例
async def example_usage():
    """使用示例"""
    config = {
        'headless': False,
        'per_minute': 5,
        'per_hour': 50,
        'per_day': 200
    }

    applier = EnhancedBossApplier(config)

    try:
        # 登录
        success = await applier._async_login("13800138000")
        if not success:
            logger.error("登录失败")
            return

        # 搜索岗位
        jobs = await applier.search_jobs_enhanced(
            keywords="Python开发",
            location="北京"
        )

        # 批量投递
        results = await applier.batch_apply_enhanced(
            jobs=jobs[:10],  # 只投递前10个
            resume_text="我的简历内容..."
        )

        # 查看统计
        stats = applier.get_stats()
        print(f"统计信息: {stats}")

    finally:
        await applier.close()


if __name__ == "__main__":
    asyncio.run(example_usage())
