import graphene
import Train.schema


class Query(Train.schema.Query, graphene.ObjectType):
    pass


class Mutation(Train.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)