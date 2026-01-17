import socket
import threading
import json
import time

class TCPClient:
    def __init__(self):
        self.socket = None
        self.server_address = None
        self.running = False
        self.receive_thread = None
        self.handlers = {}
        self.connected = False
        self.reconnect_timer = None
        self.reconnect_interval = 5  # 重连间隔（秒）
        
    def connect(self, server_ip, server_port):
        self.server_address = (server_ip, server_port)
        self.running = True
        self._connect()
        
    def _connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect(self.server_address)
            self.connected = True
            self.receive_thread = threading.Thread(target=self._receive)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            print(f"Connected to {self.server_address[0]}:{self.server_address[1]}")
        except Exception as e:
            print(f"Failed to connect to {self.server_address[0]}:{self.server_address[1]}: {e}")
            self.connected = False
            self._schedule_reconnect()
        
    def _schedule_reconnect(self):
        if self.running and not self.connected:
            self.reconnect_timer = threading.Timer(self.reconnect_interval, self._connect)
            self.reconnect_timer.daemon = True
            self.reconnect_timer.start()
            
    def disconnect(self):
        self.running = False
        self.connected = False
        if self.reconnect_timer:
            self.reconnect_timer.cancel()
        if self.receive_thread:
            self.receive_thread.join(1)
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
            
    def _receive(self):
        while self.running and self.connected:
            try:
                # 接收消息头部
                header = self.socket.recv(1024).decode('utf-8')
                if not header:
                    break
                    
                # 解析消息头部
                header_data = json.loads(header)
                message_type = header_data['type']
                data_length = header_data.get('length', 0)
                
                # 接收消息数据
                data = b''
                while len(data) < data_length:
                    packet = self.socket.recv(min(4096, data_length - len(data)))
                    if not packet:
                        break
                    data += packet
                
                if len(data) < data_length:
                    break
                    
                # 处理消息
                self._process_message(message_type, data)
                
            except Exception as e:
                print(f"TCP client receive error: {e}")
                break
        
        self.connected = False
        if self.running:
            self._schedule_reconnect()
            
    def _process_message(self, message_type, data):
        if message_type in self.handlers:
            try:
                self.handlers[message_type](data)
            except Exception as e:
                print(f"Handler error for {message_type}: {e}")
        
    def register_handler(self, message_type, handler):
        self.handlers[message_type] = handler
        
    def unregister_handler(self, message_type):
        if message_type in self.handlers:
            del self.handlers[message_type]
            
    def send_message(self, message_type, data=b''):
        if not self.connected or not self.socket:
            return False
            
        try:
            # 构建消息头部
            header = {
                'type': message_type,
                'length': len(data),
                'timestamp': time.time()
            }
            header_bytes = json.dumps(header).encode('utf-8')
            
            # 发送消息头部和数据
            self.socket.sendall(header_bytes + b'\n' + data)
            return True
        except Exception as e:
            print(f"Send message error: {e}")
            self.connected = False
            if self.running:
                self._schedule_reconnect()
            return False
            
    def is_connected(self):
        return self.connected
