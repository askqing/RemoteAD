from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QPushButton, QLabel, QSplitter, 
    QTabWidget, QGroupBox, QFormLayout, QLineEdit,
    QStatusBar, QMenuBar, QMenu, QAction, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.device.device_manager import DeviceManager
from core.network.udp_discovery import UDPClient
from core.network.tcp_client import TCPClient
from services.remote_desktop.screen_capture import ScreenCapture
from services.file_transfer.file_manager import FileManager
from services.clipboard.clipboard_sync import ClipboardSync

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("远程控制中心")
        self.setGeometry(100, 100, 1000, 700)
        
        # 初始化核心组件
        self.device_manager = DeviceManager()
        self.udp_client = UDPClient(self.device_manager.get_local_device())
        self.tcp_client = TCPClient()
        self.screen_capture = ScreenCapture()
        self.file_manager = FileManager()
        self.clipboard_sync = ClipboardSync()
        
        # 设置TCP客户端
        self.clipboard_sync.set_tcp_client(self.tcp_client)
        
        # 初始化UI组件
        self.init_ui()
        
        # 开始设备发现
        self.start_device_discovery()
        
    def init_ui(self):
        """初始化UI组件"""
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建左侧设备列表
        self.device_list = QListWidget()
        self.device_list.setMinimumWidth(250)
        self.device_list.itemDoubleClicked.connect(self.on_device_double_click)
        
        # 创建右侧标签页
        self.tab_widget = QTabWidget()
        
        # 添加设备信息标签页
        self.create_device_info_tab()
        
        # 添加功能标签页
        self.create_function_tab()
        
        # 添加分割器
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.device_list)
        splitter.addWidget(self.tab_widget)
        splitter.setSizes([250, 750])
        
        main_layout.addWidget(splitter)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
    def create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = self.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_settings)
        edit_menu.addAction(settings_action)
        
        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_device_info_tab(self):
        """创建设备信息标签页"""
        device_info_tab = QWidget()
        layout = QVBoxLayout(device_info_tab)
        
        # 设备信息分组
        device_group = QGroupBox("设备信息")
        device_layout = QFormLayout(device_group)
        
        self.device_name_label = QLabel("--")
        self.device_type_label = QLabel("--")
        self.device_ip_label = QLabel("--")
        self.device_platform_label = QLabel("--")
        
        device_layout.addRow("设备名称:", self.device_name_label)
        device_layout.addRow("设备类型:", self.device_type_label)
        device_layout.addRow("IP地址:", self.device_ip_label)
        device_layout.addRow("平台:", self.device_platform_label)
        
        # 本地设备信息分组
        local_device_group = QGroupBox("本地设备")
        local_layout = QFormLayout(local_device_group)
        
        local_device = self.device_manager.get_local_device()
        local_device_name = QLabel(local_device['name'])
        local_device_ip = QLabel(local_device['ip'])
        local_device_type = QLabel(local_device['type'])
        local_device_platform = QLabel(local_device['platform'])
        
        local_layout.addRow("设备名称:", local_device_name)
        local_layout.addRow("IP地址:", local_device_ip)
        local_layout.addRow("设备类型:", local_device_type)
        local_layout.addRow("平台:", local_device_platform)
        
        layout.addWidget(device_group)
        layout.addWidget(local_device_group)
        layout.addStretch()
        
        self.tab_widget.addTab(device_info_tab, "设备信息")
        
    def create_function_tab(self):
        """创建功能标签页"""
        function_tab = QWidget()
        layout = QVBoxLayout(function_tab)
        
        # 远程连接方式
        connect_group = QGroupBox("远程连接")
        connect_layout = QFormLayout(connect_group)
        
        # 手动输入IP/域名连接
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("输入目标IP或域名")
        self.connect_btn = QPushButton("连接")
        self.connect_btn.clicked.connect(self.connect_by_ip)
        
        # 扫描局域网设备
        self.scan_btn = QPushButton("扫描设备")
        self.scan_btn.clicked.connect(self.refresh_device_list)
        
        connect_layout.addRow("手动连接:", self.ip_input)
        connect_layout.addRow(self.connect_btn, self.scan_btn)
        
        # 远程控制按钮组
        control_group = QGroupBox("远程控制")
        control_layout = QHBoxLayout(control_group)
        
        self.remote_desktop_btn = QPushButton("远程桌面")
        self.remote_desktop_btn.setEnabled(False)
        self.remote_desktop_btn.clicked.connect(self.open_remote_desktop)
        
        self.file_transfer_btn = QPushButton("文件传输")
        self.file_transfer_btn.setEnabled(False)
        self.file_transfer_btn.clicked.connect(self.open_file_transfer)
        
        self.clipboard_btn = QPushButton("剪贴板同步")
        self.clipboard_btn.setEnabled(False)
        self.clipboard_btn.clicked.connect(self.toggle_clipboard_sync)
        
        control_layout.addWidget(self.remote_desktop_btn)
        control_layout.addWidget(self.file_transfer_btn)
        control_layout.addWidget(self.clipboard_btn)
        
        # 设备管理按钮组
        manage_group = QGroupBox("设备管理")
        manage_layout = QHBoxLayout(manage_group)
        
        self.refresh_btn = QPushButton("刷新设备列表")
        self.refresh_btn.clicked.connect(self.refresh_device_list)
        
        self.pair_btn = QPushButton("配对设备")
        self.pair_btn.setEnabled(False)
        self.pair_btn.clicked.connect(self.pair_device)
        
        self.unpair_btn = QPushButton("解除配对")
        self.unpair_btn.setEnabled(False)
        self.unpair_btn.clicked.connect(self.unpair_device)
        
        manage_layout.addWidget(self.refresh_btn)
        manage_layout.addWidget(self.pair_btn)
        manage_layout.addWidget(self.unpair_btn)
        
        layout.addWidget(connect_group)
        layout.addWidget(control_group)
        layout.addWidget(manage_group)
        layout.addStretch()
        
        self.tab_widget.addTab(function_tab, "功能")
        
    def start_device_discovery(self):
        """开始设备发现"""
        self.udp_client.start()
        
        # 定时更新设备列表
        self.device_update_timer = QTimer(self)
        self.device_update_timer.timeout.connect(self.update_device_list)
        self.device_update_timer.start(2000)  # 每2秒更新一次
        
    def update_device_list(self):
        """更新设备列表"""
        devices = self.udp_client.get_devices()
        self.device_manager.update_device_list(devices)
        
        # 更新设备列表UI
        self.device_list.clear()
        
        # 添加已配对设备
        paired_devices = self.device_manager.get_paired_devices()
        for device in paired_devices:
            item_text = f"[已配对] {device['name']} ({device['ip']})"
            item = self.device_list.addItem(item_text)
            item.setData(Qt.UserRole, device)
        
        # 添加已发现但未配对设备
        discovered_devices = self.device_manager.get_discovered_devices()
        for device in discovered_devices:
            if not self.device_manager.is_paired(device['id']):
                item_text = f"[未配对] {device['name']} ({device['ip']})"
                item = self.device_list.addItem(item_text)
                item.setData(Qt.UserRole, device)
        
        # 更新状态栏
        total_devices = len(paired_devices) + len(discovered_devices)
        self.status_bar.showMessage(f"已发现 {total_devices} 台设备，其中 {len(paired_devices)} 台已配对")
        
    def on_device_double_click(self, item):
        """双击设备列表项"""
        device = item.data(Qt.UserRole)
        if device:
            self.select_device(device)
        
    def select_device(self, device):
        """选择设备"""
        # 更新设备信息
        self.device_name_label.setText(device['name'])
        self.device_type_label.setText(device['type'])
        self.device_ip_label.setText(device['ip'])
        self.device_platform_label.setText(device['platform'])
        
        # 启用/禁用按钮
        is_paired = self.device_manager.is_paired(device['id'])
        self.remote_desktop_btn.setEnabled(is_paired)
        self.file_transfer_btn.setEnabled(is_paired)
        self.clipboard_btn.setEnabled(is_paired)
        self.pair_btn.setEnabled(not is_paired)
        self.unpair_btn.setEnabled(is_paired)
        
        # 连接到设备
        if is_paired:
            self.connect_to_device(device)
        
    def connect_to_device(self, device):
        """连接到设备"""
        if not self.tcp_client.is_connected():
            self.tcp_client.connect(device['ip'], 5001)
    
    def connect_by_ip(self):
        """通过IP连接设备"""
        ip = self.ip_input.text().strip()
        if not ip:
            QMessageBox.warning(self, "警告", "请输入IP地址或域名")
            return
        
        # 创建虚拟设备对象
        device = {
            'id': f'manual_{ip}',
            'name': f'Manual Connection - {ip}',
            'type': 'unknown',
            'ip': ip,
            'platform': 'unknown'
        }
        
        # 连接到设备
        self.connect_to_device(device)
        
        # 更新设备信息
        self.select_device(device)
        
        # 添加到设备列表
        item_text = f"[手动连接] {device['name']}"
        item = self.device_list.addItem(item_text)
        item.setData(Qt.UserRole, device)
        
        QMessageBox.information(self, "提示", f"已连接到 {ip}")
        
    def open_remote_desktop(self):
        """打开远程桌面窗口"""
        QMessageBox.information(self, "提示", "远程桌面功能开发中...")
        
    def open_file_transfer(self):
        """打开文件传输窗口"""
        QMessageBox.information(self, "提示", "文件传输功能开发中...")
        
    def toggle_clipboard_sync(self):
        """切换剪贴板同步"""
        if self.clipboard_sync.listening:
            self.clipboard_sync.stop_listening()
            self.clipboard_btn.setText("启用剪贴板同步")
            QMessageBox.information(self, "提示", "剪贴板同步已关闭")
        else:
            self.clipboard_sync.start_listening()
            self.clipboard_btn.setText("禁用剪贴板同步")
            QMessageBox.information(self, "提示", "剪贴板同步已启用")
        
    def pair_device(self):
        """配对设备"""
        current_item = self.device_list.currentItem()
        if current_item:
            device = current_item.data(Qt.UserRole)
            if device:
                # 这里应该显示配对码并等待用户输入
                QMessageBox.information(self, "提示", "设备配对功能开发中...")
        
    def unpair_device(self):
        """解除配对"""
        current_item = self.device_list.currentItem()
        if current_item:
            device = current_item.data(Qt.UserRole)
            if device:
                self.device_manager.remove_paired_device(device['id'])
                self.update_device_list()
                QMessageBox.information(self, "提示", f"已解除与 {device['name']} 的配对")
        
    def refresh_device_list(self):
        """刷新设备列表"""
        self.udp_client.discover()
        self.update_device_list()
        QMessageBox.information(self, "提示", "设备列表已刷新")
        
    def show_settings(self):
        """显示设置对话框"""
        QMessageBox.information(self, "提示", "设置功能开发中...")
        
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, "关于远程控制中心", 
                        "远程控制中心 v1.0\n\n" 
                        "基于Python的跨平台局域网远程控制软件\n" 
                        "支持设备间直接互联，无需服务器\n\n" 
                        "© 2024 远程控制中心")
        
    def closeEvent(self, event):
        """关闭事件"""
        # 停止设备发现
        self.udp_client.stop()
        
        # 停止剪贴板监听
        self.clipboard_sync.stop_listening()
        
        # 断开TCP连接
        self.tcp_client.disconnect()
        
        # 停止定时器
        if hasattr(self, 'device_update_timer'):
            self.device_update_timer.stop()
        
        event.accept()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
