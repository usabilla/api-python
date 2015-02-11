try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='usabilla',
    version='1.0',
    description="Python client for Usabilla API",
    license='MIT',
    install_requires=['urllib3', 'requests'],
    packages=find_packages(),
    py_modules=['usabilla'],
    author='George V.',
    author_email='george@usabilla.com',
    url='http://usabilla.com/api',
    test_suite='tests'
)
