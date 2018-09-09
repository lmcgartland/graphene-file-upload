from flask import Flask
from graphene_file_upload.flask import FileUploadGraphQLView

from graphql import GraphQLCachedBackend


def create_app(schema, path='/graphql'):
    app = Flask(__name__)
    app.debug = True
    app.add_url_rule(
        path,
        view_func=FileUploadGraphQLView.as_view(
            'graphql',
            schema=schema,
        ),
    )
    return app
