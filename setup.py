from setuptools import setup, find_packages
import os


def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='avm',
    version='1.0.2',
    packages=find_packages(exclude='tests'),
    url='https://github.com/SevanSSP/avm',
    license='MIT',
    author='Per Voie',
    author_email='pev@sevanssp.com',
    description='Interact with DNV GL Software\'s Application Version Manager',
    long_description=read('README.md'),
    entry_points={
            'console_scripts': [
                'avm-list = avm.entry_points:list_applications',
            ],
        },
)
