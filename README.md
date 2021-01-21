 [![Build Status](https://travis-ci.com/lmcgartland/graphene-file-upload.svg?branch=master)](https://travis-ci.com/lmcgartland/graphene-file-upload) [![PyPI version](https://badge.fury.io/py/graphene-file-upload.svg)](https://badge.fury.io/py/graphene-file-upload)

# graphene-file-upload

`graphene-file-upload` is a drop in replacement for the the GraphQL view in
Graphene for Django, and for Flask-Graphql. It supports multi-part file uploads
that adhere to the [Multipart Request Spec](https://github.com/jaydenseric/graphql-multipart-request-spec).

It currently supports Python 2.7 and 3.4+.

## Installation:

`pip install graphene-file-upload`

## Usage

To add an upload type to your mutation, import and use `Upload`.
Upload is a scalar type.

```python
from graphene_file_upload.scalars import Upload

class UploadMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        # do something with your file

        return UploadMutation(success=True)
```

### Django Integration:

To use, import the view, then add to your list of urls (replace previous
GraphQL view).

```python
from graphene_file_upload.django import FileUploadGraphQLView

urlpatterns = [
  url(r'^graphql', FileUploadGraphQLView.as_view(graphiql=True)),
]
```

### Flask Integration:

Note that `flask-graphql` version `<2.0` is not supported. At the time of
writing this README, you must install `flask-graphql` with
`pip install --pre flask-graphql`

Simply import the modified view and create a new url rule on your app:

```python
from graphene_file_upload.flask import FileUploadGraphQLView

app.add_url_rule(
    '/graphql',
    view_func=FileUploadGraphQLView.as_view(
      ...
    )
)
```

### Contributing:

If you'd like to contribute, please run the test suite prior to sending a PR.

In order to run the testing environment, create a virtual environment, install
tox, and run the tox commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-tox.txt
# You may have to deactivate and reactivate to have access to the tox command,
# depending on your system.

# Run the test suite with the versions of python you have installed
tox -e py27,py34 --develop
# Alternatively, if you're using something like pyenv and can easily install
# Multiple versions of python, then try running the following command
tox --develop

# If for some reason you need to recreate the tox environment (e.g. a new
# dependency has been added since you last ran it, you run `tox` without the
# `--develop` flag), add the -r flag to the tox command

tox -r {...additional flags...}
```

Check out [pyenv](https://github.com/pyenv/pyenv) if you'd like a simple way of
installing multiple python versions to test out.

### Packaging for PyPi:

Build the distribution.

`python3 setup.py sdist bdist_wheel`

Upload to PyPi test servers.

`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

Upload to PyPi production servers.

`twine upload dist/*`
