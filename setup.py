#!/usr/bin/env python 

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "Polynomial", # Replace with your own username
    version = "0.1.0",
    author = "Róisín Grannell",
    author_email = "r.grannell2@gmail.com",
    description = "This repository includes code to solve and graph large numbers of polynomial roots.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/rgrannell1/polynomial",
    packages = [
        "docopt"
    ],
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6'
)
