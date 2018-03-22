from subprocess import call
import os.path
import xlsxwriter
import pandas

# gets the path to where the necessary libraries are installed on your own dev set-up
localPath = os.path.abspath(xlsxwriter.__file__)

# Calls pyinstaller to bundle the app for Mac and Unix

call(["pyinstaller", "--distpath", "../builds/v3/.", \
      "--onefile", "-windowed", "--icon", "../icon/LENACon3-Icon.icns", \
      "--name", "LenaContingencies V3", "--paths="+localPath, "../src/control.py"])


