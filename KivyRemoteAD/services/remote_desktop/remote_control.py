import platform
import time

class RemoteControl:
    def __init__(self):
        self.platform = platform.system()
        self.control_method = self._get_control_method()
        
    def _get_control_method(self):
        """根据平台选择合适的远程控制方法"""
        if self.platform == 'Windows':
            return self._windows_control
        elif self.platform == 'Darwin':
            return self._macos_control
        elif self.platform == 'Linux':
            return self._linux_control
        else:
            raise NotImplementedError(f"Remote control not supported on {self.platform}")
            
    def _windows_control(self, event_type, **kwargs):
        """Windows远程控制"""
        try:
            import win32api
            import win32con
            import win32gui
            
            if event_type == 'mouse_move':
                # 移动鼠标
                x = kwargs.get('x', 0)
                y = kwargs.get('y', 0)
                win32api.SetCursorPos((x, y))
            
            elif event_type == 'mouse_click':
                # 鼠标点击
                x = kwargs.get('x', 0)
                y = kwargs.get('y', 0)
                button = kwargs.get('button', 'left')
                
                # 先移动到指定位置
                win32api.SetCursorPos((x, y))
                
                # 执行点击
                if button == 'left':
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
                elif button == 'right':
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
                elif button == 'middle':
                    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, x, y, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, x, y, 0, 0)
            
            elif event_type == 'mouse_down':
                # 鼠标按下
                x = kwargs.get('x', 0)
                y = kwargs.get('y', 0)
                button = kwargs.get('button', 'left')
                
                if button == 'left':
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
                elif button == 'right':
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
                elif button == 'middle':
                    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, x, y, 0, 0)
            
            elif event_type == 'mouse_up':
                # 鼠标释放
                x = kwargs.get('x', 0)
                y = kwargs.get('y', 0)
                button = kwargs.get('button', 'left')
                
                if button == 'left':
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
                elif button == 'right':
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
                elif button == 'middle':
                    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, x, y, 0, 0)
            
            elif event_type == 'mouse_wheel':
                # 鼠标滚轮
                delta = kwargs.get('delta', 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, delta, 0)
            
            elif event_type == 'key_down':
                # 键盘按下
                key = kwargs.get('key', '')
                win32api.keybd_event(ord(key.upper()), 0, 0, 0)
            
            elif event_type == 'key_up':
                # 键盘释放
                key = kwargs.get('key', '')
                win32api.keybd_event(ord(key.upper()), 0, win32con.KEYEVENTF_KEYUP, 0)
            
            elif event_type == 'key_press':
                # 键盘按键（按下并释放）
                key = kwargs.get('key', '')
                win32api.keybd_event(ord(key.upper()), 0, 0, 0)
                win32api.keybd_event(ord(key.upper()), 0, win32con.KEYEVENTF_KEYUP, 0)
            
            return True
        except Exception as e:
            print(f"Windows remote control error: {e}")
            return False
            
    def _macos_control(self, event_type, **kwargs):
        """macOS远程控制"""
        try:
            import subprocess
            
            if event_type == 'mouse_move':
                # 移动鼠标
                x = kwargs.get('x', 0)
                y = kwargs.get('y', 0)
                subprocess.run(['cliclick', f'm:{x},{y}'], check=True)
            
            elif event_type == 'mouse_click':
                # 鼠标点击
                x = kwargs.get('x', 0)
                y = kwargs.get('y', 0)
                button = kwargs.get('button', 'left')
                
                if button == 'left':
                    subprocess.run(['cliclick', f'c:{x},{y}'], check=True)
                elif button == 'right':
                    subprocess.run(['cliclick', f'rc:{x},{y}'], check=True)
                elif button == 'middle':
                    subprocess.run(['cliclick', f'mc:{x},{y}'], check=True)
            
            elif event_type == 'mouse_down':
                # 鼠标按下
                x = kwargs.get('x', 0)
                y = kwargs.get('y', 0)
                button = kwargs.get('button', 'left')
                
                if button == 'left':
                    subprocess.run(['cliclick', f'd:{x},{y}'], check=True)
                elif button == 'right':
                    subprocess.run(['cliclick', f'rd:{x},{y}'], check=True)
            
            elif event_type == 'mouse_up':
                # 鼠标释放
                x = kwargs.get('x', 0)
                y = kwargs.get('y', 0)
                button = kwargs.get('button', 'left')
                
                if button == 'left':
                    subprocess.run(['cliclick', f'u:{x},{y}'], check=True)
                elif button == 'right':
                    subprocess.run(['cliclick', f'ru:{x},{y}'], check=True)
            
            elif event_type == 'mouse_wheel':
                # 鼠标滚轮
                delta = kwargs.get('delta', 0)
                if delta > 0:
                    subprocess.run(['cliclick', f'wu:{delta}'], check=True)
                else:
                    subprocess.run(['cliclick', f'wd:{abs(delta)}'], check=True)
            
            elif event_type == 'key_press':
                # 键盘按键
                key = kwargs.get('key', '')
                subprocess.run(['cliclick', f'k:{key}'], check=True)
            
            return True
        except Exception as e:
            print(f"macOS remote control error: {e}")
            return False
            
    def _linux_control(self, event_type, **kwargs):
        """Linux远程控制"""
        try:
            import subprocess
            
            if event_type == 'mouse_move':
                # 移动鼠标
                x = kwargs.get('x', 0)
                y = kwargs.get('y', 0)
                subprocess.run(['xdotool', 'mousemove', str(x), str(y)], check=True)
            
            elif event_type == 'mouse_click':
                # 鼠标点击
                x = kwargs.get('x', 0)
                y = kwargs.get('y', 0)
                button = kwargs.get('button', 'left')
                
                # 先移动到指定位置
                subprocess.run(['xdotool', 'mousemove', str(x), str(y)], check=True)
                
                # 执行点击
                if button == 'left':
                    subprocess.run(['xdotool', 'click', '1'], check=True)
                elif button == 'right':
                    subprocess.run(['xdotool', 'click', '3'], check=True)
                elif button == 'middle':
                    subprocess.run(['xdotool', 'click', '2'], check=True)
            
            elif event_type == 'mouse_down':
                # 鼠标按下
                button = kwargs.get('button', 'left')
                
                if button == 'left':
                    subprocess.run(['xdotool', 'mousedown', '1'], check=True)
                elif button == 'right':
                    subprocess.run(['xdotool', 'mousedown', '3'], check=True)
                elif button == 'middle':
                    subprocess.run(['xdotool', 'mousedown', '2'], check=True)
            
            elif event_type == 'mouse_up':
                # 鼠标释放
                button = kwargs.get('button', 'left')
                
                if button == 'left':
                    subprocess.run(['xdotool', 'mouseup', '1'], check=True)
                elif button == 'right':
                    subprocess.run(['xdotool', 'mouseup', '3'], check=True)
                elif button == 'middle':
                    subprocess.run(['xdotool', 'mouseup', '2'], check=True)
            
            elif event_type == 'mouse_wheel':
                # 鼠标滚轮
                delta = kwargs.get('delta', 0)
                if delta > 0:
                    subprocess.run(['xdotool', 'click', '--repeat', str(delta), '4'], check=True)
                else:
                    subprocess.run(['xdotool', 'click', '--repeat', str(abs(delta)), '5'], check=True)
            
            elif event_type == 'key_down':
                # 键盘按下
                key = kwargs.get('key', '')
                subprocess.run(['xdotool', 'keydown', key], check=True)
            
            elif event_type == 'key_up':
                # 键盘释放
                key = kwargs.get('key', '')
                subprocess.run(['xdotool', 'keyup', key], check=True)
            
            elif event_type == 'key_press':
                # 键盘按键（按下并释放）
                key = kwargs.get('key', '')
                subprocess.run(['xdotool', 'key', key], check=True)
            
            return True
        except Exception as e:
            print(f"Linux remote control error: {e}")
            return False
            
    def send_event(self, event_type, **kwargs):
        """发送远程控制事件
        
        Args:
            event_type: 事件类型，包括：
                - mouse_move: 鼠标移动
                - mouse_click: 鼠标点击
                - mouse_down: 鼠标按下
                - mouse_up: 鼠标释放
                - mouse_wheel: 鼠标滚轮
                - key_down: 键盘按下
                - key_up: 键盘释放
                - key_press: 键盘按键
            **kwargs: 事件参数，根据事件类型不同而不同
                - mouse_move: x, y
                - mouse_click: x, y, button (left/right/middle)
                - mouse_down: x, y, button (left/right/middle)
                - mouse_up: x, y, button (left/right/middle)
                - mouse_wheel: delta (正数向上，负数向下)
                - key_down: key (按键名称)
                - key_up: key (按键名称)
                - key_press: key (按键名称)
                
        Returns:
            是否成功
        """
        return self.control_method(event_type, **kwargs)
        
    def test_control(self):
        """测试远程控制功能"""
        print(f"Testing remote control on {self.platform}...")
        
        # 测试鼠标移动
        if self.send_event('mouse_move', x=100, y=100):
            print("Mouse move test passed")
        else:
            print("Mouse move test failed")
        
        time.sleep(1)
        
        # 测试鼠标点击
        if self.send_event('mouse_click', x=100, y=100, button='left'):
            print("Mouse click test passed")
        else:
            print("Mouse click test failed")
        
        return True

if __name__ == "__main__":
    rc = RemoteControl()
    rc.test_control()
