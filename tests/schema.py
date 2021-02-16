import graphene

from graphene_file_upload.scalars import Upload


class Query(graphene.ObjectType):
    ok = graphene.Boolean(default_value=True)


class MyUpload(graphene.Mutation):
    class Arguments:
        file_in = Upload()

    ok = graphene.Boolean()
    first_line = graphene.String()

    def mutate(self, info, file_in):
        first_line = file_in.readline().strip().decode('utf-8')
        file_in.seek(0)
        return MyUpload(ok=True, first_line=first_line)


class Mutation(graphene.ObjectType):
    my_upload = MyUpload.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
