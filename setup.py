from setuptools import setup
from os import path
import os

root = path.abspath(path.dirname(__file__))
with open(path.join(root, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

version = os.getenv("PYPI_VERSION")

if not version:
  raise Exception("PYPI_VERSION not defined")

setup(
  name = 'pluralizer',
  packages = ['pluralizer'],
  version = version,
  platforms='any',
  license='MIT',
  description = 'Singularize or pluralize a given word useing a pre-defined list of rules',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Wei Xu',
  url = 'https://github.com/weixu365/pluralizer-py',
  python_requires='>=3',
  keywords = ['pluralize', 'singularize', 'singular', 'plural'],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
  ],
)
