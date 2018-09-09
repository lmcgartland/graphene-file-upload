import json
from tempfile import NamedTemporaryFile

import pytest

import graphene
from graphene_file_upload.scalars import Upload
from graphene_file_upload.flask import FileUploadGraphQLView

from .flask_app import create_app


class Query(graphene.ObjectType):
    ok = graphene.Boolean(default_value=True)


class MyUpload(graphene.Mutation):
    class Arguments:
        file_in = Upload()

    ok = graphene.Boolean()
    first_line = graphene.String()

    def mutate(self, info, file_in):
        first_line = file_in.readline().strip().decode('utf-8')
        file_in.seek(0)
        return MyUpload(ok=True, first_line=first_line)


class Mutation(graphene.ObjectType):
    my_upload = MyUpload.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


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
def test_single_file(client, file_text, expected_first_line):
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
