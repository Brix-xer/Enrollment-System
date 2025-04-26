# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['login.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('images', 'images'),  # Ensure images are included
        ('images/*', 'images'),  # Include all image files
    ],
    hiddenimports=[
        'mysql.connector.locales.eng.client_error',
        'mysql.connector.plugins.mysql_native_password',
        'babel.numbers',
        'babel.core',
        'babel.dates',
        'babel.localedata',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='HihoSystem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Hide console
    icon='HiHo.ico',  # Add application icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='HihoSystem'
)
