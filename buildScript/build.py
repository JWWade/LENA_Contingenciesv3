from subprocess import call

call(["pyinstaller", "--distpath", "../builds/v3/.", "--onefile", "-windowed", "--icon", "../icon/LENACon3-Icon.ico", "--icon", "../icon/LENACon3-Icon.icns", "--name", "LenaContingencies V3", "--paths=/Library/Python/2.7/site-packages", "../src/control.py"])
