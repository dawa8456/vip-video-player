[app]
title = VIP视频播放器
package.name = vipplayer
package.domain = com.dawa8456
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# 核心依赖：必须包含 kivy 和用来调安卓底层接口的 pyjnius
requirements = python3,kivy==2.3.0,pyjnius

orientation = portrait
osx.kivy_version = 2.3.0

# 核心权限：安卓App必须申请网络权限才能解析视频
android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.ndk_api = 21
android.private_storage = True
android.paddles = False

[buildozer]
log_level = 2
warn_on_root = 0