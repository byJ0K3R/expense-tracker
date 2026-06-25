[app]
title = Учёт расходов
package.name = expensetracker
package.domain = org.expense
source.dir = .
source.include_exts = py,kv,db
version = 1.0

requirements = python3,kivy==2.2.1,sqlite3

orientation = portrait

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
