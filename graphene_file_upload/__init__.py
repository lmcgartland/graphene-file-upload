from graphene_django.views import GraphQLView
import json
import graphene

# Implement this spec:
# https://github.com/jaydenseric/graphql-multipart-request-spec

# "Multipart GraphQL server requests are handled by apollo-upload-server middleware.
# The files upload to a temp directory, the operations field is JSON decoded and object-path
# is used to insert metadata about each of the uploads (including the temp path) in place of
# the original files in the resolver arguments."

# Basically we need to do all of the above.

class ModifiedGraphQLView(GraphQLView):
    # graphiql_template = 'graphiql.html'

    @staticmethod
    def get_graphql_params(request, data):
        request_type = request.META.get("CONTENT_TYPE")

        if "multipart/form-data" in request_type:
            query, variables, operation_name, id = super(ModifiedGraphQLView, ModifiedGraphQLView).get_graphql_params(request, data)
            operations = data.get('operations')
            files_map = data.get('map')



            try:
                operations = json.loads(operations)
                files_map = json.loads(files_map)

                variables = operations.get('variables')
                for file_key in files_map:
                    # file key is which file it is in the form-data
                    file_instances = files_map[file_key]
                    # pp.pprint(file_instances)
                    for file_instance in file_instances:
                        # print('file_instance')
                        # pp.pprint(file_instance)
                        test = obj_set(operations, file_instance, file_key, False)

                query = operations.get('query')
                variables = operations.get('variables')

            except Exception as e:
                raise e
                # raise HttpError(HttpResponseBadRequest('Operations are invalid JSON.'))

        else:
            query, variables, operation_name, id = super(ModifiedGraphQLView, ModifiedGraphQLView).get_graphql_params(request, data)

        # Example Request Body
        # {'map': '{"0":["variables.file"]}',
        #  'operations': '{"query":"mutation ($file: Upload!) {\\n  '
        #                'uploadImageTest(file: $file) {\\n    success\\n    '
        #                '__typename\\n  }\\n}\\n","variables":{}}'}
        #
        # Need to maybe map the map into the variables for files so that way the
        # resolver knows which file on the multipart form to access

        return query, variables, operation_name, id

# class ObjectPath:
def getKey(key):
    try:
        intKey = int(key)
        return intKey
    except:
        return key

def getShallowProperty(obj, prop):
    if type(prop) is int:
        return obj[prop]

    try:
        return obj.get(prop)
    except:
        return None

def obj_set(obj, path, value, doNotReplace):
    if type(path) is int:
        path = [path]
    if path is None or len(path) == 0:
        return obj
    if isinstance(path, str):
        newPath = list(map(getKey, path.split('.')))
        return obj_set(obj, newPath, value, doNotReplace )

    currentPath = path[0]
    currentValue = getShallowProperty(obj, currentPath)

    if len(path) == 1:
        if currentValue is None or not doNotReplace:
            obj[currentPath] = value

    if currentValue is None:
        try:
            if type(path[1]) == int:
                obj[currentPath] = []
            else:
                obj[currentPath] = {}
        except Exception as e:
            pass
            # This line may need to be put back in but it will break it because it assumes an array.
            # obj[currentPath] = {}

    return obj_set(obj[currentPath], path[1:], value, doNotReplace)


class Upload(graphene.types.Scalar):
    @staticmethod
    def serialize(value):
        return value

    @staticmethod
    def parse_literal(node):
        return node

    @staticmethod
    def parse_value(value):
        return value
