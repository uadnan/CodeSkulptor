import os
import shutil
import sys
import tempfile
import zipfile

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

from codeskulptor import __version__


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


GITHUB_RELEASE = "2018.09.16"
REQUESTS_LIB = "requests==2.22.0"
EXCLUDE_FROM_PACKAGES = [
    'codeskulptor.bin',
]


def download_file(url):
    directory = tempfile.mkdtemp()
    local_filename = os.path.join(directory, "www.zip")

    try:
        import requests
    except ImportError:
        os.system('"{}" -m pip install "{}"'.format(sys.executable, REQUESTS_LIB))

        import requests

    r = requests.get(url, stream=True, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) Chrome/69.0.3497.92 Safari/537.36",
        "Accept": "text/html,*/*"
    })
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return local_filename


def clean_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)


class PostInstallCommand(install):
    def run(self):
        from codeskulptor import WWW_ROOT

        clean_directory(os.path.join(WWW_ROOT, "py2"))
        clean_directory(os.path.join(WWW_ROOT, "py3"))

        local_zip_path = None
        try:
            local_zip_path = download_file(
                "https://github.com/uadnan/CodeSkulptor/releases/download/{}/www.zip".format(GITHUB_RELEASE)
            )

            with zipfile.ZipFile(local_zip_path, "r") as f:
                f.extractall(WWW_ROOT)
        finally:
            if os.path.exists(local_zip_path):
                os.remove(local_zip_path)

        install.run(self)


class PostDevelopCommand(develop):
    def run(self):
        from codeskulptor.interface import run_grabber

        run_grabber()
        develop.run(self)


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
        'beautifulsoup4==4.8.0',
        'multipart==0.2',
        REQUESTS_LIB
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
