import pyperclip
import time
import threading
import platform
from PIL import Image
import io
import base64

class ClipboardSync:
    def __init__(self):
        self.platform = platform.system()
        self.last_content = None
        self.listening = False
        self.listen_thread = None
        self.tcp_client = None
        self.on_clipboard_change = None
        
    def set_tcp_client(self, tcp_client):
        """设置TCP客户端"""
        self.tcp_client = tcp_client
        
    def get_clipboard_content(self):
        """获取剪贴板内容
        
        Returns:
            剪贴板内容，包括类型和数据
            - 如果是文本：{"type": "text", "data": "文本内容"}
            - 如果是图片：{"type": "image", "data": "base64编码的图片数据"}
            - 如果是其他类型：None
        """
        try:
            # 尝试获取文本内容
            text = pyperclip.paste()
            if text:
                return {
                    "type": "text",
                    "data": text
                }
            
            # 尝试获取图片内容（Windows）
            if self.platform == "Windows":
                try:
                    from io import BytesIO
                    import win32clipboard
                    
                    win32clipboard.OpenClipboard()
                    if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
                        dib = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
                        win32clipboard.CloseClipboard()
                        
                        # 将DIB转换为PIL Image
                        import struct
                        
                        # DIB格式：BITMAPINFOHEADER + 像素数据
                        # 解析BITMAPINFOHEADER
                        bmi_header = dib[:40]
                        bi_width, bi_height, bi_bit_count = struct.unpack(
                            '<iih', bmi_header[4:14]
                        )
                        
                        # 创建PIL Image
                        img = Image.frombytes(
                            'RGB' if bi_bit_count == 24 else 'L',
                            (bi_width, abs(bi_height)),
                            dib[40:]
                        )
                        
                        # 转换为base64
                        buffer = BytesIO()
                        img.save(buffer, format='PNG')
                        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
                        
                        return {
                            "type": "image",
                            "data": img_str
                        }
                except Exception as e:
                    print(f"Get Windows image clipboard error: {e}")
            
            # 尝试获取图片内容（macOS）
            elif self.platform == "Darwin":
                try:
                    import subprocess
                    
                    # 使用osascript获取剪贴板图片
                    script = '''
                    set theImage to the clipboard as «class PNGf»
                    if theImage is not equal to missing value then
                        return theImage
                    else
                        return ""
                    end if
                    '''
                    result = subprocess.run(
                        ['osascript', '-e', script],
                        capture_output=True,
                        text=False
                    )
                    
                    if result.returncode == 0 and result.stdout:
                        img_str = base64.b64encode(result.stdout).decode('utf-8')
                        return {
                            "type": "image",
                            "data": img_str
                        }
                except Exception as e:
                    print(f"Get macOS image clipboard error: {e}")
            
            # 尝试获取图片内容（Linux）
            elif self.platform == "Linux":
                try:
                    import subprocess
                    import tempfile
                    
                    # 使用xclip获取剪贴板图片
                    with tempfile.NamedTemporaryFile(suffix='.png') as temp:
                        subprocess.run(
                            ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-o', temp.name],
                            check=True
                        )
                        
                        # 读取并编码图片
                        with open(temp.name, 'rb') as f:
                            img_str = base64.b64encode(f.read()).decode('utf-8')
                            
                        return {
                            "type": "image",
                            "data": img_str
                        }
                except Exception as e:
                    print(f"Get Linux image clipboard error: {e}")
            
            return None
        except Exception as e:
            print(f"Get clipboard content error: {e}")
            return None
            
    def set_clipboard_content(self, content):
        """设置剪贴板内容
        
        Args:
            content: 剪贴板内容，包括类型和数据
            - 文本：{"type": "text", "data": "文本内容"}
            - 图片：{"type": "image", "data": "base64编码的图片数据"}
            
        Returns:
            是否成功
        """
        try:
            if content["type"] == "text":
                # 设置文本内容
                pyperclip.copy(content["data"])
                return True
            
            elif content["type"] == "image":
                # 解码base64图片数据
                img_data = base64.b64decode(content["data"])
                img = Image.open(io.BytesIO(img_data))
                
                if self.platform == "Windows":
                    # Windows平台设置图片剪贴板
                    import win32clipboard
                    from io import BytesIO
                    
                    # 将PIL Image转换为DIB格式
                    buffer = BytesIO()
                    img.save(buffer, format='BMP')
                    bmp_data = buffer.getvalue()[14:]  # 去掉BMP文件头
                    
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, bmp_data)
                    win32clipboard.CloseClipboard()
                    return True
                
                elif self.platform == "Darwin":
                    # macOS平台设置图片剪贴板
                    import subprocess
                    import tempfile
                    
                    with tempfile.NamedTemporaryFile(suffix='.png') as temp:
                        img.save(temp.name, format='PNG')
                        subprocess.run(
                            ['osascript', '-e', f'set the clipboard to (read (POSIX file "{temp.name}") as «class PNGf»)', temp.name],
                            check=True
                        )
                    return True
                
                elif self.platform == "Linux":
                    # Linux平台设置图片剪贴板
                    import subprocess
                    import tempfile
                    
                    with tempfile.NamedTemporaryFile(suffix='.png') as temp:
                        img.save(temp.name, format='PNG')
                        subprocess.run(
                            ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', temp.name],
                            check=True
                        )
                    return True
            
            return False
        except Exception as e:
            print(f"Set clipboard content error: {e}")
            return False
            
    def start_listening(self, on_change=None):
        """开始监听剪贴板变化
        
        Args:
            on_change: 剪贴板变化回调函数，接收新的剪贴板内容
        """
        self.listening = True
        self.on_clipboard_change = on_change
        
        self.listen_thread = threading.Thread(target=self._listen_thread)
        self.listen_thread.daemon = True
        self.listen_thread.start()
        
    def stop_listening(self):
        """停止监听剪贴板变化"""
        self.listening = False
        if self.listen_thread:
            self.listen_thread.join(1)
        
    def _listen_thread(self):
        """监听线程"""
        while self.listening:
            current_content = self.get_clipboard_content()
            
            # 检查剪贴板内容是否变化
            if current_content and current_content != self.last_content:
                self.last_content = current_content
                
                # 调用回调函数
                if self.on_clipboard_change:
                    self.on_clipboard_change(current_content)
                
                # 发送到远程设备
                if self.tcp_client and self.tcp_client.is_connected():
                    self.send_clipboard_content(current_content)
            
            # 每秒检查一次
            time.sleep(1)
            
    def send_clipboard_content(self, content):
        """发送剪贴板内容到远程设备"""
        if not self.tcp_client or not self.tcp_client.is_connected():
            return False
            
        try:
            # 发送剪贴板内容
            self.tcp_client.send_message('clipboard_content', str(content).encode('utf-8'))
            return True
        except Exception as e:
            print(f"Send clipboard content error: {e}")
            return False
            
    def receive_clipboard_content(self, content_data):
        """接收远程设备的剪贴板内容
        
        Args:
            content_data: 接收到的剪贴板内容数据（bytes）
        """
        try:
            # 解析剪贴板内容
            content = eval(content_data.decode('utf-8'))
            
            # 设置本地剪贴板
            self.set_clipboard_content(content)
            
            # 更新最后内容
            self.last_content = content
            
            # 调用回调函数
            if self.on_clipboard_change:
                self.on_clipboard_change(content)
                
            return True
        except Exception as e:
            print(f"Receive clipboard content error: {e}")
            return False
            
    def sync_clipboard(self):
        """主动同步剪贴板内容到远程设备"""
        content = self.get_clipboard_content()
        if content:
            self.send_clipboard_content(content)
            return True
        return False

if __name__ == "__main__":
    # 测试剪贴板同步功能
    cs = ClipboardSync()
    
    # 测试获取剪贴板内容
    print("当前剪贴板内容：")
    content = cs.get_clipboard_content()
    print(content)
    
    # 测试设置剪贴板内容
    test_text = "测试剪贴板同步"
    print(f"\n设置剪贴板文本：{test_text}")
    cs.set_clipboard_content({"type": "text", "data": test_text})
    
    # 再次获取剪贴板内容
    print("\n设置后的剪贴板内容：")
    content = cs.get_clipboard_content()
    print(content)
