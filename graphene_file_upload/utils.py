"""Utils

This module defines the framework-agnostic logic for handling the multipart
request spec
"""
from six import iteritems


def place_files_in_operations(operations, files_map, files):
    """Replaces None placeholders in operations with file objects in the files
    dictionary, by following the files_map logic as specified within the 'map'
    request parameter in the multipart request spec"""
    path_to_key_iter = (
        (value.split('.'), key)
        for (key, values) in iteritems(files_map)
        for value in values
    )
    # Since add_files_to_operations returns a new dict/list, first define
    # output to be operations itself
    output = operations
    for path, key in path_to_key_iter:
        file_obj = files[key]
        output = add_file_to_operations(output, file_obj, path)
    return output


def add_file_to_operations(operations, file_obj, path):
    """Handles the recursive algorithm for adding a file to the operations
    object"""
    if not path:
        if operations is not None:
            raise ValueError('Path in map does not lead to a null value')
        return file_obj
    if isinstance(operations, dict):
        key = path[0]
        sub_dict = add_file_to_operations(operations[key], file_obj, path[1:])
        return new_merged_dict(operations, {key: sub_dict})
    if isinstance(operations, list):
        index = int(path[0])
        sub_item = add_file_to_operations(
            operations[index],
            file_obj,
            path[1:],
        )
        return new_list_with_replaced_item(operations, index, sub_item)
    raise TypeError('Operations must be a dict or a list of dicts')


def new_merged_dict(*dicts):
    """Merges dictionaries into a new dictionary. Necessary for python2 and
    python34 since neither have PEP448 implemented."""
    # Necessary for python2 support
    output = {}
    for d in dicts:
        output.update(d)
    return output


def new_list_with_replaced_item(input_list, index, new_value):
    """Creates new list with replaced item at specified index"""
    output = input_list
    output[index] = new_value
    return output
