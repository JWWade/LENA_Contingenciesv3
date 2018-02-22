from subprocess import call

pyinstaller --onefile -windowed --icon ../icon/LENACon3-Icon.ico --icon ../icon/LENACon3-Icon.icns --distpath ../. --name "LenaContingencies V3" --paths=/Library/Python/2.7/site-packages  ../src/control.py
