"""
智能重试机制
支持指数退避、错误分类、断点续传
"""

import asyncio
import logging
from typing import Callable, Any, Optional, Dict
from functools import wraps
from datetime import datetime
import json
import os

logger = logging.getLogger(__name__)


class RetryConfig:
    """重试配置"""
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter


class RetryableError(Exception):
    """可重试的错误"""
    pass


class NonRetryableError(Exception):
    """不可重试的错误"""
    pass


class RetryManager:
    """重试管理器"""

    def __init__(self, config: RetryConfig = None):
        self.config = config or RetryConfig()
        self.retry_history: Dict[str, list] = {}

    def calculate_delay(self, attempt: int) -> float:
        """计算延迟时间（指数退避）"""
        delay = min(
            self.config.base_delay * (self.config.exponential_base ** attempt),
            self.config.max_delay
        )

        # 添加抖动（避免雷鸣群效应）
        if self.config.jitter:
            import random
            delay = delay * (0.5 + random.random())

        return delay

    def should_retry(self, error: Exception, attempt: int) -> bool:
        """判断是否应该重试"""
        # 不可重试的错误
        if isinstance(error, NonRetryableError):
            return False

        # 超过最大重试次数
        if attempt >= self.config.max_retries:
            return False

        # 网络错误 - 可重试
        if isinstance(error, (ConnectionError, TimeoutError)):
            return True

        # 明确标记为可重试
        if isinstance(error, RetryableError):
            return True

        # 默认不重试
        return False

    def record_retry(self, task_id: str, attempt: int, error: str):
        """记录重试历史"""
        if task_id not in self.retry_history:
            self.retry_history[task_id] = []

        self.retry_history[task_id].append({
            'attempt': attempt,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })

    async def execute_with_retry(
        self,
        func: Callable,
        *args,
        task_id: str = None,
        **kwargs
    ) -> Any:
        """执行函数并自动重试"""
        task_id = task_id or f"task_{id(func)}"

        for attempt in range(self.config.max_retries + 1):
            try:
                result = await func(*args, **kwargs)

                # 成功后清除重试历史
                if task_id in self.retry_history:
                    del self.retry_history[task_id]

                return result

            except Exception as e:
                logger.warning(f"任务 {task_id} 第 {attempt + 1} 次尝试失败: {e}")

                # 记录重试
                self.record_retry(task_id, attempt + 1, str(e))

                # 判断是否重试
                if not self.should_retry(e, attempt):
                    logger.error(f"任务 {task_id} 失败，不再重试")
                    raise

                # 计算延迟
                if attempt < self.config.max_retries:
                    delay = self.calculate_delay(attempt)
                    logger.info(f"等待 {delay:.2f} 秒后重试...")
                    await asyncio.sleep(delay)

        raise Exception(f"任务 {task_id} 重试 {self.config.max_retries} 次后仍然失败")


def retry_on_error(
    max_retries: int = 3,
    base_delay: float = 1.0,
    exponential_base: float = 2.0
):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            config = RetryConfig(
                max_retries=max_retries,
                base_delay=base_delay,
                exponential_base=exponential_base
            )
            manager = RetryManager(config)
            return await manager.execute_with_retry(func, *args, **kwargs)
        return wrapper
    return decorator


class CheckpointManager:
    """断点续传管理器"""

    def __init__(self, checkpoint_dir: str = "data/checkpoints"):
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(checkpoint_dir, exist_ok=True)

    def save_checkpoint(self, task_id: str, state: Dict[str, Any]):
        """保存检查点"""
        checkpoint_file = os.path.join(self.checkpoint_dir, f"{task_id}.json")

        try:
            with open(checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'task_id': task_id,
                    'state': state,
                    'timestamp': datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)

            logger.info(f"检查点已保存: {task_id}")

        except Exception as e:
            logger.error(f"保存检查点失败: {e}")

    def load_checkpoint(self, task_id: str) -> Optional[Dict[str, Any]]:
        """加载检查点"""
        checkpoint_file = os.path.join(self.checkpoint_dir, f"{task_id}.json")

        if not os.path.exists(checkpoint_file):
            return None

        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"检查点已加载: {task_id}")
                return data.get('state')

        except Exception as e:
            logger.error(f"加载检查点失败: {e}")
            return None

    def delete_checkpoint(self, task_id: str):
        """删除检查点"""
        checkpoint_file = os.path.join(self.checkpoint_dir, f"{task_id}.json")

        if os.path.exists(checkpoint_file):
            try:
                os.remove(checkpoint_file)
                logger.info(f"检查点已删除: {task_id}")
            except Exception as e:
                logger.error(f"删除检查点失败: {e}")

    def list_checkpoints(self) -> list:
        """列出所有检查点"""
        try:
            files = os.listdir(self.checkpoint_dir)
            return [f.replace('.json', '') for f in files if f.endswith('.json')]
        except Exception as e:
            logger.error(f"列出检查点失败: {e}")
            return []


# 使用示例
if __name__ == "__main__":
    async def test_retry():
        """测试重试机制"""

        @retry_on_error(max_retries=3, base_delay=1.0)
        async def flaky_function():
            import random
            if random.random() < 0.7:  # 70% 失败率
                raise RetryableError("模拟失败")
            return "成功"

        try:
            result = await flaky_function()
            print(f"结果: {result}")
        except Exception as e:
            print(f"最终失败: {e}")

    # 运行测试
    asyncio.run(test_retry())
