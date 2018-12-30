"""
Setup script.

"""

import os
import sys

from setuptools import find_packages
try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

import pyxpiral

def read(fname):
	"""
	Utility function to read the README file. README file is used to create
	the long description.
	"""

	return open(os.path.join(os.path.dirname(__file__), fname)).read()

VERSION = pyxpiral.__version__
NAME = "pyxpiral"
DESCRIPTION = "Pyxpiral Pseudo-DataMatrix (de)coder"

AUTHOR = "elcodedocle"
AUTHOR_EMAIL = "gael.abadin@gmail.com"
URL = "http://github.com/elcodedocle/pyxpiral/"

LICENSE = read('LICENSE')

CLASSIFIERS = [
	"Development Status :: 4 - Beta",
	"Environment :: Console",
	"Intended Audience :: UnitedWarriorsOfTheWorld",
	"License :: MIT",
	"Natural Language :: English",
	"Operating System :: Unix",
	"Operating System :: Microsoft :: Windows",
	"Programming Language :: Python :: 2.7",
	"Programming Language :: Python :: 3.7",
	"Programming Language :: Python :: 2",
	"Programming Language :: Python :: 3",
]

SCRIPTS = []

DEPENDENCIES = read('requirements.txt').split()

PACKAGE_DATA = {}
DATA_FILES = []

REQUIRED_VERSION = '2.7'

SETUP_PARAMS = dict(
	name=NAME,
	version=VERSION,
	description=DESCRIPTION,

	author=AUTHOR,
	author_email=AUTHOR_EMAIL,
	url=URL,
	long_description=read('README.md'),
	packages=find_packages(),
	package_data=PACKAGE_DATA,
	license=LICENSE,
	scripts=SCRIPTS,
	data_files=DATA_FILES,
	install_requires=DEPENDENCIES,
	classifiers=CLASSIFIERS,
)

def main():
	"""
	Setup.py main.
	"""

	if sys.version < REQUIRED_VERSION:
		print '%s %s requires Python %s or later'%(NAME, VERSION, REQUIRED_VERSION)
		sys.exit(-1)

	setup(**SETUP_PARAMS)

if __name__ == "__main__":
	main()
