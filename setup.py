#!/usr/bin/env python
import sys

from setuptools import setup

PY2 = sys.version_info.major == 2

project = "rdflib-elasticstore"
version = "0.1.0"


setup(
    name=project,
    version=version,
    description="rdflib extension for using Elasticsearch back-end store",
    author="James McCusker, Peter Wood, Ethan Rambacher",
    author_email="mccusker@gmail.com, woodp@rpi.edu, rambae@rpi.edu",
    url="http://github.com/tetherless-world/rdflib-elasticstore",
    packages=["rdflib_elasticstore"],
    download_url="https://github.com/tetherless-world/rdflib-elasticstore/zipball/master",
    license="Apache 2.0 License",
    platforms=["any"],
    long_description="""
    Elasticsearch store implementation.
    """,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: Apache 2.0 License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    install_requires=[
        "alembic>=0.8.8",
        "rdflib>=4.0",
        "six>=1.10.0",
        "elasticsearch>=1.1.4",
    ],
    setup_requires=[
        "nose>=1.3.6",
    ],
    tests_require=[
        "coveralls"
    ] + (['mock'] if PY2 else []),
    test_suite="nose.collector",
    entry_points={
        'rdf.plugins.store': [
            'Elasticsearch = rdflib_elsticstore:Elasticsearch'
        ]
    }
)
