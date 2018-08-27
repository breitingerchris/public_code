# -*- mode: python -*-
a = Analysis(['HWID.py'],
             pathex=['D:\\Python\\FurForce\\Checker3'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='HWID.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
