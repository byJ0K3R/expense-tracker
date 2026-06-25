[app]
title = Учёт расходов
package.name = expensetracker
package.domain = org.expense
source.dir = .
source.include_exts = py,kv,db
version = 1.0

requirements = python3,kivy==2.3.0,sqlite3

orientation = portrait

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
