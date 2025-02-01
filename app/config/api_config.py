"""
@Project ：tds_dev 
@File    ：api_config.py
@IDE     ：PyCharm 
@Author  ：靓仔
@Date    ：2025/1/21 0021 20:36 
"""

# API URLs
API_BASE_URL = "https://test-tds-standard.cepin.com"
API_LOGIN = f"{API_BASE_URL}/api/tds-system/admin/login"
API_ORGANIZATION_INFO = f"{API_BASE_URL}/api/tds-system/sysTemplate/dataView"

# Headers
DEFAULT_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "clienttype": "1",
    "content-type": "application/json;charset=UTF-8",
    "language": "chinese",
    "origin": API_BASE_URL,
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": f"{API_BASE_URL}/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

# Login credentials
LOGIN_DATA = {
    "password": "mmz37TnJyKJ7My9F11Ote6Vh69iqAUhlHcbyjX6oz0qW9fC1NpjwTWzHS4HhuCOEIcnrznI2RNnNnJdEFIXUcMeYGIEk0Y9axJ7N7iZzWCCoxe3nCC2YtFBDqJdP2lRhNfOsK3Gd3eB3YEVranjKN47w31OjKkxUE8Yl0VtpVJ8=",
    "account": "admin",
    "suitRange": 1
}

# API Request Data
ORGANIZATION_INFO_DATA = {
    "type": 6,
    "belongId": 1,
    "module": "tissueAnalysis",
    "suitRange": 1
}


# 新增的接口配置
NEW_API_ENDPOINT = f"{API_BASE_URL}/api/new-endpoint"
NEW_API_REQUEST_DATA = {
    "key": "value",
}

# 数据库查询配置
DB_QUERY_CONFIG = {
    "host": "121.40.48.62",
    "port": 3308,
    "database": "tds_standard",
    "user": "test",
    "password": "Talebase.Test01"
}
