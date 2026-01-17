import threading
import time
from ..network.encryption import encryption_manager

class PairingManager:
    def __init__(self, device_manager):
        self.device_manager = device_manager
        self.pairing_codes = {}
        self.pairing_requests = {}
        self.lock = threading.Lock()
        
    def generate_pairing_code(self, device_id):
        """生成配对码"""
        with self.lock:
            # 生成6位数字配对码
            pairing_code = encryption_manager.generate_pairing_code()
            # 配对码有效期为60秒
            expiry_time = time.time() + 60
            self.pairing_codes[device_id] = {
                'code': pairing_code,
                'expiry_time': expiry_time
            }
            return pairing_code
            
    def validate_pairing_code(self, device_id, pairing_code):
        """验证配对码"""
        with self.lock:
            if device_id not in self.pairing_codes:
                return False
            
            pairing_info = self.pairing_codes[device_id]
            # 检查配对码是否过期
            if time.time() > pairing_info['expiry_time']:
                del self.pairing_codes[device_id]
                return False
            
            # 检查配对码是否匹配
            if pairing_info['code'] == pairing_code:
                # 配对成功，移除配对码
                del self.pairing_codes[device_id]
                return True
            
            return False
            
    def send_pairing_request(self, device, tcp_client):
        """发送配对请求"""
        # 生成配对码
        pairing_code = self.generate_pairing_code(device['id'])
        
        # 构建配对请求消息
        pairing_request = {
            'device_id': self.device_manager.get_local_device()['id'],
            'device_name': self.device_manager.get_local_device()['name'],
            'pairing_code': pairing_code,
            'timestamp': time.time()
        }
        
        # 发送配对请求
        tcp_client.send_message('pairing_request', str(pairing_request).encode('utf-8'))
        return pairing_code
        
    def handle_pairing_request(self, request_data):
        """处理配对请求"""
        # 解析配对请求
        request = eval(request_data.decode('utf-8'))
        device_id = request['device_id']
        device_name = request['device_name']
        pairing_code = request['pairing_code']
        
        # 保存配对请求
        with self.lock:
            self.pairing_requests[device_id] = {
                'device_name': device_name,
                'pairing_code': pairing_code,
                'timestamp': time.time()
            }
        
        return device_id, device_name, pairing_code
        
    def accept_pairing_request(self, device_id, tcp_client):
        """接受配对请求"""
        with self.lock:
            if device_id not in self.pairing_requests:
                return False
            
            pairing_info = self.pairing_requests[device_id]
            pairing_code = pairing_info['pairing_code']
            
        # 构建配对响应
        pairing_response = {
            'status': 'accepted',
            'device_id': self.device_manager.get_local_device()['id'],
            'device_name': self.device_manager.get_local_device()['name'],
            'pairing_code': pairing_code,
            'timestamp': time.time()
        }
        
        # 发送配对响应
        tcp_client.send_message('pairing_response', str(pairing_response).encode('utf-8'))
        
        # 添加到已配对设备列表
        device = self.device_manager.get_device_by_id(device_id)
        if device:
            self.device_manager.add_paired_device(device)
        
        return True
        
    def reject_pairing_request(self, device_id, tcp_client):
        """拒绝配对请求"""
        # 构建配对响应
        pairing_response = {
            'status': 'rejected',
            'device_id': self.device_manager.get_local_device()['id'],
            'device_name': self.device_manager.get_local_device()['name'],
            'timestamp': time.time()
        }
        
        # 发送配对响应
        tcp_client.send_message('pairing_response', str(pairing_response).encode('utf-8'))
        
        with self.lock:
            if device_id in self.pairing_requests:
                del self.pairing_requests[device_id]
        
        return True
        
    def handle_pairing_response(self, response_data):
        """处理配对响应"""
        # 解析配对响应
        response = eval(response_data.decode('utf-8'))
        status = response['status']
        device_id = response['device_id']
        device_name = response['device_name']
        
        if status == 'accepted':
            # 配对成功，添加到已配对设备列表
            device = self.device_manager.get_device_by_id(device_id)
            if device:
                self.device_manager.add_paired_device(device)
            return True, device_name
        else:
            # 配对失败
            return False, device_name
            
    def cleanup_expired_pairing_codes(self):
        """清理过期的配对码"""
        with self.lock:
            now = time.time()
            for device_id, pairing_info in list(self.pairing_codes.items()):
                if now > pairing_info['expiry_time']:
                    del self.pairing_codes[device_id]
            
            # 清理过期的配对请求（120秒后过期）
            for device_id, request_info in list(self.pairing_requests.items()):
                if now > request_info['timestamp'] + 120:
                    del self.pairing_requests[device_id]
