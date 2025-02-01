"""
@Project ：tds_dev 
@File    ：log_control.py
@IDE     ：PyCharm 
@Author  ：靓仔
@Date    ：2025/1/21
"""

import logging
import colorlog
import time
import os
from logging.handlers import RotatingFileHandler


class LogHandler:
    """日志处理器类"""
    
    # 日志颜色配置
    LOG_COLORS = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
    
    # 日志格式
    LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
    COLOR_FORMAT = '%(log_color)s' + LOG_FORMAT + '%(reset)s'
    
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            self._setup_handlers(name, level)
    
    def _setup_handlers(self, name, level):
        """设置日志处理器"""
        # 创建日志目录
        log_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 设置日志文件路径
        log_file = os.path.join(log_dir, f'{name}.log')
        
        # 创建并配置文件处理器
        file_handler = self._create_file_handler(log_file, level)
        
        # 创建并配置控制台处理器
        console_handler = self._create_console_handler(level)
        
        # 添加处理器到logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _create_file_handler(self, log_file, level):
        """创建文件处理器"""
        handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(
            self.LOG_FORMAT,
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        return handler
    
    def _create_console_handler(self, level):
        """创建控制台处理器"""
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(colorlog.ColoredFormatter(
            self.COLOR_FORMAT,
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors=self.LOG_COLORS
        ))
        return handler


# 创建日志实例
INFO = LogHandler('info')
ERROR = LogHandler('error', logging.ERROR)
WARNING = LogHandler('warning', logging.WARNING)


if __name__ == '__main__':
    # 测试日志输出
    INFO.logger.info("这是一条信息日志")
    WARNING.logger.warning("这是一条警告日志")
    ERROR.logger.error("这是一条错误日志") 