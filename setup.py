import setuptools
from setuptools import setup

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

description = """This application controls Hioki's LCR meter (IM3536) and Sigma Kouki's stage controller (controller: shot-702, stage: SGSP-26-200) at the same time."""

setup(
    name="DeviceController",
    version="0.1.0",
    author="Yakitori",
    author_email="4yutan4@gmail.com",
    description=description,
    longdescription=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/5yutan5/tensile-LCR-tester",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
