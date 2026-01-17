@echo off
setlocal enabledelayedexpansion

echo ========================================
echo RemoteAD 打包脚本（Windows版 + p4a）
echo ========================================
echo.
echo 1. 仅打包桌面应用
echo 2. 仅打包Android应用（使用Python for Android）
echo 3. 同时打包桌面和Android应用
echo.
set /p choice=请选择打包选项 (1-3): 

if not defined choice (
    echo 错误: 请输入有效的选项
    pause
    exit /b 1
)

if !choice! lss 1 goto invalid
if !choice! gtr 3 goto invalid

echo.
echo 开始打包流程...

rem 检查Python环境
echo 检查Python环境...
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo 错误: 未找到Python环境
    pause
    exit /b 1
)

rem 检查并创建虚拟环境
echo 检查虚拟环境...
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo 错误: 创建虚拟环境失败
        pause
        exit /b 1
    )
)

rem 激活虚拟环境并安装基础依赖
echo 激活虚拟环境并安装依赖...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt

rem 处理桌面应用打包
if !choice! equ 1 if !choice! equ 3 (
    echo.
echo ========================================
echo 打包桌面应用
echo ========================================
echo 安装桌面应用依赖...
venv\Scripts\python.exe -m pip install pyqt5 pyinstaller

    rem 打包桌面应用
echo 打包桌面应用...
venv\Scripts\python.exe -m pyinstaller --onefile --windowed --name RemoteAD main_desktop.py

    if !errorlevel! neq 0 (
        echo 错误: 打包桌面应用失败
    ) else (
        echo 桌面应用打包完成！
        echo 输出路径: dist\RemoteAD.exe
    )
)

rem 处理Android应用打包
if !choice! equ 2 if !choice! equ 3 (
    echo.
echo ========================================
echo 打包Android应用（使用Python for Android）
echo ========================================
echo 安装Python for Android...
venv\Scripts\python.exe -m pip install python-for-android

    rem 检查是否已安装Java JDK 8或以上
echo 检查Java环境...
java -version >nul 2>&1
if !errorlevel! neq 0 (
        echo 警告: 未找到Java环境，Android打包可能失败
        echo 请安装Java JDK 8或以上版本
    ) else (
        java -version 2>&1 | findstr /i "version" >nul
        if !errorlevel! equ 0 (
            echo Java环境检查通过
        )
    )

    rem 打包Android应用
echo 开始打包Android应用...
echo 注意：首次打包需要下载大量依赖，可能需要较长时间
echo 请确保您的网络连接稳定...

    rem 创建Android构建目录
    if not exist "android_build" mkdir android_build

    rem 运行Python for Android打包
echo 执行Python for Android构建...
venv\Scripts\python.exe -c "
import os
import sys

try:
    from pythonforandroid.build import Context
    from pythonforandroid.recipe import Recipe
    from pythonforandroid.distribution import Distribution
    
    print('Python for Android 导入成功')
    print('开始创建构建上下文...')
    
    # 使用命令行方式运行，更可靠
    os.system('venv\\Scripts\\python.exe -m pythonforandroid create --dist_name RemoteAD --bootstrap sdl2 --requirements python3,kivy --private . --package com.remotead.remotead --name RemoteAD --version 1.0 --ndk-api 21 --arch armeabi-v7a --output-dir android_build')
    
except Exception as e:
    print(f'构建过程中出错: {str(e)}')
    print('尝试使用简化命令...')
    os.system('venv\\Scripts\\python.exe -m pythonforandroid create --dist_name RemoteAD --bootstrap sdl2 --requirements python3,kivy --private . --package com.remotead.remotead --name RemoteAD --version 1.0')
"

    rem 检查构建结果
    if exist "android_build" (
        dir "android_build" /b >nul 2>&1
        if !errorlevel! equ 0 (
            echo.
echo Android应用打包完成！
echo 输出目录: android_build\
            dir "android_build" /b
        ) else (
            echo 错误: Android应用打包失败，未生成输出文件
        )
    ) else (
        echo 错误: Android应用打包失败，未创建构建目录
    )
)

echo.
echo ========================================
echo 打包流程完成！
echo ========================================
pause

exit /b 0

:invalid
echo 错误: 请输入1-3之间的数字
pause
exit /b 1