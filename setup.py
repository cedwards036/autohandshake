import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.txt").read_text()

# This call to setup() does all the work
setup(
    name="autohandshake",
    version="1.0.0",
    description="A library for automating tasks on the Handshake career services platform",
    long_description=README,
    url="https://github.com/cedwards036/autohandshake",
    author="Christopher Edwards",
    author_email="cedwards036@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["autohandshake"],
    include_package_data=True,
    install_requires=['selenium', 'bs4']
)
