import graphene
from graphene_django.types import DjangoObjectType
from .models import Train, RailwayCompany, TrainHall, Station


# GraphQL Types for Models
class TrainType(DjangoObjectType):
    class Meta:
        model = Train


class RailwayCompanyType(DjangoObjectType):
    class Meta:
        model = RailwayCompany


class TrainHallType(DjangoObjectType):
    class Meta:
        model = TrainHall


class StationType(DjangoObjectType):
    class Meta:
        model = Station


# Query Classes
class TrainQueries(graphene.ObjectType):
    all_trains = graphene.List(TrainType)
    train_by_number = graphene.Field(TrainType, train_number=graphene.String(required=True))

    def resolve_all_trains(self, info, **kwargs):
        return Train.objects.all()

    def resolve_train_by_number(self, info, train_number):
        try:
            return Train.objects.get(train_number=train_number)
        except Train.DoesNotExist:
            return None


class RailwayCompanyQueries(graphene.ObjectType):
    all_railway_companies = graphene.List(RailwayCompanyType)
    railway_company_by_name = graphene.Field(RailwayCompanyType, railway_name=graphene.String(required=True))

    def resolve_all_railway_companies(self, info, **kwargs):
        return RailwayCompany.objects.all()

    def resolve_railway_company_by_name(self, info, railway_name):
        try:
            return RailwayCompany.objects.get(railway_name=railway_name)
        except RailwayCompany.DoesNotExist:
            return None


class TrainHallQueries(graphene.ObjectType):
    all_train_halls = graphene.List(TrainHallType)
    train_hall_by_name = graphene.Field(TrainHallType, hall_name=graphene.String(required=True))

    def resolve_all_train_halls(self, info, **kwargs):
        return TrainHall.objects.all()

    def resolve_train_hall_by_name(self, info, hall_name):
        try:
            return TrainHall.objects.get(hall_name=hall_name)
        except TrainHall.DoesNotExist:
            return None


class StationQueries(graphene.ObjectType):
    all_stations = graphene.List(StationType)
    station_by_name = graphene.Field(StationType, station_name=graphene.String(required=True))

    def resolve_all_stations(self, info, **kwargs):
        return Station.objects.all()

    def resolve_station_by_name(self, info, station_name):
        try:
            return Station.objects.get(station_name=station_name)
        except Station.DoesNotExist:
            return None