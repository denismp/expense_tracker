# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('static', 'static'), ('expense_tracker/templates', 'expense_tracker/templates'), ('expense_tracker/apps/expenses/templates', 'expense_tracker/apps/expenses/templates'), ('expense_tracker/apps/accounts/templates', 'expense_tracker/apps/accounts/templates'), ('db.sqlite3', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ExpenseTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['/Users/denisputnam/git/expense_tracker/icons/icon.icns'],
)
app = BUNDLE(
    exe,
    name='ExpenseTracker.app',
    icon='/Users/denisputnam/git/expense_tracker/icons/icon.icns',
    bundle_identifier='com.denisputnam.expense-tracker',
)
