# -*- mode: python ; coding: utf-8 -*-

added_files = [
    ("./Resource/Data/*", "Resource/Data"),
    ("./Resource/Entity/*", "Resource/Entity"),
    ("./Resource/Image/*", "Resource/Image"),
    ("./Resource/System/*", "Resource/System"),
    ("./Resource/Ui/Font/*", "Resource/Ui/Font")
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['__pycache__'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Bug Knights Shooting Edition',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='./Resource/Image/bug_knights.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Bug Knights SE',
)
