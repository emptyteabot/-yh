"""
智能限流器
防止投递过快被封号
"""

import asyncio
import time
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import deque

logger = logging.getLogger(__name__)


class RateLimiter:
    """速率限制器（令牌桶算法）"""

    def __init__(
        self,
        rate: int = 10,  # 每分钟最多投递数
        burst: int = 3,   # 突发容量
        window: int = 60  # 时间窗口（秒）
    ):
        self.rate = rate
        self.burst = burst
        self.window = window
        self.tokens = burst
        self.last_update = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1) -> bool:
        """获取令牌"""
        async with self.lock:
            now = time.time()

            # 补充令牌
            elapsed = now - self.last_update
            self.tokens = min(
                self.burst,
                self.tokens + elapsed * (self.rate / self.window)
            )
            self.last_update = now

            # 检查是否有足够的令牌
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True

            # 计算需要等待的时间
            wait_time = (tokens - self.tokens) / (self.rate / self.window)
            logger.info(f"限流中，等待 {wait_time:.2f} 秒...")
            await asyncio.sleep(wait_time)

            self.tokens = 0
            self.last_update = time.time()
            return True


class AdaptiveRateLimiter:
    """自适应限流器（根据成功率动态调整）"""

    def __init__(
        self,
        initial_rate: int = 10,
        min_rate: int = 3,
        max_rate: int = 20,
        window: int = 60
    ):
        self.current_rate = initial_rate
        self.min_rate = min_rate
        self.max_rate = max_rate
        self.window = window

        self.limiter = RateLimiter(rate=initial_rate, window=window)

        # 统计信息
        self.success_count = 0
        self.failure_count = 0
        self.total_count = 0

        # 调整阈值
        self.success_threshold = 0.8  # 成功率 > 80% 时加速
        self.failure_threshold = 0.5  # 成功率 < 50% 时减速

    async def acquire(self) -> bool:
        """获取令牌"""
        return await self.limiter.acquire()

    def record_success(self):
        """记录成功"""
        self.success_count += 1
        self.total_count += 1
        self._adjust_rate()

    def record_failure(self):
        """记录失败"""
        self.failure_count += 1
        self.total_count += 1
        self._adjust_rate()

    def _adjust_rate(self):
        """动态调整速率"""
        if self.total_count < 10:
            return  # 样本太少，不调整

        success_rate = self.success_count / self.total_count

        # 成功率高 - 加速
        if success_rate > self.success_threshold:
            new_rate = min(self.current_rate + 2, self.max_rate)
            if new_rate != self.current_rate:
                logger.info(f"成功率 {success_rate:.2%}，加速至 {new_rate}/分钟")
                self.current_rate = new_rate
                self.limiter = RateLimiter(rate=new_rate, window=self.window)

        # 成功率低 - 减速
        elif success_rate < self.failure_threshold:
            new_rate = max(self.current_rate - 2, self.min_rate)
            if new_rate != self.current_rate:
                logger.warning(f"成功率 {success_rate:.2%}，减速至 {new_rate}/分钟")
                self.current_rate = new_rate
                self.limiter = RateLimiter(rate=new_rate, window=self.window)

        # 定期重置统计
        if self.total_count >= 50:
            self.success_count = 0
            self.failure_count = 0
            self.total_count = 0


class TimeWindowLimiter:
    """时间窗口限流器（滑动窗口）"""

    def __init__(
        self,
        max_requests: int = 50,  # 每天最多投递数
        window_hours: int = 24
    ):
        self.max_requests = max_requests
        self.window_seconds = window_hours * 3600
        self.requests: deque = deque()
        self.lock = asyncio.Lock()

    async def acquire(self) -> bool:
        """获取许可"""
        async with self.lock:
            now = time.time()

            # 清理过期请求
            while self.requests and now - self.requests[0] > self.window_seconds:
                self.requests.popleft()

            # 检查是否超限
            if len(self.requests) >= self.max_requests:
                oldest = self.requests[0]
                wait_time = self.window_seconds - (now - oldest)
                logger.warning(f"已达到每日限额 {self.max_requests}，等待 {wait_time/3600:.1f} 小时")
                return False

            # 记录请求
            self.requests.append(now)
            return True

    def get_remaining(self) -> int:
        """获取剩余配额"""
        now = time.time()
        # 清理过期请求
        while self.requests and now - self.requests[0] > self.window_seconds:
            self.requests.popleft()
        return self.max_requests - len(self.requests)


class SmartThrottler:
    """智能节流器（综合多种策略）"""

    def __init__(
        self,
        per_minute: int = 10,
        per_hour: int = 100,
        per_day: int = 500,
        adaptive: bool = True
    ):
        # 多级限流
        self.minute_limiter = RateLimiter(rate=per_minute, window=60)
        self.hour_limiter = TimeWindowLimiter(max_requests=per_hour, window_hours=1)
        self.day_limiter = TimeWindowLimiter(max_requests=per_day, window_hours=24)

        # 自适应限流
        if adaptive:
            self.adaptive_limiter = AdaptiveRateLimiter(initial_rate=per_minute)
        else:
            self.adaptive_limiter = None

    async def acquire(self) -> bool:
        """获取许可（需要通过所有限流器）"""
        # 检查每日限额
        if not await self.day_limiter.acquire():
            logger.error("已达到每日投递限额")
            return False

        # 检查每小时限额
        if not await self.hour_limiter.acquire():
            logger.warning("已达到每小时投递限额")
            return False

        # 速率限制
        if self.adaptive_limiter:
            await self.adaptive_limiter.acquire()
        else:
            await self.minute_limiter.acquire()

        return True

    def record_result(self, success: bool):
        """记录投递结果"""
        if self.adaptive_limiter:
            if success:
                self.adaptive_limiter.record_success()
            else:
                self.adaptive_limiter.record_failure()

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'remaining_today': self.day_limiter.get_remaining(),
            'remaining_hour': self.hour_limiter.get_remaining(),
            'current_rate': self.adaptive_limiter.current_rate if self.adaptive_limiter else None
        }


# 使用示例
if __name__ == "__main__":
    async def test_throttler():
        """测试限流器"""
        throttler = SmartThrottler(
            per_minute=5,
            per_hour=20,
            per_day=50
        )

        for i in range(10):
            if await throttler.acquire():
                print(f"投递 #{i+1}")
                # 模拟投递
                import random
                success = random.random() > 0.3
                throttler.record_result(success)
                print(f"结果: {'成功' if success else '失败'}")
                print(f"统计: {throttler.get_stats()}")
            else:
                print(f"投递 #{i+1} 被限流")

    asyncio.run(test_throttler())
