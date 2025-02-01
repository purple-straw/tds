"""
基础服务类，提供通用的服务功能
"""
from app.base.base_request import BaseRequest
from app.utils.db_utils import DatabaseConnection
from app.utils.log_control import INFO, ERROR
from app.config.api_config import API_BASE_URL, API_LOGIN, DEFAULT_HEADERS, LOGIN_DATA
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BaseService:
    def __init__(self):
        self.db = DatabaseConnection()

    def execute_query(self, sql, params=None):
        """执行数据库查询"""
        try:
            result = self.db.execute_query(sql, params)
            if not result.get('data'):
                return []
            return result['data']
        except Exception as e:
            ERROR.logger.error(f"数据库查询失败: {str(e)}")
            raise


class BaseAPIService(BaseService):
    """包含API请求功能的基础服务类"""

    def __init__(self):
        super().__init__()
        self.headers = DEFAULT_HEADERS.copy()
        self.headers.update({
            'Connection': 'keep-alive',
            'accesstoken': 'domain=.cepin.com',
            'Host': 'test-tds-standard.cepin.com',
            'X-Requested-With': 'XMLHttpRequest'
        })
        self.base_url = API_BASE_URL
        self.token = None
        self._login()

    def _login(self):
        """登录获取token"""
        try:
            INFO.logger.info(f"正在请求登录接口: {API_LOGIN}")

            response = requests.post(
                API_LOGIN,
                json=LOGIN_DATA,
                headers=self.headers,
                verify=False
            )

            result = response.json()

            if result.get('code') == 0:
                self.token = result.get('response')
                self.headers.update({
                    'accesstoken': self.token,
                    'Authorization': f'Bearer {self.token}'
                })
                INFO.logger.info("登录成功")
                return True

            ERROR.logger.error(f"登录失败: {result.get('message')}")
            return False

        except Exception as e:
            ERROR.logger.error(f"登录异常: {str(e)}")
            return False

    def get(self, endpoint, params=None):
        """发送GET请求"""
        try:
            if not self.token and not self._login():
                raise Exception("未登录")

            url = f"{self.base_url}{endpoint}"
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                verify=False
            )

            result = response.json()

            if result.get('code') == 0:
                return result

            if result.get('code') == 401 and self._login():  # Token过期，重新登录
                response = requests.get(
                    url,
                    params=params,
                    headers=self.headers,
                    verify=False
                )
                result = response.json()
                if result.get('code') == 0:
                    return result

            raise Exception(result.get('message') or "请求失败")

        except Exception as e:
            ERROR.logger.error(f"GET请求失败: {str(e)}")
            raise

    def post(self, endpoint, data=None):
        """发送POST请求"""
        try:
            if not self.token and not self._login():
                raise Exception("未登录")

            url = f"{self.base_url}{endpoint}"
            response = requests.post(
                url,
                json=data,
                headers=self.headers,
                verify=False
            )

            result = response.json()

            if result.get('code') == 0:
                return result

            if result.get('code') == 401 and self._login():  # Token过期，重新登录
                response = requests.post(
                    url,
                    json=data,
                    headers=self.headers,
                    verify=False
                )
                result = response.json()
                if result.get('code') == 0:
                    return result

            raise Exception(result.get('message') or "请求失败")

        except Exception as e:
            ERROR.logger.error(f"POST请求失败: {str(e)}")
            raise

    def get_api_data(self, endpoint, params=None):
        """获取API数据的通用方法"""
        try:
            result = self.get(endpoint, params)
            if result.get('code') == 0:
                return result.get('response', {}).get('list', [])
            else:
                raise Exception(f"获取API数据失败: {result.get('message')}")
        except Exception as e:
            ERROR.logger.error(f"获取API数据失败: {str(e)}")
            raise
