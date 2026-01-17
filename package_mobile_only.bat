@echo off
echo Creating Mobile App...

rem Create virtual environment
echo Creating virtual environment...
python -m venv venv --clear

rem Activate virtual environment and install dependencies
echo Installing dependencies...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install kivy buildozer

rem Create buildozer.spec file
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

rem Build the mobile app
echo Building mobile app...
venv\Scripts\python.exe -m buildozer -v android debug

echo Mobile app build completed!
echo APK file should be in bin\ directory if successful.
pause