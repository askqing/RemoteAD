@echo off
setlocal enabledelayedexpansion

echo ========================================
echo RemoteAD Packaging Script (Windows)
echo ========================================
echo.
echo 1. Package Desktop App only
echo 2. Package Android App only (using python-for-android)
echo 3. Package Both
echo.
set /p choice=Enter your choice (1-3): 

if "%choice%"=="1" goto desktop
if "%choice%"=="2" goto android
if "%choice%"=="3" goto both

echo Invalid choice!
pause
exit /b 1

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
        exit /b 1
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
    echo Desktop app packaged successfully!
    echo Output: dist\RemoteAD.exe
)

goto end

:android
echo.
echo ========================================
echo Packaging Android App
echo ========================================
echo Checking virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo Installing dependencies...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe -m pip install python-for-android

echo Checking Java environment...
java -version >nul 2>&1
if !errorlevel! neq 0 (
    echo Warning: Java not found! Android packaging may fail.
    echo Please install Java JDK 8 or later.
)

echo Creating build directory...
if not exist "android_build" mkdir android_build

echo Packaging Android app...
echo Note: First build will download many dependencies, this may take a long time.
echo Please ensure stable internet connection...

rem Use the p4a command directly
echo Running python-for-android (p4a)...
venv\Scripts\p4a create --dist_name RemoteAD --bootstrap sdl2 --requirements python3,kivy --private . --package com.remotead.remotead --name RemoteAD --version 1.0 --output-dir android_build

if exist "android_build" (
    dir "android_build" >nul 2>&1
    if !errorlevel! equ 0 (
        echo.
        echo Android app packaged successfully!
        echo Output directory: android_build\
        dir "android_build" /b
    ) else (
        echo Error: Android packaging failed, no output files
    )
) else (
    echo Error: Android packaging failed, build directory not created
)

goto end

:both
echo.
echo ========================================
echo Packaging Both Apps
echo ========================================
call :desktop
call :android
goto end

:end
echo.
echo ========================================
echo Packaging Process Completed!
echo ========================================
pause
exit /b 0