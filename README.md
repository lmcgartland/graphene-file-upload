# graphene-file-upload
`graphene-file-upload` is a drop in replacement for the the GraphQL view in Graphene for Django. It supports multi-part file uploads that adhere to the Multipart Request Spec (https://github.com/jaydenseric/graphql-multipart-request-spec).

## Installation:
`pip install graphene-file-upload`

## Usage:
To use, import the view, then add to your list of urls (replace previous GraphQL view).

```python
from graphene_file_upload import ModifiedGraphQLView

urlpatterns = [
  url(r'^graphql', ModifiedGraphQLView.as_view(graphiql=True)),
]
```

To add an upload type to your mutation, import and use `Upload`. Upload is a scalar type.

```python
from graphene_file_upload import Upload

class UploadMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        # file parameter is key to uploaded file in FILES from context
        uploaded_file = info.context.FILES.get(file)
        # do something with your file

        return UploadMutation(success=True)
```
