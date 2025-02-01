from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import time
import logging
import threading
import sqlalchemy.exc

# 创建日志记录器
logger = logging.getLogger(__name__)

# 创建基础模型类
Base = declarative_base()

class Database:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self, app=None):
        if not hasattr(self, 'initialized'):
            self.engine = None
            self.session_factory = None
            self.app = app
            self.Model = Base
            self._session = {}  # 用于存储线程本地会话
            self.initialized = True
            
            if app is not None:
                self.init_app(app)

    def init_app(self, app):
        """初始化数据库"""
        try:
            # 配置数据库连接
            self.engine = create_engine(
                app.config['SQLALCHEMY_DATABASE_URI'],
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=2,
                pool_timeout=30,
                pool_recycle=300,
                pool_pre_ping=True,
                echo=app.config.get('SQLALCHEMY_ECHO', False),
                # 添加连接参数
                connect_args={
                    'connect_timeout': 10,
                    'read_timeout': 30,
                    'write_timeout': 30,
                    'client_flag': 2,
                    'autocommit': False,
                    'charset': 'utf8mb4',
                    'use_unicode': True,
                    'sql_mode': 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION',
                    'program_name': 'TDS_APP'  # 添加应用标识
                }
            )

            # 配置连接池事件
            @event.listens_for(self.engine, 'checkout')
            def ping_connection(dbapi_connection, connection_record, connection_proxy):
                try:
                    # 使用简单的SELECT 1检查连接
                    dbapi_connection.ping(reconnect=True)
                except Exception:
                    # 如果检查失败，尝试重新连接
                    if connection_proxy is not None:
                        connection_proxy._pool.dispose()
                    raise

            # 添加连接创建事件监听
            @event.listens_for(self.engine, 'connect')
            def on_connect(dbapi_connection, connection_record):
                try:
                    # 设置会话变量
                    cursor = dbapi_connection.cursor()
                    cursor.execute("SET SESSION sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'")
                    cursor.execute("SET SESSION wait_timeout=300")
                    cursor.execute("SET SESSION interactive_timeout=300")
                    cursor.close()
                except Exception as e:
                    logger.error(f"设置会话变量失败: {str(e)}")
                    raise

            # 创建会话工厂
            self.session_factory = sessionmaker(
                bind=self.engine,
                expire_on_commit=False,
                autocommit=False,
                autoflush=True
            )
            
            # 创建数据库表
            Base.metadata.create_all(self.engine)
            
            # 注册清理函数
            app.teardown_appcontext(self.cleanup)
            
        except Exception as e:
            logger.error(f"数据库初始化失败: {str(e)}")
            raise

    def get_session(self):
        """获取当前线程的会话"""
        thread_id = threading.get_ident()
        if thread_id not in self._session:
            self._session[thread_id] = scoped_session(self.session_factory)
        return self._session[thread_id]

    @contextmanager
    def session_scope(self):
        """提供事务作用域的会话上下文"""
        session = self.get_session()
        try:
            yield session
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                raise
        except Exception as e:
            try:
                session.rollback()
            except:
                pass
            logger.error(f"数据库操作失败: {str(e)}")
            raise
        finally:
            try:
                session.close()
            except:
                pass
            
            thread_id = threading.get_ident()
            if thread_id in self._session:
                try:
                    self._session[thread_id].remove()
                    del self._session[thread_id]
                except:
                    pass

    def execute_with_retry(self, operation, max_retries=3, delay=0.5):
        """执行数据库操作，带重试机制"""
        last_error = None
        for attempt in range(max_retries):
            try:
                with self.session_scope() as session:
                    try:
                        result = operation(session)
                        return result
                    except Exception as e:
                        if isinstance(e, (sqlalchemy.exc.OperationalError, sqlalchemy.exc.InternalError)):
                            # 对于连接相关的错误，重置连接
                            if hasattr(session, 'bind'):
                                session.bind.dispose()
                            raise  # 抛出异常以触发重试
                        raise
            except Exception as e:
                last_error = e
                logger.warning(f"数据库操作失败，尝试重试 ({attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(delay * (2 ** attempt))  # 指数退避
                    continue
                logger.error(f"数据库操作最终失败: {str(e)}")
                raise last_error

    def cleanup(self, exception=None):
        """清理数据库连接"""
        thread_id = threading.get_ident()
        if thread_id in self._session:
            try:
                session = self._session[thread_id]
                # 先尝试回滚任何未完成的事务
                try:
                    session.rollback()
                except:
                    pass
                
                # 移除session
                try:
                    session.remove()
                except:
                    pass
                
                del self._session[thread_id]
            except:
                pass
        
        if self.engine:
            try:
                # 使用dispose而不是直接关闭连接
                self.engine.dispose()
            except:
                pass

# 创建全局数据库实例
db = Database() 