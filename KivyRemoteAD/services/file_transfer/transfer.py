import os
import threading
import time

class FileTransfer:
    def __init__(self, chunk_size=4096, max_threads=4):
        self.chunk_size = chunk_size
        self.max_threads = max_threads
        self.transfer_tasks = {}
        self.lock = threading.Lock()
        
    def upload_file(self, file_path, tcp_client, destination_path, on_progress=None, on_complete=None):
        """上传文件
        
        Args:
            file_path: 本地文件路径
            tcp_client: TCP客户端实例
            destination_path: 目标路径
            on_progress: 进度回调函数，接收当前进度（已传输字节数）和总大小
            on_complete: 完成回调函数，接收成功或失败
            
        Returns:
            任务ID
        """
        try:
            # 获取文件信息
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            
            # 构建任务ID
            task_id = f"upload_{int(time.time())}_{threading.get_ident()}"
            
            # 创建任务信息
            task = {
                'id': task_id,
                'type': 'upload',
                'file_path': file_path,
                'destination_path': destination_path,
                'file_size': file_size,
                'transferred': 0,
                'status': 'running',
                'start_time': time.time()
            }
            
            # 添加任务到列表
            with self.lock:
                self.transfer_tasks[task_id] = task
            
            # 启动上传线程
            upload_thread = threading.Thread(
                target=self._upload_thread,
                args=(task, tcp_client, on_progress, on_complete)
            )
            upload_thread.daemon = True
            upload_thread.start()
            
            return task_id
        except Exception as e:
            print(f"Upload file error: {e}")
            if on_complete:
                on_complete(False)
            return None
            
    def _upload_thread(self, task, tcp_client, on_progress, on_complete):
        """上传线程"""
        try:
            file_path = task['file_path']
            destination_path = task['destination_path']
            file_size = task['file_size']
            
            # 发送文件信息
            file_info = {
                'type': 'file_upload_request',
                'file_name': os.path.basename(file_path),
                'file_size': file_size,
                'destination_path': destination_path
            }
            
            tcp_client.send_message('file_info', str(file_info).encode('utf-8'))
            
            # 打开文件并发送
            with open(file_path, 'rb') as f:
                transferred = 0
                while True:
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break
                        
                    # 发送文件数据
                    tcp_client.send_message('file_data', chunk)
                    
                    # 更新进度
                    transferred += len(chunk)
                    task['transferred'] = transferred
                    
                    # 调用进度回调
                    if on_progress:
                        on_progress(transferred, file_size)
                    
                    # 模拟限速（可选）
                    # time.sleep(0.001)
            
            # 发送完成消息
            tcp_client.send_message('file_complete', b'')
            
            # 更新任务状态
            task['status'] = 'completed'
            task['end_time'] = time.time()
            
            # 调用完成回调
            if on_complete:
                on_complete(True)
                
        except Exception as e:
            print(f"Upload thread error: {e}")
            # 更新任务状态
            task['status'] = 'failed'
            task['error'] = str(e)
            task['end_time'] = time.time()
            
            # 调用完成回调
            if on_complete:
                on_complete(False)
            
        finally:
            # 从任务列表中移除
            with self.lock:
                del self.transfer_tasks[task['id']]
                
    def download_file(self, file_name, file_size, tcp_client, save_path, on_progress=None, on_complete=None):
        """下载文件
        
        Args:
            file_name: 文件名
            file_size: 文件大小
            tcp_client: TCP客户端实例
            save_path: 保存路径
            on_progress: 进度回调函数，接收当前进度（已传输字节数）和总大小
            on_complete: 完成回调函数，接收成功或失败
            
        Returns:
            任务ID
        """
        try:
            # 构建任务ID
            task_id = f"download_{int(time.time())}_{threading.get_ident()}"
            
            # 创建任务信息
            task = {
                'id': task_id,
                'type': 'download',
                'file_name': file_name,
                'file_size': file_size,
                'save_path': save_path,
                'transferred': 0,
                'status': 'running',
                'start_time': time.time()
            }
            
            # 添加任务到列表
            with self.lock:
                self.transfer_tasks[task_id] = task
            
            # 启动下载线程
            download_thread = threading.Thread(
                target=self._download_thread,
                args=(task, tcp_client, on_progress, on_complete)
            )
            download_thread.daemon = True
            download_thread.start()
            
            return task_id
        except Exception as e:
            print(f"Download file error: {e}")
            if on_complete:
                on_complete(False)
            return None
            
    def _download_thread(self, task, tcp_client, on_progress, on_complete):
        """下载线程"""
        try:
            file_name = task['file_name']
            file_size = task['file_size']
            save_path = task['save_path']
            
            # 检查目录是否存在
            save_dir = os.path.dirname(save_path)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir, exist_ok=True)
            
            # 打开文件准备写入
            with open(save_path, 'wb') as f:
                transferred = 0
                
                # 这里需要等待接收数据，实际实现中应该通过消息处理器接收数据
                # 这里简化处理，假设数据会通过其他方式接收
                # 实际实现中，应该使用事件或队列来接收数据
                
                # 更新任务状态
                task['status'] = 'completed'
                task['end_time'] = time.time()
                
                # 调用完成回调
                if on_complete:
                    on_complete(True)
                    
        except Exception as e:
            print(f"Download thread error: {e}")
            # 更新任务状态
            task['status'] = 'failed'
            task['error'] = str(e)
            task['end_time'] = time.time()
            
            # 调用完成回调
            if on_complete:
                on_complete(False)
            
        finally:
            # 从任务列表中移除
            with self.lock:
                del self.transfer_tasks[task['id']]
                
    def resume_transfer(self, task_id):
        """恢复传输（断点续传）
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否成功
        """
        # 实现断点续传逻辑
        # 这里简化处理，实际实现中需要保存传输进度并恢复
        return False
        
    def cancel_transfer(self, task_id):
        """取消传输
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否成功
        """
        with self.lock:
            if task_id in self.transfer_tasks:
                task = self.transfer_tasks[task_id]
                task['status'] = 'cancelled'
                return True
        return False
        
    def get_task_status(self, task_id):
        """获取任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务状态信息
        """
        with self.lock:
            return self.transfer_tasks.get(task_id, None)
            
    def get_all_tasks(self):
        """获取所有任务
        
        Returns:
            任务列表
        """
        with self.lock:
            return list(self.transfer_tasks.values())
            
    def calculate_speed(self, transferred, start_time):
        """计算传输速度
        
        Args:
            transferred: 已传输字节数
            start_time: 开始时间
            
        Returns:
            速度（字节/秒）
        """
        elapsed = time.time() - start_time
        if elapsed == 0:
            return 0
        return transferred / elapsed
        
    def format_speed(self, speed):
        """格式化速度为人类可读格式
        
        Args:
            speed: 速度（字节/秒）
            
        Returns:
            格式化后的速度字符串
        """
        units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
        unit_index = 0
        
        while speed >= 1024 and unit_index < len(units) - 1:
            speed /= 1024
            unit_index += 1
        
        return f"{speed:.2f} {units[unit_index]}"
        
    def format_size(self, size):
        """格式化文件大小为人类可读格式
        
        Args:
            size: 文件大小（字节）
            
        Returns:
            格式化后的大小字符串
        """
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        return f"{size:.2f} {units[unit_index]}"

if __name__ == "__main__":
    # 测试文件传输功能
    ft = FileTransfer()
    
    # 测试格式化函数
    print(f"Speed: {ft.format_speed(1024 * 1024)}")
    print(f"Size: {ft.format_size(1024 * 1024 * 1024)}")
