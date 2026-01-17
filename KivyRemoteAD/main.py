import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.mobile.main_screen import RemoteControlApp

if __name__ == "__main__":
    RemoteControlApp().run()
