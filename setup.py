from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

from api import __api_version__


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="asteroid-api",
    version=__api_version__,
    description="API for use with Asteroid Jukebox.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="asteroid-music",
    url="https://github.com/asteroid-music/asteroid-api",
    packages=find_packages(exclude="tests"),
    install_requires=[
        "fastapi>=0.61.2",
        "uvicorn>=0.12.2",
        "dnspython>=2.0.0",
        "motor>=2.3.0",
        "youtube-dl>=2020.11.12",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires=">=3.7",
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-asyncio'],
    zip_safe=False,
)