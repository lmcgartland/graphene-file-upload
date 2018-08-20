# Always prefer setuptools over distutils
from setuptools import setup
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


setup(
  name = 'graphene_file_upload',
  packages = ['graphene_file_upload'], # this must be the same as the name above
  version = '1.0.0',
  description = 'Lib for adding file upload functionality to GraphQL mutations in Graphene Django and Flask-Graphql',
  long_description=long_description,
  long_description_content_type='text/x-rst',
  author = 'Lucas McGartland',
  author_email = 'lucasmcgartland@gmail.com',
  url = 'https://github.com/lmcgartland/graphene-file-upload', # use the URL to the github repo
  # download_url = 'https://github.com/lmcgartland/graphene-file-upload/archive/0.1.0.tar.gz',
  keywords = ['graphql', 'graphene', 'apollo',  'upload'], # arbitrary keywords
  classifiers = [],
  # install_requires=[]
)
