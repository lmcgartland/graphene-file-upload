import graphene
from graphene_file_upload.scalars import Upload

class Query(graphene.ObjectType):
    ok = graphene.Boolean(default_value=True)

class MyUpload(graphene.Mutation):
    class Arguments:
        file_in = Upload()

    ok = graphene.Boolean()

    def mutate(self, info, file_in):
        for line in file_in:
            print(line)
        return MyUpload(ok=True)

class Mutation(graphene.ObjectType):
    my_upload = MyUpload.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, types=[])
