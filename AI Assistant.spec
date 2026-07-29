# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all
import certifi

datas = []
binaries = []
hiddenimports = []

packages = [
    "gradio",
    "gradio_client",
    "safehttpx",
    "groq",
    "groovy",
    "pydantic",
    "pydantic_core",
]

for pkg in packages:
    try:
        d, b, h = collect_all(pkg)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception as e:
        print(f"Warning: Could not collect {pkg}: {e}")

# Include SSL certificates
datas += [
    (certifi.where(), "certifi"),
]

# Extra hidden imports
hiddenimports += [
    "pydantic",
    "pydantic_core",
    "pydantic_core._pydantic_core",
    "email_validator",
    "annotated_types",
    "typing_extensions",
    "certifi",
]

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    [],
    exclude_binaries=True,
    name="AI Assistant",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,          # Change to False after everything works
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="AI Assistant",
)