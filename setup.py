import sys

import os
from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 5)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        "This version of CodeSkulptor requires Python {}.{}, but you're trying to install it on Python {}.{}.".format(
            *REQUIRED_PYTHON, *CURRENT_PYTHON
        )
    )
    sys.exit(1)


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


from codeskulptor import __version__

EXCLUDE_FROM_PACKAGES = [
    'codeskulptor.bin',
]

setup(
    name='CodeSkulptor',
    version=__version__,
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    url='https://github.com/uadnan/CodeSkulptor',
    author='Adnan Umer',
    author_email='u.adnan@outlook.com',
    description='Unofficial CodeSkulptor Local Server',
    long_description=read('README.rst'),
    license='MIT',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    scripts=[
        'codeskulptor/bin/codeskulptor-py2.py',
        'codeskulptor/bin/codeskulptor-py3.py'
    ],
    entry_points={'console_scripts': [
        'codeskulptor-py2 = codeskulptor.interface:run_py2',
        'codeskulptor-py3 = codeskulptor.interface:run_py3',
    ]},
    install_requires=[
        'bs4',
        'multipart',
        'requests'
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only'
    ],
    project_urls={
        'Source': 'https://github.com/uadnan/CodeSkulptor',
        'Tracker': 'https://github.com/uadnan/CodeSkulptor/issues',
    },
)
