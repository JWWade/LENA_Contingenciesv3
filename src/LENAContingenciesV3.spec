# -*- mode: python -*-

block_cipher = None


a = Analysis(['control.py'],
             pathex=['C:\\Users\\Joel\\MTSU\\CSCI_4700\\LENA_Contingenciesv3\\src'],
             binaries=[],
             datas=[],
             hiddenimports=['xlsxwriter'],
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
          name='LENAContingenciesV3',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='..\\icon\\lenacon3_icon.ico')
