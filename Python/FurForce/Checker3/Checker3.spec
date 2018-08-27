# -*- mode: python -*-
a = Analysis(['Checker3.py'],
             pathex=['D:\\Python\\Checker3'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts + [('O','','OPTION')],
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Checker3.exe',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='Checker.ico')
