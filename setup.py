import os
from setuptools import setup, find_packages

import mcollector

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='async-metrics-collector',
    version=mcollector.__version__,
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A simple metrics collector.',
    long_description=README,
    author='Yaroslav Klyuyev',
    author_email='imposeren@gmail.com',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=[
        'python-daemon >= 2.1.0, <  2.2.0',
        'six >= 1.9, <  2.0',
        'psutil >= 4.0.0, < 4.1.0',
        'tinydb >= 3.1.0, < 3.2.0',
    ],
    entry_points={
        'console_scripts': 'mcollector = mcollector.handler:main'
    }
)
