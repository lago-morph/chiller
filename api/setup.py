# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "chiller_api"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion",
    "swagger-ui-bundle>=0.0.2"
]

setup(
    name=NAME,
    version=VERSION,
    description="Watch and Chill",
    author_email="",
    url="",
    keywords=["Swagger", "Watch and Chill"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['chiller_api=chiller_api.__main__:main']},
    long_description="""\
    This is a sample application for demonstrating CI/CD using GitOps and Kubernetes.  Some useful links:  * [The Pet Watch and Chill repository](https://github.com/lago-morph/chiller) * [Design document corresponding to this version of the API](https://github.com/lago-morph/chiller/wiki/Let&#x27;s-Watch-design)
    """
)
