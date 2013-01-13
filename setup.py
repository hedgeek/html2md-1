#!/usr/bin/env python
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__author__ = 'Max Arnold <arnold.maxim@gmail.com>'
__version__ = '0.1'

setup(
    name='html2md',
    version=__version__,

    # Packaging options.
    include_package_data=True,

    # Package dependencies.
    install_requires=['lxml'],

    # Metadata for PyPI.
    author='Max Arnold',
    author_email='arnold.maxim@gmail.com',
    license='BSD',
    url='https://bitbucket.org/marnold/html2md',
    keywords='html markdown converter',
    description='HTML to Markdown converter.',
    long_description=open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'README.md')), 'rb').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup',
    ]
    packages=[
        'html2md',
    ],
    platforms='any'
)
