import json
from graphene_django.views import GraphQLView

from .utils import place_files_in_operations


class ModifiedGraphQLView(GraphQLView):

    def parse_body(self, request):
        content_type = self.get_content_type(request)
        if content_type == 'multipart/form-data':
            operations = json.loads(data.get('operations', '{}'))
            files_map = json.loads(data.get('map', '{}'))
            return place_files_in_operations(
                operations,
                files_map,
                request.FILES
            )
        return super(ModifiedGraphQLView, self).parse_body(request)
