import os
from setuptools import find_packages, setup


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
        'beautifulsoup4',
        'multipart',
        'requests'
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
