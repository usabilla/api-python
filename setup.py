try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='usabilla',
    version='1.1',
    description="Python client for Usabilla API",
    license='MIT',
    install_requires=['urllib3', 'requests'],
    packages=find_packages(),
    py_modules=['usabilla'],
    author='Usabilla',
    author_email='development@usabilla.com',
    url='https://github.com/usabilla/api-python',
    test_suite='tests'
)
