# Always prefer setuptools over distutils
import io

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

BASE_DIR = path.dirname(__file__)
README_PATH = path.join(BASE_DIR, "README.md")
LONG_DESCRIPTION_TYPE = "text/markdown"

if path.isfile(README_PATH):
    with io.open(README_PATH, encoding="utf-8") as f:
        LONG_DESCRIPTION = f.read()
else:
    LONG_DESCRIPTION = ""

flask_requires = [
    "Flask>=1.0.2",
    "graphene>=2.1.2",
    "Flask-Graphql>=2.0.0",
    "flask_unittest>=0.1.2",
]

django_requires = [
    "django",
    "graphene-django>=2.0.0",
]
all_requires = flask_requires + django_requires

tests_require = [
    "coverage",
    "pytest",
    "pytest-cov",
    "pytest-django",
    "parameterized",
]

setup(
    name="graphene_file_upload",
    packages=find_packages(exclude=["tests"]),
    version="1.3.0",
    description="Lib for adding file upload functionality to GraphQL mutations in Graphene Django and Flask-Graphql",
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_TYPE,
    author="Lucas McGartland",
    author_email="lucasmcgartland@gmail.com",
    url="https://github.com/lmcgartland/graphene-file-upload",  # use the URL to the github repo
    # download_url = "https://github.com/lmcgartland/graphene-file-upload/archive/0.1.0.tar.gz",
    keywords=["graphql", "graphene", "apollo",  "upload"],  # arbitrary keywords
    install_requires=[
        "six>=1.11.0",
    ],
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Internet :: WWW/HTTP",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Flask"
    ],
    extras_require={
        "flask": flask_requires,
        "django": django_requires,
        "all": all_requires,
        "tests": tests_require,
    },
)
