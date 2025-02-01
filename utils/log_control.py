"""
@Project ：tds_dev 
@File    ：log_control.py
@IDE     ：PyCharm 
@Author  ：靓仔
@Date    ：2025/1/21 0021 20:46 
"""
"""
@Project ：utils 
@File    ：log_control.py
@IDE     ：PyCharm 
@Author  ：靓仔
@Date    ：2025/1/3 0003 16:21 
"""

import logging
import colorlog
import time
import os
from logging.handlers import RotatingFileHandler


def ensure_path_sep(path):
    return path.replace('\\', '/')


class LogHandler:
    """日志处理器类"""

    def __init__(self, name, level=logging.INFO):  # 修改默认级别为 INFO
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 如果已经有处理器，不再添加
        if not self.logger.handlers:
            # 创建日志目录
            log_dir = 'logs'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # 文件处理器
            file_handler = RotatingFileHandler(
                filename=f'{log_dir}/{name}.log',
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(level)

            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)

            # 彩色日志格式
            colors = {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }

            # 格式化器
            console_formatter = colorlog.ColoredFormatter(
                '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s',
                log_colors=colors
            )

            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

            file_handler.setFormatter(file_formatter)
            console_handler.setFormatter(console_formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)


now_time_day = time.strftime("%Y-%m-%d", time.localtime())
ERROR = LogHandler('error', logging.ERROR)  # 只记录错误
INFO = LogHandler('info', logging.INFO)  # 修改为 INFO 级别
WARNING = LogHandler('warning', logging.WARNING)

if __name__ == '__main__':
    ERROR.logger.error("666666")
    INFO.logger.info("Some info message")
    WARNING.logger.warning("Some warning message")

    print(now_time_day)
