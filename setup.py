# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# try:
    # import pypandoc
    # long_description = pypandoc.convert('README.md', 'rst')
# except(IOError, ImportError):
#     long_description = open('README.md').read()

long_description = open('README.rst').read()

flask_requires = [
    'Flask>=1.0.2',
    'graphene>=2.1.2',
    'Flask-Graphql>=2.0.0',
]

django_requires = [
    'graphene-django>=2.0.0',
]
all_requires = flask_requires + django_requires

tests_require = [
    'coverage',
    'pytest',
    'pytest-cov',
    'pytest-django'
]

setup(
    name='graphene_file_upload',
    packages=find_packages(exclude=["tests"]),
    version='1.3.0',
    description='Lib for adding file upload functionality to GraphQL mutations in Graphene Django and Flask-Graphql',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Lucas McGartland',
    author_email='lucasmcgartland@gmail.com',
    url='https://github.com/lmcgartland/graphene-file-upload',  # use the URL to the github repo
    # download_url = 'https://github.com/lmcgartland/graphene-file-upload/archive/0.1.0.tar.gz',
    keywords=['graphql', 'graphene', 'apollo',  'upload'],  # arbitrary keywords
    install_requires=[
        'six>=1.11.0',
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
        "Framework :: Flask"
    ],
    extras_require={
        'flask': flask_requires,
        'django': django_requires,
        'all': all_requires,
        'tests': tests_require,
    },
)
