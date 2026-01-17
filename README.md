# RemoteAD - 远程桌面控制应用

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/Kivy-2.1.0-green.svg)](https://kivy.org/)

一个基于 Python 和 Kivy 的跨平台远程桌面控制应用，支持桌面端（Windows/Linux/macOS）和移动端（Android）。

## 功能特性

- ✅ 实时屏幕共享和控制
- ✅ 跨平台支持（桌面端和移动端）
- ✅ 安全的加密通信
- ✅ 支持横屏/竖屏显示
- ✅ 简洁直观的用户界面

## 第一次测试

### 快速开始

#### 桌面端

1. 克隆仓库
```bash
git clone https://github.com/askqing/RemoteAD.git
cd RemoteAD
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行应用
```bash
python main_desktop.py
```

#### 移动端

1. 从 [Releases](https://github.com/askqing/RemoteAD/releases) 下载最新的 APK 文件
2. 在 Android 设备上安装 APK
3. 运行应用

### 编译 Android APK

如果你需要自己编译 Android APK，请参考 [ANDROID_COMPILE_GUIDE.md](ANDROID_COMPILE_GUIDE.md) 获取详细说明。

### 测试步骤

1. 在桌面端启动服务器
2. 在移动端启动客户端
3. 输入桌面端的 IP 地址和端口
4. 建立连接并开始控制

## 系统要求

### 桌面端
- Python 3.10+
- Windows 10+ / Linux / macOS

### 移动端
- Android 5.0 (API 21) 或更高版本
- 支持的架构：armeabi-v7a, arm64-v8a

## 技术栈

- **GUI 框架**：Kivy (桌面端和移动端)、PyQt5 (桌面端)
- **网络通信**：PyZMQ
- **加密**：PyCryptodome
- **图像处理**：OpenCV、Pillow
- **屏幕捕获**：MSS

## 开源协议

本项目采用 [MIT 协议](LICENSE) 开源。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

[askqing](https://github.com/askqing)

## 鸣谢

感谢所有为此项目做出贡献的开发者。

---

**English version below**

# RemoteAD - Remote Desktop Control Application

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/Kivy-2.1.0-green.svg)](https://kivy.org/)

A cross-platform remote desktop control application based on Python and Kivy, supporting both desktop (Windows/Linux/macOS) and mobile (Android) platforms.

## Features

- ✅ Real-time screen sharing and control
- ✅ Cross-platform support (desktop and mobile)
- ✅ Secure encrypted communication
- ✅ Supports landscape/portrait orientation
- ✅ Clean and intuitive user interface

## First Test

### Quick Start

#### Desktop

1. Clone the repository
```bash
git clone https://github.com/askqing/RemoteAD.git
cd RemoteAD
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python main_desktop.py
```

#### Mobile

1. Download the latest APK from [Releases](https://github.com/askqing/RemoteAD/releases)
2. Install the APK on your Android device
3. Run the application

### Building Android APK

If you need to build the Android APK yourself, please refer to [ANDROID_COMPILE_GUIDE.md](ANDROID_COMPILE_GUIDE.md) for detailed instructions.

### Testing Steps

1. Start the server on the desktop
2. Start the client on the mobile device
3. Enter the desktop IP address and port
4. Establish connection and start controlling

## System Requirements

### Desktop
- Python 3.10+
- Windows 10+ / Linux / macOS

### Mobile
- Android 5.0 (API 21) or higher
- Supported architectures: armeabi-v7a, arm64-v8a

## Tech Stack

- **GUI Framework**: Kivy (desktop and mobile), PyQt5 (desktop)
- **Network**: PyZMQ
- **Encryption**: PyCryptodome
- **Image Processing**: OpenCV, Pillow
- **Screen Capture**: MSS

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Issues and Pull Requests are welcome!

## Author

[askqing](https://github.com/askqing)

## Acknowledgments

Thanks to all developers who contributed to this project.
