"""Apply multipart request spec to django"""
import json
from django.forms import FileField
from graphene_django.views import GraphQLView
from graphene_django.forms.converter import convert_form_field

from ..utils import place_files_in_operations
from ..scalars import Upload


@convert_form_field.register(FileField)
def convert_form_field_to_upload(field):
    return Upload(description=field.help_text, required=field.required)


class FileUploadGraphQLView(GraphQLView):
    """Handles multipart/form-data content type in django views"""

    def parse_body(self, request):
        """Handle multipart request spec for multipart/form-data"""
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
