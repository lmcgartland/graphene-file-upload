import json
from graphene_django.views import GraphQLView

from .utils import place_files_in_operations


class FileUploadGraphQLView(GraphQLView):

    def parse_body(self, request):
        content_type = self.get_content_type(request)
        if content_type == 'multipart/form-data':
            operations = json.loads(request.POST.get('operations', '{}'))
            files_map = json.loads(request.POST.get('map', '{}'))
            return place_files_in_operations(
                operations,
                files_map,
                request.FILES
            )
        return super(FileUploadGraphQLView, self).parse_body(request)
