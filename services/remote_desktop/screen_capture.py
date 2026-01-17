import platform
import time
import numpy as np

class ScreenCapture:
    def __init__(self):
        self.platform = platform.system()
        self.capture_method = self._get_capture_method()
        
    def _get_capture_method(self):
        """根据平台选择合适的屏幕捕获方法"""
        if self.platform == 'Windows':
            return self._windows_capture
        elif self.platform == 'Darwin':
            return self._macos_capture
        elif self.platform == 'Linux':
            return self._linux_capture
        else:
            raise NotImplementedError(f"Screen capture not supported on {self.platform}")
            
    def _windows_capture(self):
        """Windows屏幕捕获"""
        try:
            from mss import mss
            with mss() as sct:
                # 获取主显示器
                monitor = sct.monitors[1]
                # 捕获屏幕
                screenshot = sct.grab(monitor)
                # 转换为numpy数组
                img = np.array(screenshot)
                # 转换为RGB格式（去掉alpha通道）
                if img.shape[2] == 4:
                    img = img[:, :, :3]
                return img
        except Exception as e:
            print(f"Windows screen capture error: {e}")
            return None
            
    def _macos_capture(self):
        """macOS屏幕捕获"""
        try:
            import subprocess
            import sys
            import io
            from PIL import Image
            
            # 使用screencapture命令捕获屏幕
            process = subprocess.Popen(
                ['screencapture', '-t', 'png', '-x', '-'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"macOS screen capture error: {stderr.decode('utf-8')}")
                return None
            
            # 从stdout读取图像
            img = Image.open(io.BytesIO(stdout))
            # 转换为numpy数组
            img = np.array(img)
            # 转换为RGB格式
            if img.shape[2] == 4:
                img = img[:, :, :3]
            return img
        except Exception as e:
            print(f"macOS screen capture error: {e}")
            return None
            
    def _linux_capture(self):
        """Linux屏幕捕获"""
        try:
            import subprocess
            import sys
            import io
            from PIL import Image
            
            # 使用scrot命令捕获屏幕
            process = subprocess.Popen(
                ['scrot', '-z', '-t', '0', '-'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                # 尝试使用xwd命令
                try:
                    process = subprocess.Popen(
                        ['xwd', '-root', '-silent'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    stdout, stderr = process.communicate()
                    
                    if process.returncode != 0:
                        print(f"Linux screen capture error: {stderr.decode('utf-8')}")
                        return None
                    
                    img = Image.open(io.BytesIO(stdout))
                    img = np.array(img)
                    if img.shape[2] == 4:
                        img = img[:, :, :3]
                    return img
                except Exception as e:
                    print(f"Linux screen capture error: {e}")
                    return None
            
            # 从stdout读取图像
            img = Image.open(io.BytesIO(stdout))
            # 转换为numpy数组
            img = np.array(img)
            # 转换为RGB格式
            if img.shape[2] == 4:
                img = img[:, :, :3]
            return img
        except Exception as e:
            print(f"Linux screen capture error: {e}")
            return None
            
    def capture(self):
        """捕获屏幕"""
        return self.capture_method()
        
    def test_capture(self):
        """测试屏幕捕获功能"""
        print(f"Testing screen capture on {self.platform}...")
        start_time = time.time()
        img = self.capture()
        end_time = time.time()
        
        if img is not None:
            print(f"Capture successful! Image shape: {img.shape}, Time: {end_time - start_time:.2f}s")
            return True
        else:
            print("Capture failed!")
            return False

if __name__ == "__main__":
    sc = ScreenCapture()
    sc.test_capture()
