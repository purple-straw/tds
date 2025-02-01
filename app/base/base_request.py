"""
@Project ：tds_dev 
@File    ：base_request.py
@IDE     ：PyCharm 
@Author  ：靓仔
@Date    ：2025/1/21
"""

import json
import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from app.config.api_config import (
    API_LOGIN,
    DEFAULT_HEADERS,
    LOGIN_DATA
)
from app.utils.log_control import INFO, ERROR
from contextlib import contextmanager

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BaseRequest:
    def __init__(self):
        self.session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=3,  # 最大重试次数
            backoff_factor=0.5,  # 重试间隔
            status_forcelist=[500, 502, 503, 504],  # 需要重试的HTTP状态码
        )
        
        # 配置适配器
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,  # 连接池大小
            pool_maxsize=10  # 最大连接数
        )
        
        # 注册适配器
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        # 设置默认超时
        self.timeout = (5, 15)  # (连接超时, 读取超时)
        
        self.headers = DEFAULT_HEADERS.copy()
        # 添加一些必要的请求头
        self.headers.update({
            'Connection': 'keep-alive',
            'accesstoken': 'domain=.cepin.com',
            'Host': 'test-tds-standard.cepin.com',
            'X-Requested-With': 'XMLHttpRequest'
        })
        if 'accept-encoding' in self.headers:
            del self.headers['accept-encoding']
        self.login = API_LOGIN
        self.token = None
        self._login()  # 初始化时自动登录获取token

    def _login(self):
        """内部登录方法，获取token"""
        try:
            INFO.logger.info(f"正在请求登录接口: {self.login}")

            response = self.session.post(
                self.login,
                json=LOGIN_DATA,
                headers=self.headers,
                verify=False,
                timeout=self.timeout
            )

            result = response.json()

            if result.get('code') == 0:
                self.token = result.get('response')
                self.headers['accesstoken'] = self.token
                self.headers['Authorization'] = f'Bearer {self.token}'
                INFO.logger.info("登录成功")
            else:
                ERROR.logger.error(f"登录失败: {result.get('message')}")
                raise Exception(f"登录失败: {result.get('message')}")

            return result

        except requests.exceptions.Timeout:
            ERROR.logger.error("登录请求超时")
            raise
        except requests.exceptions.ConnectionError:
            ERROR.logger.error("连接服务器失败")
            raise
        except requests.exceptions.RequestException as e:
            ERROR.logger.error(f"请求失败: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            ERROR.logger.error(f"JSON解析失败: {str(e)}")
            raise

    @contextmanager
    def get_session(self):
        """获取一个新的会话"""
        session = requests.Session()
        try:
            yield session
        finally:
            session.close()

    def get(self, endpoint):
        """GET请求"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(
                url,
                headers=self.headers,
                verify=False,
                timeout=self.timeout
            )
            return response.json()
        except Exception as e:
            ERROR.logger.error(f"GET请求失败: {str(e)}")
            return {'error': str(e)}

    def post(self, endpoint, data=None):
        """POST请求"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.post(
                url,
                json=data,
                headers=self.headers,
                verify=False,
                timeout=self.timeout
            )
            return response.json()
        except Exception as e:
            ERROR.logger.error(f"POST请求失败: {str(e)}")
            return {'error': str(e)}

# 创建全局实例
api_client = BaseRequest()
