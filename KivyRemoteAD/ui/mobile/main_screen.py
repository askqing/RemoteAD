from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.listview import ListItemButton, ListView
from kivy.adapters.listadapter import ListAdapter
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.device.device_manager import DeviceManager
from core.network.udp_discovery import UDPClient
from core.network.tcp_client import TCPClient

class DeviceListButton(ListItemButton):
    """设备列表按钮"""
    pass

class MainScreen(BoxLayout):
    """主界面"""
    device_list = ObjectProperty()
    status_label = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # 初始化核心组件
        self.device_manager = DeviceManager()
        self.udp_client = UDPClient(self.device_manager.get_local_device())
        self.tcp_client = TCPClient()
        
        # 创建UI组件
        self.create_ui()
        
        # 开始设备发现
        self.start_device_discovery()
        
    def create_ui(self):
        """创建UI组件"""
        # 创建标题栏
        title_label = Label(text='远程控制中心', font_size='24sp', size_hint_y=None, height=50)
        self.add_widget(title_label)
        
        # 创建状态栏
        self.status_label = Label(text='就绪', size_hint_y=None, height=30)
        self.add_widget(self.status_label)
        
        # 创建设备列表
        self.device_list = ListView(
            adapter=ListAdapter(
                data=[],
                cls=DeviceListButton,
                args_converter=self.args_converter
            )
        )
        self.add_widget(self.device_list)
        
        # 创建按钮栏
        button_layout = BoxLayout(size_hint_y=None, height=50)
        
        refresh_btn = Button(text='刷新', on_press=self.refresh_device_list)
        button_layout.add_widget(refresh_btn)
        
        remote_desktop_btn = Button(text='远程桌面', on_press=self.open_remote_desktop)
        button_layout.add_widget(remote_desktop_btn)
        
        file_transfer_btn = Button(text='文件传输', on_press=self.open_file_transfer)
        button_layout.add_widget(file_transfer_btn)
        
        clipboard_btn = Button(text='剪贴板', on_press=self.toggle_clipboard_sync)
        button_layout.add_widget(clipboard_btn)
        
        self.add_widget(button_layout)
        
    def args_converter(self, row_index, item):
        """列表项转换器"""
        return {
            'text': item['text'],
            'size_hint_y': None,
            'height': 40,
            'device_data': item['device']
        }
        
    def start_device_discovery(self):
        """开始设备发现"""
        self.udp_client.start()
        
        # 定时更新设备列表
        from kivy.clock import Clock
        Clock.schedule_interval(self.update_device_list, 2)  # 每2秒更新一次
        
    def update_device_list(self, dt):
        """更新设备列表"""
        devices = self.udp_client.get_devices()
        self.device_manager.update_device_list(devices)
        
        # 构建设备列表数据
        list_data = []
        
        # 添加已配对设备
        paired_devices = self.device_manager.get_paired_devices()
        for device in paired_devices:
            list_data.append({
                'text': f"[已配对] {device['name']} ({device['ip']})",
                'device': device
            })
        
        # 添加已发现但未配对设备
        discovered_devices = self.device_manager.get_discovered_devices()
        for device in discovered_devices:
            if not self.device_manager.is_paired(device['id']):
                list_data.append({
                    'text': f"[未配对] {device['name']} ({device['ip']})",
                    'device': device
                })
        
        # 更新设备列表
        self.device_list.adapter.data = list_data
        self.device_list._trigger_reset_populate()
        
        # 更新状态栏
        total_devices = len(paired_devices) + len(discovered_devices)
        self.status_label.text = f"已发现 {total_devices} 台设备，其中 {len(paired_devices)} 台已配对"
        
    def refresh_device_list(self, instance):
        """刷新设备列表"""
        self.udp_client.discover()
        self.update_device_list(0)
        self.show_popup("提示", "设备列表已刷新")
        
    def open_remote_desktop(self, instance):
        """打开远程桌面"""
        self.show_popup("提示", "远程桌面功能开发中...")
        
    def open_file_transfer(self, instance):
        """打开文件传输"""
        self.show_popup("提示", "文件传输功能开发中...")
        
    def toggle_clipboard_sync(self, instance):
        """切换剪贴板同步"""
        self.show_popup("提示", "剪贴板同步功能开发中...")
        
    def show_popup(self, title, content):
        """显示弹窗"""
        popup = Popup(
            title=title,
            content=Label(text=content),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()
        
    def on_device_select(self, instance):
        """设备选择事件"""
        device = instance.device_data
        self.show_popup("设备信息", f"设备名称: {device['name']}\nIP地址: {device['ip']}\n设备类型: {device['type']}")

class RemoteControlApp(App):
    """远程控制应用"""
    
    def build(self):
        """构建应用"""
        return MainScreen()

if __name__ == "__main__":
    RemoteControlApp().run()
