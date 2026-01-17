@echo off
setlocal enabledelayedexpansion

echo ========================================
echo RemoteAD 打包脚本（Windows最终版）
echo ========================================
echo.
echo 1. 仅打包桌面应用（推荐，已测试可用）
echo 2. 准备Kivy Launcher应用文件（无需编译APK）
echo 3. 退出

echo.
echo 注意：在Windows上无法直接生成Android APK文件！
echo 原因：python-for-android依赖的sh库不支持Windows系统。
echo 推荐方案：使用Kivy Launcher在Android设备上直接运行应用。
echo 高级方案：使用WSL（Windows子系统Linux）或Linux虚拟机构建APK。
echo.

set /p choice=请选择选项 (1-3): 

if "%choice%"=="1" goto desktop
if "%choice%"=="2" goto kivy_launcher
if "%choice%"=="3" goto end

echo 无效选项！
pause
goto end

:desktop
echo.
echo ========================================
echo 正在打包桌面应用
echo ========================================
echo 检查虚拟环境...

if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo 错误: 创建虚拟环境失败
        pause
        goto end
    )
)

echo 安装桌面应用依赖...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe -m pip install pyqt5 pyinstaller

echo 开始打包桌面应用...
venv\Scripts\python.exe -m pyinstaller --onefile --windowed --name RemoteAD main_desktop.py

if !errorlevel! neq 0 (
    echo 错误: 打包桌面应用失败
) else (
    echo 成功: 桌面应用打包完成！
    echo 输出文件: %cd%\dist\RemoteAD.exe
)

goto end

:kivy_launcher
echo.
echo ========================================
echo 正在准备Kivy Launcher应用文件
echo ========================================
echo 这将创建一个可以直接在Android设备上运行的应用文件夹。
echo 您需要：
echo 1. 在Android设备上安装Kivy Launcher（从Google Play商店）
echo 2. 将生成的KivyRemoteAD文件夹复制到设备的Download目录
echo 3. 打开Kivy Launcher应用，您的应用将显示在列表中
echo.

set /p confirm=是否继续？(Y/N): 
if /i "%confirm%" neq "Y" goto end

echo 创建Kivy RemoteAD应用文件夹...

if exist "KivyRemoteAD" (
    echo 删除旧的应用文件夹...
    rmdir /s /q "KivyRemoteAD"
)

mkdir "KivyRemoteAD"
mkdir "KivyRemoteAD\core"
mkdir "KivyRemoteAD\services"
mkdir "KivyRemoteAD\ui"

rem 复制核心文件
echo 复制核心文件...
echo 正在复制主程序文件...
copy "main_mobile.py" "KivyRemoteAD\main.py" >nul
echo 正在复制核心模块...
xcopy /E /I /Q "core" "KivyRemoteAD\core" >nul
echo 正在复制服务模块...
xcopy /E /I /Q "services" "KivyRemoteAD\services" >nul
echo 正在复制UI模块...
xcopy /E /I /Q "ui" "KivyRemoteAD\ui" >nul
echo 正在复制依赖文件...
copy "requirements.txt" "KivyRemoteAD\requirements.txt" >nul

echo 成功: Kivy Launcher应用文件准备完成！
echo 应用文件夹: %cd%\KivyRemoteAD

echo.
echo 使用说明：
echo 1. 在Android设备上安装 Kivy Launcher

echo 2. 将 KivyRemoteAD 文件夹复制到设备的 Download 目录
echo 3. 打开 Kivy Launcher 应用
echo 4. 您的应用将显示在列表中，点击即可运行
echo.
echo 注意：第一次运行可能需要较长时间加载依赖。

goto end

:end
echo.
echo ========================================
echo 打包流程完成！
echo ========================================
pause