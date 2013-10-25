from setuptools import setup, find_packages
from distutils.extension import Extension

# Forces numpy to be installed
import numpy as np

import sys

if 'setuptools.extension' in sys.modules:
    m = sys.modules['setuptools.extension']
    m.Extension.__dict__ = m._Extension.__dict__

packages = find_packages()

classifiers = ''' Intended Audience :: Science/Research
Intended Audience :: Developers
Intended Audience :: Education
Operating System :: OS Independent
Programming Language :: Python
Topic :: Scientific/Engineering
Topic :: Education
Topic :: Software Development :: Libraries :: Python Modules'''


setup(name = 'ooitk', 
        version='2.1.0',
        description='Ocean Observatories Initiative Toolkit',
        long_description=open('README.md').read(),
        license='LICENSE.txt',
        author='Luke Campbell',
        author_email='lcampbell@asascience.com',
        url='https://github.com/ooici/ion-functions/',
        classifiers=classifiers.split('\n'),
        packages=packages,
        keywords=['oceanography', 'seawater'],
        install_requires=[
            'ipython==0.13.0',
            'readline',
        ]
)

