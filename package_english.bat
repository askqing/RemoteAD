@echo off
setlocal enabledelayedexpansion

echo ========================================
echo RemoteAD Packaging Script (Windows Final)
echo ========================================
echo.
echo 1. Package Desktop App only (Recommended, Tested)
echo 2. Prepare Kivy Launcher Files (No APK Compilation Needed)
echo 3. Exit

echo.
echo IMPORTANT: Cannot generate Android APK directly on Windows!
echo Reason: python-for-android depends on the 'sh' library which only supports Linux/macOS.
echo Recommended Solution: Use Kivy Launcher to run the app directly on Android devices.
echo Advanced Solution: Use WSL (Windows Subsystem for Linux) or Linux VM to build APK.
echo.

set /p choice=Enter your choice (1-3): 

if "%choice%"=="1" goto desktop
if "%choice%"=="2" goto kivy_launcher
if "%choice%"=="3" goto end

echo Invalid choice!
pause
goto end

:desktop
echo.
echo ========================================
echo Packaging Desktop App
echo ========================================
echo Checking virtual environment...

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo Error: Failed to create virtual environment
        pause
        goto end
    )
)

echo Installing desktop dependencies...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe -m pip install pyqt5 pyinstaller

echo Packaging desktop app...
venv\Scripts\python.exe -m pyinstaller --onefile --windowed --name RemoteAD main_desktop.py

if !errorlevel! neq 0 (
    echo Error: Failed to package desktop app
) else (
    echo Success: Desktop app packaged successfully!
    echo Output file: %cd%\dist\RemoteAD.exe
)

goto end

:kivy_launcher
echo.
echo ========================================
echo Preparing Kivy Launcher Files
echo ========================================
echo This will create a folder that can be run directly on Android devices.
echo You need to:
echo 1. Install Kivy Launcher on your Android device (from Google Play Store)
echo 2. Copy the generated KivyRemoteAD folder to your device's Download directory
echo 3. Open Kivy Launcher app, your app will be listed there
echo.

set /p confirm=Continue? (Y/N): 
if /i "%confirm%" neq "Y" goto end

echo Creating Kivy RemoteAD app folder...

if exist "KivyRemoteAD" (
    echo Removing old app folder...
    rmdir /s /q "KivyRemoteAD"
)

mkdir "KivyRemoteAD"
mkdir "KivyRemoteAD\core"
mkdir "KivyRemoteAD\services"
mkdir "KivyRemoteAD\ui"

rem Copy core files
echo Copying core files...
echo Copying main program file...
copy "main_mobile.py" "KivyRemoteAD\main.py" >nul
echo Copying core modules...
xcopy /E /I /Q "core" "KivyRemoteAD\core" >nul
echo Copying service modules...
xcopy /E /I /Q "services" "KivyRemoteAD\services" >nul
echo Copying UI modules...
xcopy /E /I /Q "ui" "KivyRemoteAD\ui" >nul
echo Copying requirements file...
copy "requirements.txt" "KivyRemoteAD\requirements.txt" >nul

echo Success: Kivy Launcher files prepared!
echo App folder: %cd%\KivyRemoteAD

echo.
echo Usage Instructions:
echo 1. Install Kivy Launcher on your Android device
echo 2. Copy the KivyRemoteAD folder to your device's Download directory
echo 3. Open Kivy Launcher app
echo 4. Your app will be listed, click to run
echo.
echo Note: First run may take longer to load dependencies.

goto end

:end
echo.
echo ========================================
echo Packaging Process Completed!
echo ========================================
pause