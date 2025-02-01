"""
数据库工具模块
"""
from sqlalchemy import create_engine, text as sa_text
from sqlalchemy.pool import QueuePool
from app.config.config import DevelopmentConfig
from app.utils.log_control import INFO, ERROR
import time
import urllib.parse


class DatabaseConnection:
    # 创建数据库引擎
    password = urllib.parse.quote_plus(DevelopmentConfig.MYSQL_PASSWORD)  # 处理特殊字符
    engine = create_engine(
        f'mysql+pymysql://{DevelopmentConfig.MYSQL_USER}:{password}'
        f'@{DevelopmentConfig.MYSQL_HOST}:{DevelopmentConfig.MYSQL_PORT}/{DevelopmentConfig.MYSQL_DB}',
        pool_size=5,  # 减小连接池大小，避免过多连接
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=300,  # 缩短连接回收时间到5分钟
        pool_pre_ping=True,
        echo=False,
        future=True,  # 使用新的 SQLAlchemy 2.0 API
        connect_args={
            'connect_timeout': 60,
            'read_timeout': 60,
            'write_timeout': 60,
            'program_name': 'TDS_APP',
            'charset': 'utf8mb4',
            'autocommit': False,
            'client_flag': 2,
            'ssl': None  # 禁用SSL
        }
    )

    def __init__(self):
        self.connection = None
        self._in_transaction = False

    def connect(self):
        """获取数据库连接"""
        retry_count = 3
        retry_delay = 0.5
        last_error = None

        while retry_count > 0:
            try:
                if self.connection is not None:
                    try:
                        if not self.connection.closed:
                            self.connection.close()
                    except Exception as e:
                        INFO.logger.warning(f"关闭旧连接时出现警告: {str(e)}")

                self.connection = self.engine.connect()
                self._in_transaction = False
                
                # 使用事务执行会话设置
                with self.connection.begin():
                    self.connection.execute(sa_text("SET SESSION wait_timeout=300"))
                    self.connection.execute(sa_text("SET SESSION interactive_timeout=300"))
                    self.connection.execute(sa_text("SET SESSION sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'"))
                
                INFO.logger.info("获取数据库连接成功")
                return
            except Exception as e:
                last_error = e
                retry_count -= 1
                if retry_count > 0:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    ERROR.logger.error(f"获取数据库连接失败: {str(e)}")
                    raise last_error

    def close(self):
        """关闭数据库连接"""
        if self.connection is not None:
            try:
                if not self.connection.closed:
                    # 如果在事务中，尝试回滚
                    if self._in_transaction:
                        try:
                            self.connection.rollback()
                        except:
                            pass
                    self.connection.close()
                    INFO.logger.info("数据库连接已关闭")
            except Exception as e:
                ERROR.logger.error(f"关闭数据库连接失败: {str(e)}")
            finally:
                self.connection = None
                self._in_transaction = False

    def execute(self, sql, params=None):
        """执行更新SQL"""
        retry_count = 3
        retry_delay = 0.5
        last_error = None

        while retry_count > 0:
            try:
                self.connect()
                
                # 确保 SQL 是 text 对象
                if isinstance(sql, str):
                    sql = sa_text(sql)
                
                # 使用显式事务
                trans = self.connection.begin()
                try:
                    self._in_transaction = True
                    result = self.connection.execute(sql, params or {})
                    trans.commit()
                    INFO.logger.info(f"SQL执行成功: {sql}")
                    return result.rowcount
                except:
                    trans.rollback()
                    raise
                finally:
                    self._in_transaction = False
            except Exception as e:
                last_error = e
                retry_count -= 1
                if retry_count > 0:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                ERROR.logger.error(f"SQL执行失败: {str(e)}, SQL: {sql}")
                raise last_error
            finally:
                self.close()

    def execute_query(self, sql, params=None):
        """执行查询SQL"""
        start_time = time.time()
        retry_count = 3
        retry_delay = 0.5
        last_error = None

        while retry_count > 0:
            try:
                self.connect()
                
                # 确保 SQL 是 text 对象
                if isinstance(sql, str):
                    sql = sa_text(sql)
                
                # 查询不需要事务，但使用 with 语句确保资源正确释放
                with self.connection.begin():
                    self._in_transaction = True
                    result = self.connection.execute(sql, params or {})
                    rows = result.fetchall()
                    data = [dict(row._mapping) for row in rows]
                    
                    query_time = round((time.time() - start_time) * 1000)
                    INFO.logger.info(f"SQL执行成功: {sql}")
                    return {
                        'data': data,
                        'query_time': query_time
                    }
            except Exception as e:
                last_error = e
                retry_count -= 1
                if retry_count > 0:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                ERROR.logger.error(f"SQL执行失败: {str(e)}, SQL: {sql}")
                raise last_error
            finally:
                self._in_transaction = False
                self.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                # 如果发生异常，记录错误并确保回滚
                ERROR.logger.error(f"数据库操作出错: {str(exc_val)}")
                if self._in_transaction and self.connection and not self.connection.closed:
                    try:
                        self.connection.rollback()
                    except:
                        pass
        finally:
            self.close()

