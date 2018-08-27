# -*- mode: python -*-
a = Analysis(['hwid.py'],
             pathex=['D:\\Programming\\Python\\Reddit'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts + [('O','','OPTION')],
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Reddit.exe',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='Checker.ico')
