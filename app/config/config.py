class Config:
    DEBUG = True
    # 其他配置项...

    # 数据库配置
    SQLALCHEMY_POOL_SIZE = 5
    SQLALCHEMY_MAX_OVERFLOW = 10
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 1800
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 1800
    }

class DevelopmentConfig(Config):
    DEBUG = True
    # 开发环境特定配置...

    # 数据库配置
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123456'
    MYSQL_DB = 'tds_standard'

    # API配置
    API_BASE_URL = 'https://test-tds-standard.cepin.com'
    API_USERNAME = 'admin'
    API_PASSWORD = '123456'
    
    # 其他配置
    SECRET_KEY = 'dev'
    CORS_HEADERS = 'Content-Type'

class ProductionConfig(Config):
    DEBUG = False
    # 生产环境特定配置... 

    # 数据库配置
    MYSQL_HOST = 'production_host'
    MYSQL_PORT = 3306
    MYSQL_USER = 'production_user'
    MYSQL_PASSWORD = 'production_password'
    MYSQL_DB = 'tds'
    
    # API配置
    API_BASE_URL = 'https://tds-standard.cepin.com'
    API_USERNAME = 'production_user'
    API_PASSWORD = 'production_password'
    
    # 其他配置
    SECRET_KEY = 'production_key'
    CORS_HEADERS = 'Content-Type'

class TestingConfig:
    """测试环境配置"""
    TESTING = True
    DEBUG = True
    
    # 数据库配置
    MYSQL_HOST = 'test_host'
    MYSQL_PORT = 3306
    MYSQL_USER = 'test_user'
    MYSQL_PASSWORD = 'test_password'
    MYSQL_DB = 'tds_test'
    
    # API配置
    API_BASE_URL = 'https://test-tds-standard.cepin.com'
    API_USERNAME = 'test_user'
    API_PASSWORD = 'test_password'
    
    # 其他配置
    SECRET_KEY = 'test_key'
    CORS_HEADERS = 'Content-Type' 