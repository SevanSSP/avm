from setuptools import setup, find_packages

setup(
    name='avm',
    version='0.1.0',
    packages=find_packages(exclude='tests'),
    url='https://github.com/SevanSSP/avm',
    license='MIT',
    author='Per Voie',
    author_email='pev@sevanssp.com',
    description='Interact with DNV GL Software\'s Application Version Manager'
)
