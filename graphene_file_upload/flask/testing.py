"""
Flask testing module
"""
from flask.testing import FlaskClient
from flask_unittest import ClientTestCase

from graphene_file_upload.testing import GraphQLFileUploadTestMixin


class GraphQLFileUploadTestCase(GraphQLFileUploadTestMixin, ClientTestCase):
    def setUp(self, client: FlaskClient) -> None:
        self.client = client
