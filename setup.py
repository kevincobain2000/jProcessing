#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
setup(
    name = 'jProcessing', #First Level Dir
    version='0.1',
    author='KATHURIA Pulkit',
    author_email='pulkit@jaist.ac.jp',
    packages= find_packages('src'),
    scripts = ['scripts/vcabocha.py'],
    package_dir = {'':'src'},
    package_data = {'': ['data/*'],
    },
    include_package_data = True,
    exclude_package_data = {'': ['jNlp/*.p']},
    url='http://www.jaist.ac.jp/~s1010205',
    license='LICENSE.txt',
    description='Japanese NLP Utilities',
    long_description=open('README').read(),
    classifiers=['Development Status :: 2 - Pre-Alpha','Natural Language :: Japanese',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence'],
                 
    )

"""
File System
===========
jNlp/
    setup.py
    README
    LICENCE.txt
    scripts/
      ...
    src/
      jNlp/
          __init__.py
          jCabocha.py #see foo.py to check how to access somefile.dat
          jTokenize.py
          jConvert.py
          jColor.py
          edict_search.py
          edict_examples.py
          jSentiments.py
          
          classifiers/
            ..
          data/
            katakanaChart.txt
            hiraganaChart.txt
            edict dictionary files *not included*
          jnlp/
            *not with this package*#see MANIFEST.in
              ...
          _dicts/
            dict files *NA*
"""
