[app]
title = MyApp
package.name = myapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
entrypoint = main_kivy.py

[buildozer]
log_level = 2


[app.android]
android.gradle = True
permissions = INTERNET
api = 33
sdk = 33
ndk = 25b
arch = arm64-v8a
minapi = 21
build_tools_version = 33.0.2
