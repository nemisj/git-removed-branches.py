# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='git-removed-branches',
    version='0.1.0',
    description='Remove local git branches which are no longer available in the remote',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nemisj/git-removed-branches.py',
    author='Maks Nemisj',
    author_email='info@nemisj.com',
    keywords='git branches development tools',
    license='License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    packages=find_packages(),
    python_requires='>=2.7, >=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Pytest',
        'Framework :: Flake8',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD',
        'Operating System :: MacOS :: MacOS X'
    ],
    scripts=['bin/removed-branches'],
    entry_points={
        'console_scripts': [
            'git-removed-branches=main:main',
        ],
    }
)
