# coding: utf-8

"""
    Watch and Chill

    This is a sample application for demonstrating CI/CD using GitOps and Kubernetes.  Some useful links:  * [The Pet Watch and Chill repository](https://github.com/lago-morph/chiller) * [Design document corresponding to this version of the API](https://github.com/lago-morph/chiller/wiki/Let's-Watch-design)  # noqa: E501

    OpenAPI spec version: 1.0.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from setuptools import setup, find_packages  # noqa: H301

NAME = "chiller-api-client"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Watch and Chill",
    author_email="",
    url="",
    keywords=["Swagger", "Watch and Chill"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    This is a sample application for demonstrating CI/CD using GitOps and Kubernetes.  Some useful links:  * [The Pet Watch and Chill repository](https://github.com/lago-morph/chiller) * [Design document corresponding to this version of the API](https://github.com/lago-morph/chiller/wiki/Let&#x27;s-Watch-design)  # noqa: E501
    """
)
