# From: https://packaging.python.org/tutorials/packaging-projects/
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BioSimG10-pkg",
    version="1.0.0",
    author="Jørgen Navjord, Eirik Høyheim",
    author_email="navjordj@gmail.com, eirihoyh@nmbu",
    description="Package for running biology simulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/navjordj/BioSim_G10_Eirik_Jorgen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
