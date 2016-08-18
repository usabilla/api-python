try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

VERSION = '1.2.1'

setup(
    name='usabilla-api',
    version=VERSION,
    description="Python client for Usabilla API",
    license='MIT',
    install_requires=['urllib3', 'requests'],
    packages=find_packages(),
    py_modules=['usabilla'],
    author='Usabilla',
    author_email='development@usabilla.com',
    url='https://github.com/usabilla/api-python',
    download_url='https://github.com/usabilla/api-python/tarball/%s' % VERSION,
    test_suite='tests'
)
