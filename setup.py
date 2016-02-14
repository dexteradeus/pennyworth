import os
import sys
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

dependencies = ['future']
if sys.version_info < (3,4):
    dependencies.append('enum34')

setup(
    name = "pennyworth",
    version = "0.1",
    author = "Chris Hand",
    author_email = "dexteradeus@users.noreply.github.com",
    description = ("Python client for A.L.F.R.E.D (Almighty Lightweight Fact "
                  "Remote Exchange Daemon)"),
    license = "MIT",
    keywords = "shell",
    url = "https://github.com/dexteradeus/pennyworth",
    packages=['pennyworth'],
    long_description=read('README.md'),
    install_requires=dependencies,
    test_suite='tests',
    classifiers=[
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)
