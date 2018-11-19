"""Apply multipart request spec to flask"""
from flask import request
from flask_graphql import GraphQLView
from graphql_server import load_json_body

from ..utils import place_files_in_operations


class FileUploadGraphQLView(GraphQLView):
    """Handles multipart/form-data content type in flask views"""

    def parse_body(self):
        """Handle multipart request spec for multipart/form-data"""
        content_type = request.mimetype
        if content_type == 'multipart/form-data':
            operations = load_json_body(request.form.get('operations', '{}'))
            files_map = load_json_body(request.form.get('map', '{}'))
            return place_files_in_operations(
                operations,
                files_map,
                request.files
            )
        return super(FileUploadGraphQLView, self).parse_body()
