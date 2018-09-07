from collections import namedtuple

import pytest

from graphene_file_upload.utils import place_files_in_operations


class FFake(object):
    '''Fake File object that is placed in operations'''
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'FFake(value={value})'.format(value=self.value)

    def __eq__(self, other):
        return isinstance(other, FFake) and self.value == other.value


Parameter = namedtuple('TestParameter', (
    'operations',
    'files_map',
    'file_name_map',
    'expected',
))

CASE_PARAMS = (
    # Handle simple operations
    Parameter(
        operations={
            'query': 'q',
            'variables': {'f': None},
        },
        files_map={
            'thiz_file': ['variables.f']
        },
        file_name_map={
            'thiz_file': FFake('thiz')
        },
        expected={
            'query': 'q',
            'variables': {'f': FFake('thiz')},
        }
    ),
    # Handle batch operations
    Parameter(
        operations=[
            {'query': 'q1', 'variables': {'file': None}},
            {'query': 'q2', 'variables': {'files': [None, None]}},
        ],
        files_map={
            'tf1': ['0.variables.file', '1.variables.files.0'],
            'tf2': ['1.variables.files.1'],
        },
        file_name_map={
            'tf1': FFake('f1'),
            'tf2': FFake('f2'),
        },
        expected=[
            {'query': 'q1', 'variables': {'file': FFake('f1')}},
            {'query': 'q2', 'variables': {'files': [FFake('f1'), FFake('f2')]}},
        ],
    ),
)


@pytest.mark.parametrize(
    'operations,files_map,file_name_map,expected',
    CASE_PARAMS
)
def test_place_files_in_operations(
    operations,
    files_map,
    file_name_map,
    expected,
):
    actual = place_files_in_operations(operations, files_map, file_name_map)
    assert actual == expected
