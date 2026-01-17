# Android 编译完整指南

本指南将详细说明如何在 Ubuntu 系统中使用 Buildozer 编译 Android 应用。

## 1. 系统环境要求

- Ubuntu 22.04 LTS 或更高版本
- 至少 4GB 内存（建议 8GB+）
- 至少 20GB 空闲磁盘空间
- 稳定的网络连接

## 2. 更换国内软件源

### 2.1 备份原软件源
```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
```

### 2.2 替换为阿里云镜像源
```bash
sudo sed -i 's@/archive.ubuntu.com/@/mirrors.aliyun.com/@g' /etc/apt/sources.list
```

### 2.3 更新软件包列表
```bash
sudo apt-get update
```

## 3. 安装系统依赖

### 3.1 安装基本编译工具
```bash
sudo apt-get install -y build-essential git curl python3-pip python3-dev
```

### 3.2 安装 Buildozer 依赖
```bash
sudo apt-get install -y \n    zip unzip openjdk-17-jdk-headless \n    autoconf libtool pkg-config zlib1g-dev \n    libncurses5-dev libncursesw5-dev libtinfo5 \n    cmake libffi-dev libssl-dev libxml2-dev \n    libxslt1-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \n    gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \n    gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools \n    gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 \n    gstreamer1.0-qt5 gstreamer1.0-pulseaudio \n    libmtdev-dev libjpeg-dev libpng-dev libsdl2-dev \n    libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

## 4. 安装 Python 依赖

### 4.1 升级 pip
```bash
sudo pip3 install --upgrade pip
```

### 4.2 安装 Buildozer
```bash
pip3 install --user buildozer
```

### 4.3 将 Buildozer 添加到 PATH
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## 5. 编译 Android 应用

### 5.1 进入项目目录
```bash
cd /path/to/remote-control-project
```

### 5.2 初始化 Buildozer（如果没有 buildozer.spec 文件）
```bash
buildozer init
```

### 5.3 编译 APK
```bash
# 首次编译会下载大量依赖，可能需要较长时间
buildozer -v android debug
```

### 5.4 编译完成
编译成功后，APK 文件将位于 `bin/` 目录下，文件名类似：`remotead-1.0-debug.apk`

## 6. 常见问题解决方案

### 6.1 软件包无法定位
```bash
# 刷新软件包列表
sudo apt-get update

# 尝试安装单个软件包，查看具体错误
sudo apt-get install -y [package-name]

# 如果仍然无法定位，尝试使用其他镜像源，如清华大学源
sudo sed -i 's@/mirrors.aliyun.com/@/mirrors.tuna.tsinghua.edu.cn/@g' /etc/apt/sources.list
sudo apt-get update
```

### 6.2 Java 版本问题
```bash
# 查看当前 Java 版本
java -version

# 如果版本不是 17，安装 openjdk-17
sudo apt-get install -y openjdk-17-jdk-headless

# 设置默认 Java 版本
sudo update-alternatives --config java
```

### 6.3 内存不足问题
```bash
# 增加 swap 空间
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 永久启用 swap
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 6.4 Buildozer 编译错误
```bash
# 清除之前的编译缓存
buildozer android clean

# 查看详细日志
buildozer -v android debug 2>&1 | tee buildozer.log

# 常见错误：NDK 版本不匹配
# 修改 buildozer.spec 文件中的 android.ndk 版本
nano buildozer.spec
```

## 7. 使用编译好的 APK

### 7.1 将 APK 传输到 Android 设备
```bash
# 使用 adb 命令（需要安装 adb）
sudo apt-get install -y adb
adb devices
adb install bin/remotead-1.0-debug.apk

# 或使用文件传输工具，如 scp、FTP 等
```

### 7.2 在 Android 设备上运行
1. 开启设备的「开发者选项」和「USB 调试」
2. 安装 APK 文件
3. 打开应用程序列表，找到「RemoteAD」应用
4. 点击运行

## 8. 进阶选项

### 8.1 编译发布版本（Release）
```bash
# 需要配置签名密钥
buildozer -v android release
```

### 8.2 仅编译特定架构
```bash
# 修改 buildozer.spec 文件中的 android.arch
android.arch = armeabi-v7a  # 或 arm64-v8a

buildozer -v android debug
```

### 8.3 使用 Buildozer 命令行选项
```bash
# 查看所有可用命令
buildozer --help

# 查看 Android 相关命令
buildozer android --help
```

## 9. 编译脚本

### 9.1 创建编译脚本（compile_android.sh）
```bash
#!/bin/bash

echo "=== 开始编译 Android 应用 ==="
echo "当前目录: $(pwd)"
echo "开始时间: $(date)"

# 清除之前的编译缓存
echo "=== 清除编译缓存 ==="
buildozer android clean

# 编译 APK
echo "=== 编译 APK ==="
buildozer -v android debug

if [ $? -eq 0 ]; then
    echo "=== 编译成功！==="
    echo "APK 文件位置: $(find bin -name "*.apk")"
    echo "结束时间: $(date)"
else
    echo "=== 编译失败！==="
    echo "查看日志: buildozer.log"
    exit 1
fi
```

### 9.2 运行编译脚本
```bash
chmod +x compile_android.sh
./compile_android.sh
```

## 10. 项目配置说明

### 10.1 buildozer.spec 关键配置
```ini
[app]
title = RemoteAD              # 应用名称
package.name = remotead       # 包名
package.domain = com.remotead # 域名
version = 1.0                 # 版本号
requirements = python3,kivy,cryptography,pillow,pyyaml  # 依赖库
orientation = landscape       # 屏幕方向

# Android 配置
android.api = 31              # API 级别
android.sdk = 33              # SDK 版本
android.ndk = 25.1.8937393    # NDK 版本
android.arch = armeabi-v7a,arm64-v8a  # 支持的架构
android.accept_sdk_license = True     # 自动接受 SDK 许可证
```

### 10.2 项目结构要求
```
project/
├── main_mobile.py            # 主入口文件
├── buildozer.spec            # Buildozer 配置文件
├── core/                     # 核心代码
├── ui/                       # UI 代码
├── services/                 # 服务代码
└── requirements.txt          # Python 依赖
```

## 11. 调试技巧

### 11.1 查看应用日志
```bash
adb logcat -s python
```

### 11.2 实时调试
```bash
# 连接到运行中的应用
buildozer android deploy run logcat
```

### 11.3 常见应用崩溃原因
- 权限问题：确保在 `buildozer.spec` 中配置了必要的权限
- 依赖版本不兼容：尝试降低或升级问题依赖的版本
- 代码错误：使用 adb logcat 查看具体错误信息
- 资源文件缺失：确保所有必要的资源文件都包含在项目中

## 12. 权限配置

### 12.1 在 buildozer.spec 中添加权限
```ini
android.permissions = INTERNET,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,ACCESS_NETWORK_STATE
```

## 13. 优化编译速度

### 13.1 使用本地缓存
```bash
# 配置 Buildozer 使用本地缓存
export PIP_CACHE_DIR="$HOME/.cache/pip"
export GRADLE_USER_HOME="$HOME/.gradle"
```

### 13.2 并行编译
```bash
# 修改 buildozer.spec 文件
android.gradle_parallel = True
```

## 14. 总结

1. 确保 Ubuntu 系统环境正确配置
2. 安装所有必要的依赖
3. 配置 buildozer.spec 文件
4. 使用 Buildozer 编译 APK
5. 调试和测试编译好的 APK

遵循本指南，您应该能够成功编译 Android 应用。如果遇到问题，请参考「常见问题解决方案」部分，或查看 Buildozer 详细日志以定位问题。

---

**提示：** 首次编译会下载大量依赖（包括 Android SDK、NDK 等），可能需要较长时间。请确保网络稳定，并耐心等待。

**注意：** 编译过程中可能会遇到各种问题，建议仔细阅读错误信息，逐步排查。