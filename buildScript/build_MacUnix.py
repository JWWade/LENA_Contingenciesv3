"""
The MIT License (MIT)
Copyright (c) 2018 Paul Yoder, Joshua Wade, Kenneth Bailey, Mena Sargios, Joseph Hull, Loraina Lampley, John Peden,
Bishoy Boktor, Kate Lovett, Joel Norris, Joseph London, Jesse Offei-nkansah

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

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


