"""
AIHawk 客户端封装
集成 GitHub 高星项目 Auto_Jobs_Applier_AIHawk
"""

import os
import sys
import yaml
import subprocess
from typing import Dict, List
from datetime import datetime

# 添加 AIHawk 到路径
AIHAWK_PATH = os.path.join(os.path.dirname(__file__), '../../third_party/Auto_Jobs_Applier_AIHawk')
sys.path.insert(0, AIHAWK_PATH)


class AIHawkClient:
    """AIHawk 客户端 - 自动投递岗位"""

    def __init__(self):
        self.aihawk_path = AIHAWK_PATH
        self.data_folder = os.path.join(self.aihawk_path, 'data_folder')

        # 确保数据目录存在
        os.makedirs(self.data_folder, exist_ok=True)

    def create_config_files(
        self,
        task_id: str,
        keywords: List[str],
        locations: List[str],
        max_count: int,
        resume_text: str,
        llm_api_key: str
    ) -> str:
        """创建 AIHawk 配置文件"""

        # 1. 保存简历
        resume_path = os.path.join(self.data_folder, f'resume_{task_id}.txt')
        with open(resume_path, 'w', encoding='utf-8') as f:
            f.write(resume_text)

        # 2. 创建 secrets.yaml
        secrets = {
            'llm_api_key': llm_api_key
        }
        secrets_path = os.path.join(self.data_folder, 'secrets.yaml')
        with open(secrets_path, 'w', encoding='utf-8') as f:
            yaml.dump(secrets, f)

        # 3. 创建 work_preferences.yaml
        work_preferences = {
            'remote': True,
            'hybrid': True,
            'onsite': True,
            'experience_level': {
                'internship': True,
                'entry': True,
                'associate': False,
                'mid_senior_level': False,
                'director': False,
                'executive': False
            },
            'job_types': {
                'full_time': True,
                'contract': False,
                'part_time': True,
                'temporary': False,
                'internship': True,
                'other': False,
                'volunteer': False
            },
            'date': {
                'all_time': False,
                'month': False,
                'week': True,
                '24_hours': False
            },
            'positions': keywords,
            'locations': locations,
            'apply_once_at_company': True,
            'distance': 50,
            'company_blacklist': [],
            'title_blacklist': [],
            'location_blacklist': []
        }
        work_pref_path = os.path.join(self.data_folder, 'work_preferences.yaml')
        with open(work_pref_path, 'w', encoding='utf-8') as f:
            yaml.dump(work_preferences, f)

        # 4. 创建 plain_text_resume.yaml（简历结构化数据）
        plain_text_resume = self._parse_resume_to_yaml(resume_text)
        resume_yaml_path = os.path.join(self.data_folder, 'plain_text_resume.yaml')
        with open(resume_yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(plain_text_resume, f, allow_unicode=True)

        return self.data_folder

    def _parse_resume_to_yaml(self, resume_text: str) -> Dict:
        """将简历文本解析为 YAML 格式"""

        # 简单解析（实际应该更智能）
        lines = resume_text.split('\n')

        # 提取基本信息
        name = lines[0].replace('姓名:', '').strip() if lines else "Unknown"

        # 提取联系方式
        email = ""
        phone = ""
        for line in lines[:10]:
            if '@' in line:
                email = line.split('@')[0].split()[-1] + '@' + line.split('@')[1].split()[0]
            if '手机' in line or '电话' in line:
                import re
                phone_match = re.search(r'1[3-9]\d{9}', line)
                if phone_match:
                    phone = phone_match.group()

        return {
            'personal_information': {
                'name': name,
                'surname': '',
                'date_of_birth': '',
                'country': 'China',
                'city': '北京',
                'address': '',
                'zip_code': '',
                'phone_prefix': '+86',
                'phone': phone,
                'email': email,
                'github': '',
                'linkedin': ''
            },
            'self_identification': {
                'gender': '',
                'pronouns': '',
                'veteran': '',
                'disability': '',
                'ethnicity': ''
            },
            'legal_authorization': {
                'eu_work_authorization': '',
                'us_work_authorization': '',
                'requires_us_visa': '',
                'requires_us_sponsorship': '',
                'requires_eu_visa': '',
                'legally_allowed_to_work_in_eu': '',
                'legally_allowed_to_work_in_us': '',
                'requires_eu_sponsorship': '',
                'canada_work_authorization': '',
                'requires_canada_visa': '',
                'legally_allowed_to_work_in_canada': '',
                'requires_canada_sponsorship': '',
                'uk_work_authorization': '',
                'requires_uk_visa': '',
                'legally_allowed_to_work_in_uk': '',
                'requires_uk_sponsorship': ''
            },
            'work_preferences': {
                'remote_work': True,
                'in_person_work': True,
                'open_to_relocation': True,
                'willing_to_complete_assessments': True,
                'willing_to_undergo_drug_tests': False,
                'willing_to_undergo_background_checks': True
            },
            'education_details': [],
            'experience_details': [],
            'projects': [],
            'availability': {
                'notice_period': '2 weeks'
            },
            'salary_expectations': {
                'salary_range_usd': '3000-5000'
            },
            'certifications': [],
            'languages': [
                {
                    'language': 'Chinese',
                    'proficiency': 'Native'
                },
                {
                    'language': 'English',
                    'proficiency': 'Professional'
                }
            ],
            'interests': []
        }

    def run_aihawk(self, task_id: str, max_count: int) -> Dict:
        """运行 AIHawk 自动投递"""

        try:
            # 修改 config.py 中的最大投递数
            config_path = os.path.join(self.aihawk_path, 'config.py')
            self._update_config(config_path, max_count)

            # 运行 AIHawk
            cmd = [
                sys.executable,
                os.path.join(self.aihawk_path, 'main.py')
            ]

            print(f"[{task_id}] 执行命令: {' '.join(cmd)}")
            print(f"[{task_id}] 工作目录: {self.aihawk_path}")

            result = subprocess.run(
                cmd,
                cwd=self.aihawk_path,
                capture_output=True,
                text=True,
                timeout=3600,  # 1小时超时
                env={**os.environ, 'PYTHONPATH': self.aihawk_path}
            )

            # 解析结果
            output = result.stdout
            error = result.stderr

            # 从输出中提取统计信息
            applied_count = self._extract_count(output, r'Applied to (\d+) jobs')
            success_count = self._extract_count(output, r'Successfully applied to (\d+)')
            failed_count = applied_count - success_count if applied_count > 0 else 0

            return {
                'success': result.returncode == 0,
                'applied_count': applied_count,
                'success_count': success_count,
                'failed_count': failed_count,
                'output': output,
                'error': error if result.returncode != 0 else None
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': '任务超时（超过1小时）'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _update_config(self, config_path: str, max_count: int):
        """更新 config.py 中的最大投递数"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 替换最大投递数
            import re
            content = re.sub(
                r'JOB_MAX_APPLICATIONS = \d+',
                f'JOB_MAX_APPLICATIONS = {max_count}',
                content
            )

            # 修改 LLM 配置为 DeepSeek
            content = re.sub(
                r"LLM_MODEL_TYPE = '[^']*'",
                "LLM_MODEL_TYPE = 'openai'",
                content
            )
            content = re.sub(
                r"LLM_MODEL = '[^']*'",
                "LLM_MODEL = 'deepseek-chat'",
                content
            )

            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(content)

        except Exception as e:
            print(f"警告: 无法更新配置文件: {e}")

    def _extract_count(self, text: str, pattern: str) -> int:
        """从文本中提取数字"""
        import re
        match = re.search(pattern, text)
        return int(match.group(1)) if match else 0


# 全局实例
aihawk_client = AIHawkClient()
