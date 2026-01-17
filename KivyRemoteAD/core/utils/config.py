import json
import os
from .logger import logger

class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.expanduser('~/.remote_control')
        self.config_file = os.path.join(self.config_dir, 'config.json')
        self.default_config = {
            'network': {
                'udp_port': 5000,
                'tcp_port': 5001,
                'discovery_interval': 5
            },
            'remote_desktop': {
                'fps': 30,
                'quality': 80,
                'compression': 'jpeg'
            },
            'file_transfer': {
                'chunk_size': 4096,
                'max_threads': 4
            },
            'security': {
                'encryption': True,
                'require_pairing': True
            }
        }
        self.config = self._load_config()
        
    def _load_config(self):
        """加载配置文件"""
        # 如果配置目录不存在，创建它
        os.makedirs(self.config_dir, exist_ok=True)
        
        # 如果配置文件不存在，创建默认配置
        if not os.path.exists(self.config_file):
            self._save_config(self.default_config)
            return self.default_config
        
        # 尝试加载配置文件
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 合并默认配置和用户配置
                return self._merge_configs(self.default_config, config)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            # 加载失败，使用默认配置
            return self.default_config
            
    def _save_config(self, config):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            logger.info(f"Config saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            
    def _merge_configs(self, default, user):
        """合并默认配置和用户配置"""
        if not isinstance(user, dict):
            return default
        
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # 递归合并字典
                result[key] = self._merge_configs(result[key], value)
            else:
                # 使用用户配置值
                result[key] = value
        
        return result
        
    def get(self, key_path, default=None):
        """获取配置值
        
        Args:
            key_path: 配置键路径，使用点分隔，例如 'network.udp_port'
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except KeyError:
            logger.warning(f"Config key '{key_path}' not found, using default: {default}")
            return default
        
    def set(self, key_path, value):
        """设置配置值
        
        Args:
            key_path: 配置键路径，使用点分隔，例如 'network.udp_port'
            value: 配置值
        """
        keys = key_path.split('.')
        config = self.config
        
        # 遍历到最后一个键的父级
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # 设置值
        config[keys[-1]] = value
        
        # 保存配置
        self._save_config(self.config)
        
    def reset(self):
        """重置配置为默认值"""
        self.config = self.default_config.copy()
        self._save_config(self.config)
        logger.info("Config reset to default")
        
    def get_all(self):
        """获取所有配置"""
        return self.config

# 创建全局配置实例
config_manager = ConfigManager()
