import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "Carrotron2",
    version = "0.0.2",
    author = "Alexander Lloyd",
    author_email = "axl639@student.bham.ac.uk",
    description = ("Declarative Robotics Library"),
    keywords = "Robotics",
    url = "https://github.com/alexander-lloyd/Carrotron2.git",
    packages=find_packages(),
    install_requires=required,
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
)
