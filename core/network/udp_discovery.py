import socket
import threading
import json
import time
from datetime import datetime

class UDPServer:
    def __init__(self, device_info, port=5000):
        self.device_info = device_info
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = False
        self.broadcast_thread = None
        self.listen_thread = None
        
    def start(self):
        self.running = True
        self.listen_thread = threading.Thread(target=self._listen)
        self.broadcast_thread = threading.Thread(target=self._broadcast)
        self.listen_thread.daemon = True
        self.broadcast_thread.daemon = True
        self.listen_thread.start()
        self.broadcast_thread.start()
        
    def stop(self):
        self.running = False
        if self.listen_thread:
            self.listen_thread.join(1)
        if self.broadcast_thread:
            self.broadcast_thread.join(1)
        self.sock.close()
        
    def _listen(self):
        self.sock.bind(('', self.port))
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = json.loads(data.decode('utf-8'))
                if message['type'] == 'discovery_request' and addr[0] != self.device_info['ip']:
                    # 回复发现请求
                    response = {
                        'type': 'discovery_response',
                        'device_info': self.device_info,
                        'timestamp': datetime.now().isoformat()
                    }
                    self.sock.sendto(json.dumps(response).encode('utf-8'), addr)
                elif message['type'] == 'discovery_response':
                    # 处理其他设备的响应
                    self._handle_device_response(message['device_info'], addr[0])
            except Exception as e:
                if self.running:
                    print(f"UDP listen error: {e}")
                continue
    
    def _broadcast(self):
        while self.running:
            try:
                request = {
                    'type': 'discovery_request',
                    'device_info': self.device_info,
                    'timestamp': datetime.now().isoformat()
                }
                self.sock.sendto(json.dumps(request).encode('utf-8'), ('<broadcast>', self.port))
                time.sleep(5)  # 每5秒发送一次广播
            except Exception as e:
                if self.running:
                    print(f"UDP broadcast error: {e}")
                continue
    
    def _handle_device_response(self, device_info, ip):
        """处理其他设备的响应，需要被子类重写"""
        pass

class UDPClient:
    def __init__(self, device_info, port=5000):
        self.device_info = device_info
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = False
        self.listen_thread = None
        self.devices = {}
        
    def start(self):
        self.running = True
        self.listen_thread = threading.Thread(target=self._listen)
        self.listen_thread.daemon = True
        self.listen_thread.start()
        self.discover()
        
    def stop(self):
        self.running = False
        if self.listen_thread:
            self.listen_thread.join(1)
        self.sock.close()
        
    def discover(self):
        """主动发送发现请求"""
        request = {
            'type': 'discovery_request',
            'device_info': self.device_info,
            'timestamp': datetime.now().isoformat()
        }
        self.sock.sendto(json.dumps(request).encode('utf-8'), ('<broadcast>', self.port))
        
    def _listen(self):
        self.sock.bind(('', self.port))
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = json.loads(data.decode('utf-8'))
                if message['type'] == 'discovery_request' and addr[0] != self.device_info['ip']:
                    # 回复发现请求
                    response = {
                        'type': 'discovery_response',
                        'device_info': self.device_info,
                        'timestamp': datetime.now().isoformat()
                    }
                    self.sock.sendto(json.dumps(response).encode('utf-8'), addr)
                elif message['type'] == 'discovery_response':
                    # 添加设备到列表
                    device_info = message['device_info']
                    device_info['ip'] = addr[0]
                    device_info['last_seen'] = datetime.now().isoformat()
                    self.devices[device_info['id']] = device_info
            except Exception as e:
                if self.running:
                    print(f"UDP client listen error: {e}")
                continue
    
    def get_devices(self):
        """获取发现的设备列表"""
        # 移除超过30秒未更新的设备
        now = datetime.now()
        for device_id, device in list(self.devices.items()):
            last_seen = datetime.fromisoformat(device['last_seen'])
            if (now - last_seen).total_seconds() > 30:
                del self.devices[device_id]
        return list(self.devices.values())
