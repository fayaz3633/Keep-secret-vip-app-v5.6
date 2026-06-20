[app]

# (str) Title of your application
title = Keep Secret VIP

# (str) Package name
package.name = keepsecretvip

# (str) Package domain (needed for android packaging)
package.domain = org.fayaz.wallet

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,db,json

# (str) Application version
version = 1.0.0

# (list) Application requirements
# خالص اور لائٹ ویٹ pycryptodome، بغیر کسی ورژن کے جھنجھٹ کے
requirements = python3,kivy,pycryptodome

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
# آپ کی تجویز کے مطابق ماڈرن پلے اسٹور UI کے لیے 0 سیٹ کر دیا ہے
fullscreen = 0

# =============================================================================
# Android specific configurations
# =============================================================================

# (list) Permissions for Intruder Capture and Security
android.permissions = CAMERA, VIBRATE

# (int) Target Android API (Android 13)
android.api = 33

# (int) Minimum API your APK will support (Android 7.0)
android.minapi = 24

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) Automatically accept SDK license agreements
android.accept_sdk_license = True

# (list) Android architectures to build for (Modern 64-bit devices)
android.archs = arm64-v8a

# (bool) Use ccache to speed up compilation
android.ccache = 1

# =============================================================================
# Buildozer configurations
# =============================================================================

[buildozer]

# (int) Log level (2 = debug)
log_level = 2
