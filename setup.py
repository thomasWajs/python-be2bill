from distutils.core import setup
from setuptools import find_packages

setup(
    name='be2bill',
    version='0.0.1',
    author='Thomas Wajs',
    author_email='thomas.wajs@gmail.com',
    packages=find_packages(),
    py_modules=['be2bill_sdk'],
    scripts=[],
    url='http://pypi.python.org/pypi/python-be2bill/',
    license='LICENSE.txt',
    description='An sdk implementing the be2bill API',
    long_description=open('README.md').read(),
    include_package_data=True,
    zip_safe=False,
)
