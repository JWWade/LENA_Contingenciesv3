#setup.py
from distutils.core import setup
import py2exe

setup(
	console=['control.py'],
	options = {
		'xlsxwriter': {
			'packages':['xlsxwriter']
		}
	}
)

