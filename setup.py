"""Setup script"""

from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pastlogging",
    version="1.0a1",
    description="Logging extension to emit full logs when a threshold is reached",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jimstraus/pastlogging",
    author="Jim Straus",
    author_email="jims@keymail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="logging",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    extras_require={"dev": ["check-manifest"], "test": ["pytest", "pytest-cover"]},
)

