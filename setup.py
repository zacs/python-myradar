import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="python-myradar",
    version="1.4.0",
    author="Zac Schellhardt",
    author_email="zac.schellhardt@gmail.com",
    description=("A thin Python Wrapper for the MyRadar (Dark Sky replacement) weather API"),
    license="BSD 2-clause",
    keywords="weather API wrapper forecast.io location darksky myradar",
    url="http://github.com/zacs/python-myradar/",
    packages=['myradar'],
    package_data={'myradar': ['LICENSE.txt', 'README.rst']},
    long_description=open('README.rst').read(),
    install_requires=['requests>=1.6', 'responses'],
)
