@echo off
echo ========================================
echo RemoteAD Packaging Script
echo ========================================
echo.
echo 1. Package Desktop App only
echo 2. Package Mobile App only
echo 3. Package Both Desktop and Mobile Apps
echo.
set /p choice=Please select packaging option (1-3): 

if "%choice%"=="1" goto desktop
if "%choice%"=="2" goto mobile
if "%choice%"=="3" goto both

echo Error: Invalid choice!
pause
exit /b 1

:desktop
echo Starting Desktop App Packaging...
call venv\Scripts\activate.bat
pip install pyqt5 pyinstaller
pyinstaller --onefile --windowed --name RemoteAD main_desktop.py
echo Desktop App Packaging Completed!
echo Output Path: dist\RemoteAD.exe
goto end

:mobile
echo Starting Mobile App Packaging...
call venv\Scripts\activate.bat
pip install kivy buildozer
echo Creating buildozer.spec file...
echo [app] > buildozer.spec
echo title = RemoteAD >> buildozer.spec
echo package.name = remotead >> buildozer.spec
echo package.domain = com.remotead >> buildozer.spec
echo source.dir = . >> buildozer.spec
echo source.include_exts = py,png,jpg,kv,atlas >> buildozer.spec
echo version = 1.0 >> buildozer.spec
echo requirements = python3,kivy >> buildozer.spec
echo orientation = landscape >> buildozer.spec
echo [buildozer] >> buildozer.spec
echo log_level = 2 >> buildozer.spec
buildozer -v android debug
echo Mobile App Packaging Completed!
echo Output Path: bin\remotead-1.0-debug.apk
goto end

:both
echo Starting Both Apps Packaging...
call venv\Scripts\activate.bat
pip install pyqt5 pyinstaller kivy buildozer
pyinstaller --onefile --windowed --name RemoteAD main_desktop.py
echo Creating buildozer.spec file...
echo [app] > buildozer.spec
echo title = RemoteAD >> buildozer.spec
echo package.name = remotead >> buildozer.spec
echo package.domain = com.remotead >> buildozer.spec
echo source.dir = . >> buildozer.spec
echo source.include_exts = py,png,jpg,kv,atlas >> buildozer.spec
echo version = 1.0 >> buildozer.spec
echo requirements = python3,kivy >> buildozer.spec
echo orientation = landscape >> buildozer.spec
echo [buildozer] >> buildozer.spec
echo log_level = 2 >> buildozer.spec
buildozer -v android debug
echo Both Apps Packaging Completed!
goto end

:end
echo ========================================
echo Packaging Process Finished!
echo ========================================
pause