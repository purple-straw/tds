"""
配置管理器
"""
import os
from typing import Dict, Any


class ConfigManager:
    _instance = None
    _config = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._config:
            self._load_config()

    def _load_config(self):
        """加载配置"""
        self._config = {
            'api': {
                'base_url': 'https://test-tds-standard.cepin.com',
                'login': '/api/tds-system/admin/login',
                'headers': {
                    'Connection': 'keep-alive',
                    'accesstoken': 'domain=.cepin.com',
                    'Host': 'test-tds-standard.cepin.com',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                'login_data': {
                    "loginName": "admin",
                    "password": "123456",
                    "type": "account"
                }
            },
            'database': {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': int(os.getenv('DB_PORT', 3306)),
                'user': os.getenv('DB_USER', 'root'),
                'password': os.getenv('DB_PASSWORD', ''),
                'database': os.getenv('DB_NAME', 'tds'),
                'charset': 'utf8mb4'
            },
            'endpoints': {
                'personnel': {
                    'list': '/api/tds-system/admin/organization/personnel/list',
                    'db_list': '/api/tds-system/admin/organization/personnel/db/list',
                    'rank_distribution': '/api/tds-system/admin/organization/personnel/rank/distribution',
                    'db_rank_distribution': '/api/tds-system/admin/organization/personnel/db/rank/distribution',
                    'age_average': '/api/tds-system/admin/organization/personnel/age/average',
                    'db_age_average': '/api/tds-system/admin/organization/personnel/db/age/average'
                }
            }
        }

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    def get_all(self) -> Dict:
        """获取所有配置"""
        return self._config.copy()

    def update(self, key: str, value: Any) -> None:
        """更新配置值"""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value


# 创建全局配置实例
config = ConfigManager()
