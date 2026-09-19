# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(SPECPATH)

a = Analysis(
    [str(ROOT / "tools" / "gui.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        (str(ROOT / "fonts"), "fonts"),
        (str(ROOT / "icons"), "icons"),
    ],
    hiddenimports=["PIL._tkinter_finder"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="aurebesh-translator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,   # no terminal window
    disable_windowed_traceback=False,
    argv_emulation=False,
    # .ico is a Windows-only resource; PyInstaller ignores `icon` on Linux,
    # where the window's own icon (set via iconphoto in gui.py) is what
    # shows in the taskbar.
    icon=str(ROOT / "icons" / "icon.ico") if sys.platform.startswith("win") else None,
)
