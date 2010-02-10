import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='gitblogger',
        version='20100210.1',
        description='Parse strings containing quote-delimited tokens.',
        long_description=read('README.rst'),
        author='Lars Kellogg-Stedman',
        author_email='lars@oddbit.com',
        packages=['pqs'],
        )
