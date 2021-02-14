import json

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from graphene_file_upload.django import FileUploadGraphQLView
from tests.schema import schema

try:
    from django.urls import re_path as path
except ImportError:
    from django.conf.urls import url as path


def response_utf8_json(resp):
    return json.loads(resp.content.decode())


urlpatterns = [
    path('graphql', FileUploadGraphQLView.as_view(schema=schema), name='graphql'),
]

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

    t_file = SimpleUploadedFile(name='test.txt', content=file_text.encode('utf-8'))

    response = client.post(
        '/graphql',
        data={
            'operations': json.dumps({
                'query': query,
                'variables': {
                    'file': None,
                },
            }),
            't_file': t_file,
            'map': json.dumps({
                't_file': ['variables.file'],
            }),
        }
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


@pytest.mark.parametrize(
    'client,file_text,expected_first_line',
    (
            (None, u'Fake Data\nLine2\n', u'Fake Data'),
            # Try the fire emoji
            (None, u'\U0001F525\nLine2\nLine3\n', u'\U0001F525'),
    ),
    indirect=['client']
)
def test_file_graphql_query(client, file_text, expected_first_line):
    from graphene_file_upload.django.testing import file_graphql_query

    query = '''
        mutation testMutation($file: Upload!) {
            myUpload(fileIn: $file) {
                ok
                firstLine
            }
        }
    '''

    t_file = SimpleUploadedFile(name='test.txt', content=file_text.encode('utf-8'))

    response = file_graphql_query(
        query,
        op_name='testMutation',
        files={'file': t_file},
        client=client,
        graphql_url='/graphql',
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
