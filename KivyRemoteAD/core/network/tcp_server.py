import socket
import threading
import json
import time

class TCPServer:
    def __init__(self, port=5001):
        self.port = port
        self.server_socket = None
        self.clients = {}
        self.running = False
        self.listen_thread = None
        self.handlers = {}
        
    def start(self):
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('', self.port))
        self.server_socket.listen(5)
        self.listen_thread = threading.Thread(target=self._listen)
        self.listen_thread.daemon = True
        self.listen_thread.start()
        
    def stop(self):
        self.running = False
        if self.listen_thread:
            self.listen_thread.join(1)
        for client_id, client in list(self.clients.items()):
            self._close_client(client_id)
        if self.server_socket:
            self.server_socket.close()
        
    def _listen(self):
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                if self.running:
                    print(f"TCP server listen error: {e}")
                break
        
    def _handle_client(self, client_socket, client_address):
        client_id = f"{client_address[0]}:{client_address[1]}"
        self.clients[client_id] = {
            'socket': client_socket,
            'address': client_address,
            'last_active': time.time()
        }
        
        try:
            while self.running:
                # 接收消息头部
                header = client_socket.recv(1024).decode('utf-8')
                if not header:
                    break
                    
                # 解析消息头部
                header_data = json.loads(header)
                message_type = header_data['type']
                data_length = header_data.get('length', 0)
                
                # 接收消息数据
                data = b''
                while len(data) < data_length:
                    packet = client_socket.recv(min(4096, data_length - len(data)))
                    if not packet:
                        break
                    data += packet
                
                if len(data) < data_length:
                    break
                    
                # 处理消息
                self._process_message(message_type, data, client_id)
                self.clients[client_id]['last_active'] = time.time()
                
        except Exception as e:
            if self.running:
                print(f"TCP client {client_id} error: {e}")
        finally:
            self._close_client(client_id)
            
    def _close_client(self, client_id):
        if client_id in self.clients:
            try:
                self.clients[client_id]['socket'].close()
            except:
                pass
            del self.clients[client_id]
            
    def _process_message(self, message_type, data, client_id):
        if message_type in self.handlers:
            try:
                self.handlers[message_type](data, client_id)
            except Exception as e:
                print(f"Handler error for {message_type}: {e}")
        
    def register_handler(self, message_type, handler):
        self.handlers[message_type] = handler
        
    def unregister_handler(self, message_type):
        if message_type in self.handlers:
            del self.handlers[message_type]
            
    def send_message(self, client_id, message_type, data=b''):
        if client_id not in self.clients:
            return False
            
        try:
            client_socket = self.clients[client_id]['socket']
            # 构建消息头部
            header = {
                'type': message_type,
                'length': len(data),
                'timestamp': time.time()
            }
            header_bytes = json.dumps(header).encode('utf-8')
            
            # 发送消息头部和数据
            client_socket.sendall(header_bytes + b'\n' + data)
            self.clients[client_id]['last_active'] = time.time()
            return True
        except Exception as e:
            print(f"Send message error to {client_id}: {e}")
            self._close_client(client_id)
            return False
            
    def broadcast_message(self, message_type, data=b''):
        for client_id in list(self.clients.keys()):
            self.send_message(client_id, message_type, data)
            
    def get_clients(self):
        return list(self.clients.keys())
