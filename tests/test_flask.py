import json
from tempfile import NamedTemporaryFile

import pytest
from flask.testing import FlaskClient
from parameterized import parameterized

from graphene_file_upload.flask.testing import GraphQLFileUploadTestCase
from graphene_file_upload.testing import file_graphql_query
from .flask_app import create_app
from .schema import schema


def response_utf8_json(resp):
    return json.loads(resp.data.decode())


@pytest.fixture
def client():
    app = create_app(schema=schema)
    client = app.test_client()
    yield client


@pytest.mark.parametrize(
    'client,file_text,expected_first_line',
    (
        (None, u'Fake Data\nLine2\n', u'Fake Data'),
        # Try the fire emoji
        (None, u'\U0001F525\nLine2\nLine3\n', u'\U0001F525'),
    ),
    indirect=['client']
)
def test_upload(client, file_text, expected_first_line):
    query = '''
        mutation testMutation($file: Upload!) {
            myUpload(fileIn: $file) {
                ok
                firstLine
            }
        }
    '''
    with NamedTemporaryFile() as t_file:
        t_file.write(file_text.encode('utf-8'))
        t_file.seek(0)

        response = file_graphql_query(
            query,
            op_name='testMutation',
            files={'file': t_file},
            client=client,
        )

    assert response.status_code == 200
    assert response_utf8_json(response) == {
        'data': {
            'myUpload': {
                'ok': True,
                'firstLine': expected_first_line,
            },
        }
    }


class MyUploadTestCase(GraphQLFileUploadTestCase):
    app = create_app(schema=schema)

    @parameterized.expand([
        (u'Fake Data\nLine2\n', u'Fake Data'),
        # Try the fire emoji
        (u'\U0001F525\nLine2\nLine3\n', u'\U0001F525'),
    ])
    def test_upload(self, client, file_text, expected_first_line):
        query = '''
           mutation testMutation($file: Upload!) {
               myUpload(fileIn: $file) {
                   ok
                   firstLine
               }
           }
       '''

        with NamedTemporaryFile() as t_file:
            t_file.write(file_text.encode('utf-8'))
            t_file.seek(0)

            response = self.file_query(
                query,
                op_name='testMutation',
                files={'file': t_file},
            )

            assert response.status_code == 200
            assert response_utf8_json(response) == {
                'data': {
                    'myUpload': {
                        'ok': True,
                        'firstLine': expected_first_line,
                    },
                }
            }
