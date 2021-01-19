"""Apply multipart request spec to django"""
import json
from graphene_django.views import GraphQLView

from ..utils import place_files_in_operations


class FileUploadGraphQLView(GraphQLView):
    """Handles multipart/form-data content type in django views"""

    def parse_body(self, request):
        """Handle multipart request spec for multipart/form-data"""
        content_type = self.get_content_type(request)
        if content_type == 'multipart/form-data' and 'operations' in request.POST:
            operations = json.loads(request.POST.get('operations', '{}'))
            files_map = json.loads(request.POST.get('map', '{}'))
            return place_files_in_operations(
                operations,
                files_map,
                request.FILES
            )
        return super(FileUploadGraphQLView, self).parse_body(request)
