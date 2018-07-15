# graphene-file-upload

`graphene-file-upload` is a drop in replacement for the the GraphQL view in
Graphene for Django, and for Flask-Graphql. It supports multi-part file uploads
that adhere to the [Multipart Request Spec](https://github.com/jaydenseric/graphql-multipart-request-spec).

## Installation:

`pip install graphene-file-upload`

## Usage

To add an upload type to your mutation, import and use `Upload`.
Upload is a scalar type.

```python
from graphene_file_upload.scalars import Upload

class UploadMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        # do something with your file

        return UploadMutation(success=True)
```

### Django Integration:

To use, import the view, then add to your list of urls (replace previous
GraphQL view).

```python
from graphene_file_upload.django import ModifiedGraphQLView

urlpatterns = [
  url(r'^graphql', ModifiedGraphQLView.as_view(graphiql=True)),
]
```

### Flask Integration:

Note that `flask-graphql` version `<2.0` is not supported. At the time of
writing this README, you must install `flask-graphql` with
`pip install --pre flask-graphql`

Simply import the modified view and create a new url rule on your app:

```python
from graphene_file_upload.flask import ModifiedGraphQLView

app.add_url_rule(
    '/graphql',
    view_func=ModifiedGraphQLView.as_view(
      ...
    )
)
```

## Other Notes

#### Testing:

TO-DO, still need to write tests for Django and Flask views.

#### Packaging for PyPi:

Build the distribution.

`python3 setup.py sdist bdist_wheel`

Upload to PyPi test servers.

`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

Upload to PyPi production servers.

`twine upload dist/*`

