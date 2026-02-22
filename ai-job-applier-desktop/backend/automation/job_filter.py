"""
投递去重器
避免重复投递同一岗位
"""

import hashlib
import json
import logging
import os
from typing import Set, Dict, Optional, List
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


class DeduplicateManager:
    """去重管理器"""

    def __init__(self, storage_file: str = "data/applied_jobs.json"):
        self.storage_file = storage_file
        self.applied_jobs: Set[str] = set()
        self.job_details: Dict[str, Dict] = {}
        self._load()

    def _load(self):
        """加载已投递记录"""
        if not os.path.exists(self.storage_file):
            return

        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.applied_jobs = set(data.get('applied_jobs', []))
                self.job_details = data.get('job_details', {})
            logger.info(f"已加载 {len(self.applied_jobs)} 条投递记录")
        except Exception as e:
            logger.error(f"加载投递记录失败: {e}")

    def _save(self):
        """保存投递记录"""
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)

        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'applied_jobs': list(self.applied_jobs),
                    'job_details': self.job_details,
                    'updated_at': datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存投递记录失败: {e}")

    def generate_job_id(self, job: Dict) -> str:
        """生成岗位唯一ID"""
        # 使用多个字段组合生成唯一ID
        key_fields = [
            job.get('job_id', ''),
            job.get('company', ''),
            job.get('job_title', ''),
            job.get('location', '')
        ]

        key_string = '|'.join(str(f) for f in key_fields)
        return hashlib.md5(key_string.encode()).hexdigest()

    def is_applied(self, job: Dict) -> bool:
        """检查是否已投递"""
        job_id = self.generate_job_id(job)
        return job_id in self.applied_jobs

    def mark_applied(self, job: Dict):
        """标记为已投递"""
        job_id = self.generate_job_id(job)
        self.applied_jobs.add(job_id)

        # 保存详细信息
        self.job_details[job_id] = {
            'job_title': job.get('job_title'),
            'company': job.get('company'),
            'applied_at': datetime.now().isoformat(),
            'job_url': job.get('job_url', '')
        }

        self._save()
        logger.info(f"已标记投递: {job.get('company')} - {job.get('job_title')}")

    def get_applied_count(self) -> int:
        """获取已投递数量"""
        return len(self.applied_jobs)

    def get_applied_today(self) -> int:
        """获取今日投递数量"""
        today = datetime.now().date()
        count = 0

        for job_id, details in self.job_details.items():
            applied_at = datetime.fromisoformat(details['applied_at'])
            if applied_at.date() == today:
                count += 1

        return count

    def get_applied_companies(self) -> Set[str]:
        """获取已投递的公司列表"""
        companies = set()
        for details in self.job_details.values():
            companies.add(details['company'])
        return companies

    def clear_old_records(self, days: int = 90):
        """清理旧记录"""
        cutoff_date = datetime.now() - timedelta(days=days)
        removed_count = 0

        job_ids_to_remove = []
        for job_id, details in self.job_details.items():
            applied_at = datetime.fromisoformat(details['applied_at'])
            if applied_at < cutoff_date:
                job_ids_to_remove.append(job_id)

        for job_id in job_ids_to_remove:
            self.applied_jobs.discard(job_id)
            del self.job_details[job_id]
            removed_count += 1

        if removed_count > 0:
            self._save()
            logger.info(f"已清理 {removed_count} 条旧记录")


class BlacklistManager:
    """黑名单管理器"""

    def __init__(self, storage_file: str = "data/blacklist.json"):
        self.storage_file = storage_file
        self.blacklist: Dict[str, List[str]] = defaultdict(list)
        self._load()

    def _load(self):
        """加载黑名单"""
        if not os.path.exists(self.storage_file):
            return

        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                self.blacklist = defaultdict(list, json.load(f))
            logger.info(f"已加载黑名单")
        except Exception as e:
            logger.error(f"加载黑名单失败: {e}")

    def _save(self):
        """保存黑名单"""
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)

        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(dict(self.blacklist), f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存黑名单失败: {e}")

    def add_company(self, company: str, reason: str = ""):
        """添加公司到黑名单"""
        if company not in self.blacklist['companies']:
            self.blacklist['companies'].append(company)
            self._save()
            logger.info(f"已添加公司到黑名单: {company} ({reason})")

    def add_keyword(self, keyword: str, reason: str = ""):
        """添加关键词到黑名单"""
        if keyword not in self.blacklist['keywords']:
            self.blacklist['keywords'].append(keyword)
            self._save()
            logger.info(f"已添加关键词到黑名单: {keyword} ({reason})")

    def is_blacklisted(self, job: Dict) -> tuple[bool, str]:
        """检查岗位是否在黑名单"""
        company = job.get('company', '')
        job_title = job.get('job_title', '')
        description = job.get('description', '')

        # 检查公司黑名单
        for blacklisted_company in self.blacklist.get('companies', []):
            if blacklisted_company.lower() in company.lower():
                return True, f"公司在黑名单: {blacklisted_company}"

        # 检查关键词黑名单
        full_text = f"{job_title} {description}".lower()
        for keyword in self.blacklist.get('keywords', []):
            if keyword.lower() in full_text:
                return True, f"包含黑名单关键词: {keyword}"

        return False, ""

    def remove_company(self, company: str):
        """从黑名单移除公司"""
        if company in self.blacklist['companies']:
            self.blacklist['companies'].remove(company)
            self._save()
            logger.info(f"已从黑名单移除公司: {company}")

    def remove_keyword(self, keyword: str):
        """从黑名单移除关键词"""
        if keyword in self.blacklist['keywords']:
            self.blacklist['keywords'].remove(keyword)
            self._save()
            logger.info(f"已从黑名单移除关键词: {keyword}")


class JobFilter:
    """岗位过滤器（综合去重和黑名单）"""

    def __init__(self):
        self.dedup_manager = DeduplicateManager()
        self.blacklist_manager = BlacklistManager()

    def should_apply(self, job: Dict) -> tuple[bool, str]:
        """判断是否应该投递"""
        # 检查是否已投递
        if self.dedup_manager.is_applied(job):
            return False, "已投递过"

        # 检查黑名单
        is_blacklisted, reason = self.blacklist_manager.is_blacklisted(job)
        if is_blacklisted:
            return False, reason

        return True, "可以投递"

    def mark_applied(self, job: Dict):
        """标记为已投递"""
        self.dedup_manager.mark_applied(job)

    def filter_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """过滤岗位列表"""
        filtered_jobs = []
        stats = {
            'total': len(jobs),
            'already_applied': 0,
            'blacklisted': 0,
            'passed': 0
        }

        for job in jobs:
            should_apply, reason = self.should_apply(job)

            if should_apply:
                filtered_jobs.append(job)
                stats['passed'] += 1
            elif "已投递" in reason:
                stats['already_applied'] += 1
            else:
                stats['blacklisted'] += 1

        logger.info(
            f"岗位过滤完成: 总数 {stats['total']}, "
            f"已投递 {stats['already_applied']}, "
            f"黑名单 {stats['blacklisted']}, "
            f"可投递 {stats['passed']}"
        )

        return filtered_jobs

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'total_applied': self.dedup_manager.get_applied_count(),
            'applied_today': self.dedup_manager.get_applied_today(),
            'applied_companies': len(self.dedup_manager.get_applied_companies()),
            'blacklisted_companies': len(self.blacklist_manager.blacklist.get('companies', [])),
            'blacklisted_keywords': len(self.blacklist_manager.blacklist.get('keywords', []))
        }


# 使用示例
if __name__ == "__main__":
    # 创建过滤器
    job_filter = JobFilter()

    # 添加黑名单
    job_filter.blacklist_manager.add_company("某外包公司", "外包")
    job_filter.blacklist_manager.add_keyword("996", "工作制度")

    # 测试岗位
    test_jobs = [
        {'job_id': '1', 'company': 'A公司', 'job_title': 'Python开发'},
        {'job_id': '2', 'company': '某外包公司', 'job_title': 'Java开发'},
        {'job_id': '3', 'company': 'B公司', 'job_title': 'Go开发 996'},
        {'job_id': '1', 'company': 'A公司', 'job_title': 'Python开发'},  # 重复
    ]

    # 过滤
    filtered = job_filter.filter_jobs(test_jobs)
    print(f"过滤后: {len(filtered)} 个岗位")

    # 标记投递
    for job in filtered:
        job_filter.mark_applied(job)

    # 统计
    print(f"统计: {job_filter.get_stats()}")
