"""Use flask's Test client to run file based graphql test."""
from .. import testingbase

DEFAULT_GRAPHQL_URL = "/graphql/"


def create_client_post(client):
    """
    Create client_post function for testingbase.file_graphql_query from django.test.Client
    """
    def client_post(graphql_url, data, files, headers=None):
        data.update(files)
        if headers:
            response = client.post(graphql_url, data=data, headers=headers)
        else:
            response = client.post(graphql_url, data=data)
        return response
    return client_post


def file_graphql_query(
        query, op_name=None, input_data=None, variables=None,
        headers=None, files=None, client=None, graphql_url=None,
):
    """
    Perform file based mutation, using django.test.Client

    :param str query: GraphQL query to run
    :param str op_name: If the query is a mutation or named query, you must
        supply the op_name. For annon queries ("{ ... }"), should be None (default).
    :param dict input_data: If provided, the $input variable in GraphQL will be set
        to this value. If both ``input_data`` and ``variables``,
        are provided, the ``input`` field in the ``variables``
        dict will be overwritten with this value. Defaults to None.
    :param dict variables: If provided, the "variables" field in GraphQL will be
        set to this value. Defaults to None.
    :param dict headers: If provided, the headers in POST request to GRAPHQL_URL
        will be set to this value. Defaults to None
    :param dict files: Files to be sent via request.FILES. Defaults to None.
    :param  flask.testing.FlaskClient: Test client. Defaults to None.
    :param str graphql_url: URL to graphql endpoint. Defaults to "/graphql"
    :return: Response object from client
    """
    client_post = create_client_post(client)
    return testingbase.file_graphql_query(
        query, op_name, input_data, variables, headers, files, client_post, graphql_url)
