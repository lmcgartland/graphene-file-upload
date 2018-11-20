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

setup(
    name='graphene_file_upload',
    packages=find_packages(),
    version='1.2.2',
    description='Lib for adding file upload functionality to GraphQL mutations in Graphene Django and Flask-Graphql',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Lucas McGartland',
    author_email='lucasmcgartland@gmail.com',
    url='https://github.com/lmcgartland/graphene-file-upload', # use the URL to the github repo
    # download_url = 'https://github.com/lmcgartland/graphene-file-upload/archive/0.1.0.tar.gz',
    keywords=['graphql', 'graphene', 'apollo',  'upload'], # arbitrary keywords
    classifiers=[],
    install_requires=[
        'six>=1.11.0',
    ],
    extras_require={
        'flask': flask_requires,
        'django': django_requires,
        'all': all_requires,
    },
)
