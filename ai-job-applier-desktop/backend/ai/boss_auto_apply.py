"""
Boss 直聘自动投递引擎 - 使用 Playwright 浏览器自动化
"""
import asyncio
from playwright.async_api import async_playwright, Page, Browser
from typing import Dict, List, Optional
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class BossAutoApply:
    """Boss 直聘自动投递"""

    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.cookies_file = Path("data/boss_cookies.json")
        self.is_logged_in = False

    async def init_browser(self):
        """初始化浏览器"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=False,  # 显示浏览器,方便调试
            args=['--start-maximized']
        )
        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = await context.new_page()

        # 加载 cookies
        if self.cookies_file.exists():
            with open(self.cookies_file, 'r') as f:
                cookies = json.load(f)
                await context.add_cookies(cookies)
                self.is_logged_in = True
                logger.info("已加载 Boss 直聘 cookies")

    async def login_with_qrcode(self):
        """扫码登录 Boss 直聘"""
        try:
            await self.page.goto('https://www.zhipin.com/')
            await self.page.wait_for_timeout(2000)

            # 点击登录按钮
            login_btn = await self.page.query_selector('.btns .btn-sign-up')
            if login_btn:
                await login_btn.click()
                await self.page.wait_for_timeout(1000)

            # 切换到扫码登录
            qr_tab = await self.page.query_selector('.sign-form-switch')
            if qr_tab:
                await qr_tab.click()

            logger.info("请使用 Boss 直聘 APP 扫码登录...")

            # 等待登录成功(检测用户头像出现)
            await self.page.wait_for_selector('.user-avatar', timeout=120000)

            # 保存 cookies
            cookies = await self.page.context.cookies()
            self.cookies_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cookies_file, 'w') as f:
                json.dump(cookies, f)

            self.is_logged_in = True
            logger.info("Boss 直聘登录成功!")
            return True

        except Exception as e:
            logger.error(f"登录失败: {e}")
            return False

    async def search_jobs(self, keyword: str, city: str = "全国", page_num: int = 1) -> List[Dict]:
        """搜索岗位"""
        try:
            # 构建搜索 URL
            search_url = f"https://www.zhipin.com/web/geek/job?query={keyword}&city={city}&page={page_num}"
            await self.page.goto(search_url)
            await self.page.wait_for_timeout(3000)

            # 解析岗位列表
            jobs = []
            job_cards = await self.page.query_selector_all('.job-card-wrapper')

            for card in job_cards:
                try:
                    # 提取岗位信息
                    title_elem = await card.query_selector('.job-title')
                    title = await title_elem.inner_text() if title_elem else ""

                    salary_elem = await card.query_selector('.salary')
                    salary = await salary_elem.inner_text() if salary_elem else ""

                    company_elem = await card.query_selector('.company-name')
                    company = await company_elem.inner_text() if company_elem else ""

                    link_elem = await card.query_selector('.job-card-left')
                    job_link = await link_elem.get_attribute('href') if link_elem else ""
                    if job_link and not job_link.startswith('http'):
                        job_link = f"https://www.zhipin.com{job_link}"

                    jobs.append({
                        'title': title.strip(),
                        'salary': salary.strip(),
                        'company': company.strip(),
                        'url': job_link,
                        'platform': 'boss'
                    })

                except Exception as e:
                    logger.error(f"解析岗位失败: {e}")
                    continue

            logger.info(f"搜索到 {len(jobs)} 个岗位")
            return jobs

        except Exception as e:
            logger.error(f"搜索岗位失败: {e}")
            return []

    async def apply_job(self, job_url: str, greeting_message: str = "") -> bool:
        """投递岗位"""
        try:
            # 打开岗位详情页
            await self.page.goto(job_url)
            await self.page.wait_for_timeout(2000)

            # 查找"立即沟通"按钮
            chat_btn = await self.page.query_selector('.btn-startchat')
            if not chat_btn:
                logger.warning("未找到沟通按钮,可能已投递或岗位已关闭")
                return False

            # 点击沟通按钮
            await chat_btn.click()
            await self.page.wait_for_timeout(2000)

            # 如果有打招呼输入框,输入消息
            if greeting_message:
                input_box = await self.page.query_selector('.chat-input')
                if input_box:
                    await input_box.fill(greeting_message)
                    await self.page.wait_for_timeout(500)

                    # 点击发送
                    send_btn = await self.page.query_selector('.btn-send')
                    if send_btn:
                        await send_btn.click()
                        await self.page.wait_for_timeout(1000)

            logger.info(f"投递成功: {job_url}")
            return True

        except Exception as e:
            logger.error(f"投递失败: {e}")
            return False

    async def batch_apply(
        self,
        keyword: str,
        city: str = "全国",
        max_count: int = 10,
        greeting_template: str = "",
        progress_callback=None
    ) -> Dict:
        """批量投递"""
        try:
            # 确保已登录
            if not self.is_logged_in:
                success = await self.login_with_qrcode()
                if not success:
                    return {'success': 0, 'failed': 0, 'message': '登录失败'}

            results = {'success': 0, 'failed': 0, 'details': []}

            # 搜索岗位
            jobs = await self.search_jobs(keyword, city)
            jobs = jobs[:max_count]  # 限制数量

            # 逐个投递
            for i, job in enumerate(jobs):
                if progress_callback:
                    progress_callback(i + 1, len(jobs), f"投递: {job['title']}")

                # 生成个性化打招呼消息
                greeting = greeting_template.format(
                    company=job['company'],
                    position=job['title']
                ) if greeting_template else f"您好,我对{job['title']}职位很感兴趣,期待与您沟通!"

                # 投递
                success = await self.apply_job(job['url'], greeting)

                if success:
                    results['success'] += 1
                    results['details'].append({
                        'job': job['title'],
                        'company': job['company'],
                        'status': 'success'
                    })
                else:
                    results['failed'] += 1
                    results['details'].append({
                        'job': job['title'],
                        'company': job['company'],
                        'status': 'failed'
                    })

                # 间隔 5-10 秒,避免被限流
                await asyncio.sleep(5)

            return results

        except Exception as e:
            logger.error(f"批量投递失败: {e}")
            return {'success': 0, 'failed': 0, 'message': str(e)}

    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()


# 全局实例
_boss_auto_apply = None


async def get_boss_auto_apply() -> BossAutoApply:
    """获取 Boss 自动投递实例"""
    global _boss_auto_apply
    if _boss_auto_apply is None:
        _boss_auto_apply = BossAutoApply()
        await _boss_auto_apply.init_browser()
    return _boss_auto_apply
