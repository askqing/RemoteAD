[app]
title = RemoteAD
package.name = remotead
package.domain = com.remotead
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
# Use specific versions to avoid compatibility issues
requirements = python3,kivy==2.1.0,pillow==9.5.0,pyyaml==6.0,cython==0.29.35,pycryptodome
orientation = landscape

# Android specific
android.api = 31
# Use the recommended NDK version from p4a logs: 25b
android.ndk = 25b
android.archs = armeabi-v7a,arm64-v8a
android.accept_sdk_license = True
android.gradle_dependencies =
android.enable_androidx = True
android.enable_jetifier = True
# Add necessary permissions
android.permissions = INTERNET,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,ACCESS_NETWORK_STATE

[buildozer]
log_level = 2
warn_on_root = 1
download_cache_dir = ./.buildozer/cache
download_cache = True
# Increase download timeout to handle network issues
download_timeout = 300
# Use a more reliable download method
use_new_download = True
# Use gradle build instead of ant
android.use_gradle = True
# Skip building aab for now
android.build_aab = False
# Use legacy builder for better compatibility
android.legacy_api = True
# Clean build every time to avoid cached issues
android.clean_build = True 
