# -*- mode: python -*-

block_cipher = None


a = Analysis(['../src/control.py'],
             pathex=['/Library/Python/2.7/site-packages', '/Users/Home/Documents/kol-ij/_Spring_18/CSCI_4700/LENA_Contingenciesv3/buildScript'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='LenaContingencies V3',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='../icon/LENACon3-Icon.icns')
app = BUNDLE(exe,
             name='LenaContingencies V3.app',
             icon='../icon/LENACon3-Icon.icns',
             bundle_identifier=None)
