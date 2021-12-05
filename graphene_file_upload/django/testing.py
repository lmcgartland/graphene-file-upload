"""
Django testing module
"""

from django.test import TestCase, SimpleTestCase
from graphene_file_upload.testing import GraphQLFileUploadTestMixin


class GraphQLFileUploadTestCase(GraphQLFileUploadTestMixin, TestCase):
    pass


class GraphQLFileUploadSimpleTestCase(GraphQLFileUploadTestMixin, SimpleTestCase):
    pass
