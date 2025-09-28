[app]
title = nVweb Browser
package.name = nvweb
package.domain = org.nvweb
version = 0.1
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
main.py = main.py
icon.filename = %(source.dir)s/icon.png
requirements = python3,kivy,kivy_garden.webview
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.permissions = INTERNET
orientation = portrait
fullscreen = 0
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
