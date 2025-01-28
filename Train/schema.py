import graphene
from Train.mutations.station_mutation import StationMutations
from Train.mutations.railway_mutation import RailwayCompanyMutations
from Train.mutations.trainhall_mutation import TrainHallMutations
from Train.mutations.train_mutation import TrainMutations


# Combine all mutations into a single class
class Mutation(StationMutations, RailwayCompanyMutations, TrainHallMutations, TrainMutations, graphene.ObjectType):
    pass


# Define the schema
schema = graphene.Schema(mutation=Mutation)