"""
人类行为模拟器
模拟真实的鼠标移动和键盘输入
"""

import asyncio
import random
import logging
from typing import Tuple, List
from playwright.async_api import Page

logger = logging.getLogger(__name__)


class HumanBehaviorSimulator:
    """人类行为模拟器"""

    def __init__(self, page: Page):
        self.page = page

    @staticmethod
    def bezier_curve(
        start: Tuple[float, float],
        end: Tuple[float, float],
        control_points: int = 2
    ) -> List[Tuple[float, float]]:
        """生成贝塞尔曲线路径"""
        points = []

        # 生成控制点
        controls = []
        for _ in range(control_points):
            x = random.uniform(min(start[0], end[0]), max(start[0], end[0]))
            y = random.uniform(min(start[1], end[1]), max(start[1], end[1]))
            controls.append((x, y))

        # 生成曲线上的点
        steps = random.randint(20, 40)
        for i in range(steps + 1):
            t = i / steps

            # 三次贝塞尔曲线
            if control_points == 2:
                x = (
                    (1 - t) ** 3 * start[0] +
                    3 * (1 - t) ** 2 * t * controls[0][0] +
                    3 * (1 - t) * t ** 2 * controls[1][0] +
                    t ** 3 * end[0]
                )
                y = (
                    (1 - t) ** 3 * start[1] +
                    3 * (1 - t) ** 2 * t * controls[0][1] +
                    3 * (1 - t) * t ** 2 * controls[1][1] +
                    t ** 3 * end[1]
                )
            else:
                # 简单线性插值
                x = start[0] + (end[0] - start[0]) * t
                y = start[1] + (end[1] - start[1]) * t

            points.append((x, y))

        return points

    async def move_mouse_human_like(
        self,
        target_x: float,
        target_y: float,
        duration: float = None
    ):
        """人类般的鼠标移动"""
        try:
            # 获取当前鼠标位置（假设从中心开始）
            current_x = random.randint(800, 1000)
            current_y = random.randint(400, 600)

            # 生成贝塞尔曲线路径
            path = self.bezier_curve(
                (current_x, current_y),
                (target_x, target_y),
                control_points=2
            )

            # 计算总时长
            if duration is None:
                distance = ((target_x - current_x) ** 2 + (target_y - current_y) ** 2) ** 0.5
                duration = random.uniform(0.5, 1.5) * (distance / 1000)

            # 沿路径移动
            step_delay = duration / len(path)
            for x, y in path:
                await self.page.mouse.move(x, y)
                await asyncio.sleep(step_delay + random.uniform(-0.01, 0.01))

            logger.debug(f"鼠标移动到 ({target_x}, {target_y})")

        except Exception as e:
            logger.error(f"鼠标移动失败: {e}")

    async def click_human_like(
        self,
        x: float,
        y: float,
        button: str = "left"
    ):
        """人类般的点击"""
        try:
            # 移动到目标位置（带随机偏移）
            offset_x = random.uniform(-5, 5)
            offset_y = random.uniform(-5, 5)
            await self.move_mouse_human_like(x + offset_x, y + offset_y)

            # 随机延迟
            await asyncio.sleep(random.uniform(0.1, 0.3))

            # 按下
            await self.page.mouse.down(button=button)
            await asyncio.sleep(random.uniform(0.05, 0.15))

            # 释放
            await self.page.mouse.up(button=button)

            logger.debug(f"点击 ({x}, {y})")

        except Exception as e:
            logger.error(f"点击失败: {e}")

    async def type_human_like(
        self,
        selector: str,
        text: str,
        delay_range: Tuple[float, float] = (0.05, 0.15)
    ):
        """人类般的键盘输入"""
        try:
            # 聚焦输入框
            await self.page.click(selector)
            await asyncio.sleep(random.uniform(0.2, 0.5))

            # 逐字输入
            for char in text:
                await self.page.keyboard.type(char)

                # 随机延迟（模拟打字速度）
                delay = random.uniform(*delay_range)

                # 偶尔停顿（模拟思考）
                if random.random() < 0.1:
                    delay += random.uniform(0.3, 0.8)

                await asyncio.sleep(delay)

            logger.debug(f"输入文本: {text[:20]}...")

        except Exception as e:
            logger.error(f"输入失败: {e}")

    async def scroll_human_like(
        self,
        direction: str = "down",
        amount: int = None
    ):
        """人类般的滚动"""
        try:
            if amount is None:
                amount = random.randint(300, 800)

            # 分段滚动（更自然）
            segments = random.randint(3, 6)
            segment_amount = amount // segments

            for _ in range(segments):
                scroll_value = segment_amount if direction == "down" else -segment_amount

                # 添加随机抖动
                scroll_value += random.randint(-50, 50)

                await self.page.evaluate(f"window.scrollBy(0, {scroll_value})")
                await asyncio.sleep(random.uniform(0.1, 0.3))

            logger.debug(f"滚动 {direction} {amount}px")

        except Exception as e:
            logger.error(f"滚动失败: {e}")

    async def random_mouse_movement(self):
        """随机鼠标移动（模拟浏览）"""
        try:
            # 随机移动 2-4 次
            movements = random.randint(2, 4)

            for _ in range(movements):
                x = random.randint(200, 1700)
                y = random.randint(200, 900)
                await self.move_mouse_human_like(x, y)
                await asyncio.sleep(random.uniform(0.5, 1.5))

        except Exception as e:
            logger.error(f"随机移动失败: {e}")

    async def simulate_reading(self, duration: float = None):
        """模拟阅读页面"""
        try:
            if duration is None:
                duration = random.uniform(2, 5)

            # 随机滚动和停顿
            elapsed = 0
            while elapsed < duration:
                # 滚动一小段
                await self.scroll_human_like("down", amount=random.randint(100, 300))

                # 停顿（模拟阅读）
                pause = random.uniform(0.5, 2.0)
                await asyncio.sleep(pause)
                elapsed += pause

                # 偶尔向上滚动（模拟回看）
                if random.random() < 0.2:
                    await self.scroll_human_like("up", amount=random.randint(50, 150))
                    await asyncio.sleep(random.uniform(0.3, 0.8))

            logger.debug(f"模拟阅读 {duration:.1f} 秒")

        except Exception as e:
            logger.error(f"模拟阅读失败: {e}")

    async def simulate_hesitation(self):
        """模拟犹豫（投递前）"""
        try:
            # 鼠标在按钮附近徘徊
            for _ in range(random.randint(2, 4)):
                x = random.randint(800, 1000)
                y = random.randint(400, 600)
                await self.move_mouse_human_like(x, y)
                await asyncio.sleep(random.uniform(0.3, 0.8))

            # 停顿（模拟思考）
            await asyncio.sleep(random.uniform(1.0, 3.0))

            logger.debug("模拟犹豫")

        except Exception as e:
            logger.error(f"模拟犹豫失败: {e}")


class AntiDetectionEnhancer:
    """反检测增强器"""

    def __init__(self, page: Page):
        self.page = page

    async def inject_advanced_scripts(self):
        """注入高级反检测脚本"""
        # 1. 伪造浏览器插件
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    {
                        name: 'Chrome PDF Plugin',
                        filename: 'internal-pdf-viewer',
                        description: 'Portable Document Format'
                    },
                    {
                        name: 'Chrome PDF Viewer',
                        filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
                        description: ''
                    }
                ]
            });
        """)

        # 2. 伪造语言
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en-US', 'en']
            });
        """)

        # 3. 伪造硬件并发数
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'hardwareConcurrency', {
                get: () => 8
            });
        """)

        # 4. 伪造设备内存
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'deviceMemory', {
                get: () => 8
            });
        """)

        # 5. 伪造权限
        await self.page.add_init_script("""
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """)

        logger.info("高级反检测脚本已注入")

    async def randomize_viewport(self):
        """随机化视口大小"""
        widths = [1366, 1440, 1536, 1920]
        heights = [768, 900, 864, 1080]

        width = random.choice(widths)
        height = random.choice(heights)

        await self.page.set_viewport_size({"width": width, "height": height})
        logger.debug(f"视口大小: {width}x{height}")


# 使用示例
async def example_usage():
    """使用示例"""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 创建模拟器
        simulator = HumanBehaviorSimulator(page)
        enhancer = AntiDetectionEnhancer(page)

        # 注入反检测脚本
        await enhancer.inject_advanced_scripts()

        # 访问页面
        await page.goto("https://www.zhipin.com")

        # 模拟人类行为
        await simulator.simulate_reading(duration=3)
        await simulator.random_mouse_movement()

        # 输入文本
        await simulator.type_human_like("#search-input", "Python开发工程师")

        # 点击搜索
        button = await page.query_selector("#search-button")
        if button:
            box = await button.bounding_box()
            await simulator.click_human_like(
                box['x'] + box['width'] / 2,
                box['y'] + box['height'] / 2
            )

        await asyncio.sleep(5)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(example_usage())
