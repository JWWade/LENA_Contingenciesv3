# -*- mode: python -*-

block_cipher = None


a = Analysis(['.foo.py'],
             pathex=['D', 'D', 'envLibsite-packageenvLclearibsite-packages', '/Users/Home/Documents/kol-ij/_Spring_18/CSCI_4700/LENA_Contingenciesv3/testEXEC'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='.foo',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='.foo')
