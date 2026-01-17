@echo off
setlocal enabledelayedexpansion

echo ========================================
echo 基于Python的跨平台局域网远程控制软件打包脚本
echo ========================================
echo.
echo 1. 仅打包桌面应用
echo 2. 仅打包移动应用
echo 3. 同时打包桌面和移动应用
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
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo 错误: 创建虚拟环境失败
        pause
        exit /b 1
    )
)

rem 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat
if !errorlevel! neq 0 (
    echo 错误: 激活虚拟环境失败
    pause
    exit /b 1
)

rem 更新pip
echo 更新pip...
python -m pip install --upgrade pip

rem 安装基础依赖
echo 安装基础依赖...
pip install -r requirements.txt

rem 处理桌面应用打包
if !choice! equ 1 (goto desktop)
if !choice! equ 3 (goto desktop)
goto skip_desktop

:desktop
rem 安装桌面应用依赖
echo 安装桌面应用依赖...
pip install pyqt5
pip install pyinstaller

rem 打包桌面应用
echo 打包桌面应用...
pyinstaller --onefile --windowed --name RemoteAD --icon=icon.ico main_desktop.py

if !errorlevel! neq 0 (
    echo 错误: 打包桌面应用失败
    pause
    exit /b 1
)

echo 桌面应用打包完成！
echo 输出路径: dist\RemoteAD.exe

:skip_desktop

rem 处理移动应用打包
if !choice! equ 2 (goto mobile)
if !choice! equ 3 (goto mobile)
goto skip_mobile

:mobile
rem 安装移动应用依赖
echo 安装移动应用依赖...
pip install kivy
pip install buildozer

rem 创建Buildozer配置文件
echo 创建Buildozer配置文件...
echo [app] > buildozer.spec
echo title = RemoteAD >> buildozer.spec
echo package.name = remotead >> buildozer.spec
echo package.domain = com.remotead >> buildozer.spec
echo source.dir = . >> buildozer.spec
echo source.include_exts = py,png,jpg,kv,atlas >> buildozer.spec
echo version = 1.0 >> buildozer.spec
echo requirements = python3,kivy >> buildozer.spec
echo orientation = landscape >> buildozer.spec
echo osx.python_version = 3.8 >> buildozer.spec
echo osx.kivy_version = 2.0.0 >> buildozer.spec
echo fullscreen = 0 >> buildozer.spec
echo android.api = 27 >> buildozer.spec
echo android.sdk = 24 >> buildozer.spec
echo android.ndk = 17 >> buildozer.spec
echo android.arch = armeabi-v7a >> buildozer.spec
echo android.buildtools = 28.0.3 >> buildozer.spec
echo android.use_aapt2 = True >> buildozer.spec
echo android.skip_update = False >> buildozer.spec
echo android.accept_sdk_license = True >> buildozer.spec
echo android.logcat_filters = *:S python:D >> buildozer.spec
echo log_level = 2 >> buildozer.spec
echo [buildozer] >> buildozer.spec
echo log_level = 2 >> buildozer.spec

rem 打包移动应用
echo 打包移动应用...
buildozer -v android debug

if !errorlevel! neq 0 (
    echo 错误: 打包移动应用失败
    pause
    exit /b 1
)

echo 移动应用打包完成！
echo 输出路径: bin\remotead-1.0-debug.apk

:skip_mobile

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