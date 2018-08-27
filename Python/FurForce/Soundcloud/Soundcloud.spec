# -*- mode: python -*-
a = Analysis(['Soundcloud.py'],
             pathex=['D:\\Python\\FurForce\\Soundcloud'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts + [('O','','OPTION')],
          a.binaries,
          a.zipfiles,
          a.datas,
          name='FurForce Soundcloud.exe',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='Checker.ico')
