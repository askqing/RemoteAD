import os
import platform
import time
import json

class FileManager:
    def __init__(self):
        self.platform = platform.system()
        
    def get_file_list(self, path='.'):
        """获取文件列表
        
        Args:
            path: 目录路径
            
        Returns:
            文件列表，每个文件包含以下信息：
            - name: 文件名
            - path: 文件路径
            - size: 文件大小（字节）
            - is_dir: 是否为目录
            - modified: 最后修改时间
        """
        try:
            file_list = []
            # 获取绝对路径
            abs_path = os.path.abspath(path)
            
            # 遍历目录
            for item in os.listdir(abs_path):
                item_path = os.path.join(abs_path, item)
                item_stat = os.stat(item_path)
                
                file_list.append({
                    'name': item,
                    'path': item_path,
                    'size': item_stat.st_size,
                    'is_dir': os.path.isdir(item_path),
                    'modified': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item_stat.st_mtime))
                })
            
            # 按目录优先，然后按名称排序
            file_list.sort(key=lambda x: (not x['is_dir'], x['name']))
            return file_list
        except Exception as e:
            print(f"Get file list error: {e}")
            return []
            
    def get_file_info(self, path):
        """获取文件信息
        
        Args:
            path: 文件路径
            
        Returns:
            文件信息字典
        """
        try:
            abs_path = os.path.abspath(path)
            if not os.path.exists(abs_path):
                return None
                
            stat = os.stat(abs_path)
            return {
                'name': os.path.basename(abs_path),
                'path': abs_path,
                'size': stat.st_size,
                'is_dir': os.path.isdir(abs_path),
                'modified': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime))
            }
        except Exception as e:
            print(f"Get file info error: {e}")
            return None
            
    def create_directory(self, path):
        """创建目录
        
        Args:
            path: 目录路径
            
        Returns:
            是否成功
        """
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            print(f"Create directory error: {e}")
            return False
            
    def delete_file(self, path):
        """删除文件
        
        Args:
            path: 文件路径
            
        Returns:
            是否成功
        """
        try:
            if os.path.isdir(path):
                # 删除目录及其内容
                import shutil
                shutil.rmtree(path)
            else:
                # 删除文件
                os.remove(path)
            return True
        except Exception as e:
            print(f"Delete file error: {e}")
            return False
            
    def rename_file(self, old_path, new_path):
        """重命名文件
        
        Args:
            old_path: 原文件路径
            new_path: 新文件路径
            
        Returns:
            是否成功
        """
        try:
            os.rename(old_path, new_path)
            return True
        except Exception as e:
            print(f"Rename file error: {e}")
            return False
            
    def get_free_space(self, path='.'):
        """获取可用空间
        
        Args:
            path: 目录路径
            
        Returns:
            可用空间（字节）
        """
        try:
            if self.platform == 'Windows':
                import ctypes
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(path), None, None, ctypes.pointer(free_bytes))
                return free_bytes.value
            else:
                # Unix-like systems
                statvfs = os.statvfs(path)
                return statvfs.f_frsize * statvfs.f_bavail
        except Exception as e:
            print(f"Get free space error: {e}")
            return 0
            
    def get_home_directory(self):
        """获取用户主目录
        
        Returns:
            主目录路径
        """
        return os.path.expanduser('~')
        
    def get_desktop_directory(self):
        """获取桌面目录
        
        Returns:
            桌面目录路径
        """
        home = self.get_home_directory()
        if self.platform == 'Windows':
            return os.path.join(home, 'Desktop')
        elif self.platform == 'Darwin':
            return os.path.join(home, 'Desktop')
        else:
            # Linux
            return os.path.join(home, 'Desktop')
            
    def normalize_path(self, path):
        """标准化路径
        
        Args:
            path: 路径
            
        Returns:
            标准化后的路径
        """
        return os.path.normpath(path)
        
    def join_path(self, *paths):
        """连接路径
        
        Args:
            *paths: 路径片段
            
        Returns:
            连接后的路径
        """
        return os.path.join(*paths)
        
    def exists(self, path):
        """检查文件是否存在
        
        Args:
            path: 文件路径
            
        Returns:
            是否存在
        """
        return os.path.exists(path)
        
    def is_directory(self, path):
        """检查是否为目录
        
        Args:
            path: 文件路径
            
        Returns:
            是否为目录
        """
        return os.path.isdir(path)
        
    def is_file(self, path):
        """检查是否为文件
        
        Args:
            path: 文件路径
            
        Returns:
            是否为文件
        """
        return os.path.isfile(path)
        
    def get_file_hash(self, path, hash_type='md5'):
        """获取文件哈希值
        
        Args:
            path: 文件路径
            hash_type: 哈希类型，支持md5、sha1、sha256
            
        Returns:
            文件哈希值
        """
        try:
            import hashlib
            
            if hash_type not in ['md5', 'sha1', 'sha256']:
                hash_type = 'md5'
                
            hash_func = getattr(hashlib, hash_type)
            h = hash_func()
            
            with open(path, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    h.update(chunk)
            
            return h.hexdigest()
        except Exception as e:
            print(f"Get file hash error: {e}")
            return None

if __name__ == "__main__":
    # 测试文件管理功能
    fm = FileManager()
    
    # 获取当前目录文件列表
    print("Current directory files:")
    files = fm.get_file_list('.')
    for file in files:
        print(f"{file['name']} {'(dir)' if file['is_dir'] else ''} - {file['size']} bytes - {file['modified']}")
    
    # 获取主目录
    print(f"\nHome directory: {fm.get_home_directory()}")
    
    # 获取桌面目录
    print(f"Desktop directory: {fm.get_desktop_directory()}")
    
    # 获取可用空间
    print(f"Free space: {fm.get_free_space('.')} bytes")
