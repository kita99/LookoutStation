from setuptools import setup, find_packages

requirements = open('requirements.txt', 'r')

setup(
    name='lookoutstation-api',
    version='1.0',
    packages=find_packages(),
    install_requires=[r for r in requirements.read().split('\n')]
)
