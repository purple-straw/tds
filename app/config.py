SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/dbname?charset=utf8mb4'
SQLALCHEMY_POOL_SIZE = 10  # 连接池大小
SQLALCHEMY_POOL_TIMEOUT = 30  # 连接超时时间（秒）
SQLALCHEMY_POOL_RECYCLE = 1800  # 连接回收时间（秒）
SQLALCHEMY_MAX_OVERFLOW = 20  # 最大溢出连接数 