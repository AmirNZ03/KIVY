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
permissions = INTERNET
api = 33
ndk = 25b
arch = armeabi-v7a
minapi = 21
sdk = 33
build_tools_version = 33.0.2
