import uuid
import platform
import socket
import json
import os
from datetime import datetime

class DeviceManager:
    def __init__(self):
        self.local_device = self._get_local_device_info()
        self.discovered_devices = {}
        self.paired_devices = self._load_paired_devices()
        
    def _get_local_device_info(self):
        """获取本地设备信息"""
        # 生成唯一设备ID
        device_id = self._get_device_id()
        
        # 获取设备名称
        device_name = platform.node()
        
        # 获取设备类型
        device_type = self._get_device_type()
        
        # 获取IP地址
        ip_address = self._get_ip_address()
        
        return {
            'id': device_id,
            'name': device_name,
            'type': device_type,
            'ip': ip_address,
            'platform': platform.system(),
            'version': platform.version(),
            'last_seen': datetime.now().isoformat()
        }
        
    def _get_device_id(self):
        """获取或生成设备唯一ID"""
        # 尝试从文件中读取设备ID
        config_dir = os.path.expanduser('~/.remote_control')
        device_id_file = os.path.join(config_dir, 'device_id.json')
        
        if os.path.exists(device_id_file):
            try:
                with open(device_id_file, 'r') as f:
                    data = json.load(f)
                    return data['device_id']
            except:
                pass
        
        # 生成新的设备ID
        device_id = str(uuid.uuid4())
        
        # 保存设备ID到文件
        os.makedirs(config_dir, exist_ok=True)
        with open(device_id_file, 'w') as f:
            json.dump({'device_id': device_id}, f)
        
        return device_id
        
    def _get_device_type(self):
        """获取设备类型"""
        system = platform.system()
        if system == 'Windows' or system == 'Darwin' or system == 'Linux':
            return 'desktop'
        elif system == 'Android' or system == 'iOS':
            return 'mobile'
        else:
            return 'unknown'
        
    def _get_ip_address(self):
        """获取本地IP地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except:
            return '127.0.0.1'
        
    def update_device_list(self, devices):
        """更新已发现设备列表"""
        for device in devices:
            device_id = device['id']
            # 跳过本地设备
            if device_id == self.local_device['id']:
                continue
            # 更新设备信息
            device['last_seen'] = datetime.now().isoformat()
            self.discovered_devices[device_id] = device
        
        # 移除超过30秒未更新的设备
        self._cleanup_old_devices()
        
    def _cleanup_old_devices(self):
        """清理旧设备"""
        now = datetime.now()
        for device_id, device in list(self.discovered_devices.items()):
            last_seen = datetime.fromisoformat(device['last_seen'])
            if (now - last_seen).total_seconds() > 30:
                del self.discovered_devices[device_id]
        
    def get_discovered_devices(self):
        """获取已发现设备列表"""
        self._cleanup_old_devices()
        return list(self.discovered_devices.values())
        
    def get_paired_devices(self):
        """获取已配对设备列表"""
        return list(self.paired_devices.values())
        
    def add_paired_device(self, device):
        """添加已配对设备"""
        device_id = device['id']
        self.paired_devices[device_id] = device
        self._save_paired_devices()
        
    def remove_paired_device(self, device_id):
        """移除已配对设备"""
        if device_id in self.paired_devices:
            del self.paired_devices[device_id]
            self._save_paired_devices()
        
    def is_paired(self, device_id):
        """检查设备是否已配对"""
        return device_id in self.paired_devices
        
    def _load_paired_devices(self):
        """加载已配对设备列表"""
        config_dir = os.path.expanduser('~/.remote_control')
        paired_devices_file = os.path.join(config_dir, 'paired_devices.json')
        
        if os.path.exists(paired_devices_file):
            try:
                with open(paired_devices_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {}
        
    def _save_paired_devices(self):
        """保存已配对设备列表"""
        config_dir = os.path.expanduser('~/.remote_control')
        paired_devices_file = os.path.join(config_dir, 'paired_devices.json')
        
        os.makedirs(config_dir, exist_ok=True)
        with open(paired_devices_file, 'w') as f:
            json.dump(self.paired_devices, f)
        
    def get_local_device(self):
        """获取本地设备信息"""
        return self.local_device
        
    def update_local_device_ip(self):
        """更新本地设备IP地址"""
        self.local_device['ip'] = self._get_ip_address()
        
    def get_device_by_id(self, device_id):
        """根据设备ID获取设备信息"""
        # 先检查已配对设备
        if device_id in self.paired_devices:
            return self.paired_devices[device_id]
        
        # 再检查已发现设备
        if device_id in self.discovered_devices:
            return self.discovered_devices[device_id]
        
        return None
