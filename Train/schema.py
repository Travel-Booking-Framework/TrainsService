import graphene
from Train.mutations.station_mutation import StationMutations
from Train.mutations.railway_mutation import RailwayCompanyMutations
from Train.mutations.trainhall_mutation import TrainHallMutations
from Train.mutations.train_mutation import TrainMutations
from Train.query import TrainQueries, RailwayCompanyQueries, TrainHallQueries, StationQueries


# Combine all mutations into a single class
class Mutation(StationMutations, RailwayCompanyMutations, TrainHallMutations, TrainMutations, graphene.ObjectType):
    pass


# Combine all queries into a single class
class Query(TrainQueries, RailwayCompanyQueries, TrainHallQueries, StationQueries, graphene.ObjectType):
    pass


# Define the schema
schema = graphene.Schema(mutation=Mutation, query=Query)