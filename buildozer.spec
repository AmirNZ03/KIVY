[app]

# نام اپلیکیشن
title = MyApp
# package name (بدون فاصله و فقط انگلیسی)
package.name = myapp
# domain دلخواه
package.domain = org.example
# مسیر سورس کد
source.dir = .
# فایل‌هایی که شامل می‌شوند
source.include_exts = py,png,jpg,kv,atlas
# نسخه اپ
version = 0.1
# فایل اصلی برنامه
entrypoint = main_kivy.py

# Android
[buildozer]

# بدون پرسش root
android.permissions = INTERNET
android.api = 33
android.ndk = 25b
android.arch = armeabi-v7a
android.minapi = 21
android.sdk = 33
