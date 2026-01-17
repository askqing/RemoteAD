#!/usr/bin/env python3
"""
RemoteAD Packaging Script
This script handles packaging for both desktop and mobile applications.
"""

import os
import sys
import subprocess

def print_menu():
    """Print the packaging menu."""
    print("=" * 50)
    print("RemoteAD Packaging Script")
    print("=" * 50)
    print()
    print("1. Package Desktop App only")
    print("2. Package Mobile App only")
    print("3. Package Both Desktop and Mobile Apps")
    print()

def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, shell=True)
    if result.returncode != 0:
        print(f"Error: Command failed with exit code {result.returncode}")
        return False
    return True

def activate_venv():
    """Activate the virtual environment."""
    venv_activate = os.path.join("venv", "Scripts", "activate.bat")
    if not os.path.exists(venv_activate):
        print("Creating virtual environment...")
        if not run_command([sys.executable, "-m", "venv", "venv"]):
            return False
    return True

def install_deps(deps):
    """Install Python dependencies."""
    return run_command(["pip", "install"] + deps)

def package_desktop():
    """Package the desktop application."""
    print("\n" + "=" * 50)
    print("Packaging Desktop App")
    print("=" * 50)
    
    # Install dependencies
    if not install_deps(["pyqt5", "pyinstaller"]):
        return False
    
    # Package with PyInstaller
    if not run_command(["pyinstaller", "--onefile", "--windowed", "--name", "RemoteAD", "main_desktop.py"]):
        return False
    
    print("Desktop App Packaging Completed!")
    print(f"Output Path: {os.path.join('dist', 'RemoteAD.exe')}")
    return True

def package_mobile():
    """Package the mobile application."""
    print("\n" + "=" * 50)
    print("Packaging Mobile App")
    print("=" * 50)
    
    # Install dependencies
    if not install_deps(["kivy", "buildozer"]):
        return False
    
    # Create buildozer.spec file
    print("Creating buildozer.spec file...")
    with open("buildozer.spec", "w") as f:
        f.write("[app]\n")
        f.write("title = RemoteAD\n")
        f.write("package.name = remotead\n")
        f.write("package.domain = com.remotead\n")
        f.write("source.dir = .\n")
        f.write("source.include_exts = py,png,jpg,kv,atlas\n")
        f.write("version = 1.0\n")
        f.write("requirements = python3,kivy\n")
        f.write("orientation = landscape\n")
        f.write("[buildozer]\n")
        f.write("log_level = 2\n")
    
    # Package with Buildozer
    if not run_command(["buildozer", "-v", "android", "debug"]):
        return False
    
    print("Mobile App Packaging Completed!")
    print(f"Output Path: {os.path.join('bin', 'remotead-1.0-debug.apk')}")
    return True

def main():
    """Main function."""
    print_menu()
    
    try:
        choice = input("Please select packaging option (1-3): ").strip()
        
        # Validate choice
        if choice not in ["1", "2", "3"]:
            print("Error: Invalid choice!")
            return 1
        
        # Activate virtual environment
        if not activate_venv():
            return 1
        
        # Update pip
        run_command(["python", "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install base requirements
        run_command(["pip", "install", "-r", "requirements.txt"])
        
        # Execute packaging based on choice
        if choice in ["1", "3"]:
            if not package_desktop():
                return 1
        
        if choice in ["2", "3"]:
            if not package_mobile():
                return 1
        
        print("\n" + "=" * 50)
        print("Packaging Process Finished!")
        print("=" * 50)
        input("Press Enter to exit...")
        return 0
        
    except KeyboardInterrupt:
        print("\n\nPackaging process interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())