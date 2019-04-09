#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup
import os
import sys

if sys.version_info < (3, 5):
    sys.exit('Sorry, Python < 3.5 is not supported.')
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('vitae/__init__.py', 'rb') as fid:
    for line in fid:
        line = line.decode('utf-8')
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break

download_url = ('https://github.com/josephcslater/vitae/\
                blob/master/dist/vitae-' + version + '.whl')


setup(name='vitae',
      version=version,
      description=('Tools for academics for building a Curriculum Vitae and other oft-requested documents.'),
      author=u'Joseph C. Slater',
      author_email='joseph.c.slater@gmail.com',
      url='https://github.com/josephcslater/vitae',
      packages=['vitae'],
      package_data={'vitae': ['../readme.rst', 'data/*.bib'],
                    '': ['readme.rst']},
      long_description=read('readme.rst'),
      keywords=['curriculum vitae', 'academia', 'cv', 'resume'],
      install_requires=['bibtexparser', 'appdirs'],
      include_package_data=True
      )

# https://docs.python.org/3/distutils/setupscript.html#additional-meta-data
