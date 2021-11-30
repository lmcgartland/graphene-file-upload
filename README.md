[![Build Status](https://travis-ci.com/lmcgartland/graphene-file-upload.svg?branch=master)](https://travis-ci.com/lmcgartland/graphene-file-upload) [![PyPI version](https://badge.fury.io/py/graphene-file-upload.svg)](https://badge.fury.io/py/graphene-file-upload) [![Downloads](https://pepy.tech/badge/graphene-file-upload)](https://pepy.tech/project/graphene-file-upload)
 
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/graphene-file-upload) ![PyPI - Django Version](https://img.shields.io/pypi/djversions/graphene-file-upload) ![Flask](https://img.shields.io/badge/flask%20-%23000.svg?&style=flat&logo=flask&logoColor=white)

# graphene-file-upload

`graphene-file-upload` is a drop in replacement for the the GraphQL view in Graphene for Django, and for Flask-Graphql. 

It supports multi-part file uploads that adhere to the [Multipart Request Spec](https://github.com/jaydenseric/graphql-multipart-request-spec).

It currently supports Python 2.7 and 3.4+.

## Installation:

```shell script

pip install graphene-file-upload

```

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

## Testing

### Flask

https://flask.palletsprojects.com/en/1.1.x/testing/#the-testing-skeleton

```py 
# Create a fixture using the file_graphql_query helper and `client` fixture.
import os
import json
import tempfile

from flaskr import flaskr
import pytest
from graphene_file_upload.flask.testing import file_graphql_query


@pytest.fixture
def client():
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            flaskr.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return file_graphql_query(*args, **kwargs, client=client)

    return func

# Test your query using the client_query fixture
def test_some_query(client_query):
    test_file = SimpleUploadedFile(name='test.txt', content=file_text.encode('utf-8'))
    
    response = client_query(
        '''
        mutation testMutation($file: Upload!) {
            myUpload(fileIn: $file) {
                ok
            }
        }
        ''',
        op_name='testMutation'
        files={'file': test_file},
    )

    content = json.loads(response.content)
    assert 'errors' not in content
```

### Django

Writing test using [django's test client](https://docs.djangoproject.com/en/3.1/topics/testing/tools/#default-test-client)

#### Using pytest

To use pytest define a simple fixture using the query helper below

```py
# Create a fixture using the file_graphql_query helper and `client` fixture from `pytest-django`.

import json
import pytest
from graphene_file_upload.django.testing import file_graphql_query

@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return file_graphql_query(*args, **kwargs, client=client)

    return func

# Test your query using the client_query fixture
def test_some_query(client_query):
    test_file = SimpleUploadedFile(name='test.txt', content=file_text.encode('utf-8'))
    
    response = client_query(
        '''
        mutation testMutation($file: Upload!) {
            myUpload(fileIn: $file) {
                ok
            }
        }
        ''',
        op_name='testMutation'
        files={'file': test_file},
    )

    content = json.loads(response.content)
    assert 'errors' not in content
```

#### Using unittest

Your endpoint is set through the `GRAPHQL_URL` attribute on `GraphQLFileUploadTestCase`. The default endpoint is `GRAPHQL_URL = “/graphql/”`.

```py
import json

from graphene_file_upload.django.testing import GraphQLFileUploadTestCase

class MutationTestCase(GraphQLFileUploadTestCase):
   def test_some_mutation(self):
        test_file = SimpleUploadedFile(name='test.txt', content=file_text.encode('utf-8'))

        response = self.file_query(
            '''
            mutation testMutation($file: Upload!) {
                myUpload(fileIn: $file) {
                    ok
                }
            }
            ''',
            op_name='testMutation',
            files={'file': test_file},
        )

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
```

### Contributing:

If you'd like to contribute, please run the test suite prior to sending a PR.

In order to run the testing environment, create a virtual environment, install
tox, and run the tox commands:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ make install
# You may have to deactivate and reactivate to have access to the tox command,
# depending on your system.

# Run the test suite with the versions of python you have installed
$ tox
# Alternatively, if you're using something like pyenv and can easily install
# Multiple versions of python, then try running the following command
$ tox

# If for some reason you need to recreate the tox environment (e.g. a new
# dependency has been added since you last ran it, add the -r flag to the
# tox command)
$ tox -r {...additional flags...}
```

Check out [pyenv](https://github.com/pyenv/pyenv) if you'd like a simple way of
installing multiple python versions to test out.

### Packaging for PyPi:

Run
```bash
$ make deploy
```
