#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-streamduo",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_streamduo"],
    install_requires=[
        # NB: Pin these to a more specific version for tap reliability
        "singer-python",
        "requests",
        "streamduo"
    ],
    entry_points="""
    [console_scripts]
    tap-streamduo=tap_streamduo:main
    """,
    packages=["tap_streamduo"],
    package_data = {
        "schemas": ["tap_streamduo/schemas/*.json"]
    },
    include_package_data=True,
)
