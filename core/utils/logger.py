import logging
import os
import time

class Logger:
    def __init__(self, name='remote_control', log_dir=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 如果没有提供日志目录，使用默认目录
        if not log_dir:
            log_dir = os.path.expanduser('~/.remote_control/logs')
        
        # 创建日志目录
        os.makedirs(log_dir, exist_ok=True)
        
        # 创建日志文件名
        log_file = os.path.join(log_dir, f'{name}_{time.strftime("%Y-%m-%d")}.log')
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            # 创建文件处理器
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            # 创建控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # 创建日志格式
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # 添加处理器
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
            
    def get_logger(self):
        """获取logger实例"""
        return self.logger

# 创建全局logger实例
logger = Logger().get_logger()
