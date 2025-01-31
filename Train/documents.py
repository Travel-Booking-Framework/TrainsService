from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Train, TrainHall, RailwayCompany, Station


@registry.register_document
class StationDocument(Document):
    """
    Elasticsearch Document for Station Model
    """
    class Index:
        name = 'stations'  # Index name in Elasticsearch

    class Django:
        model = Station  # Model being mapped to this Document

        # Fields to be indexed in Elasticsearch
        fields = [
            'station_name',
            'station_city',
            'station_province',
        ]

        ignore_signals = False  # Enable signals to sync changes
        auto_refresh = True  # Automatically refresh the index


@registry.register_document
class RailwayCompanyDocument(Document):
    """
    Elasticsearch Document for RailwayCompany Model
    """
    class Index:
        name = 'railway_companies'  # Index name in Elasticsearch

    class Django:
        model = RailwayCompany  # Model being mapped to this Document

        # Fields to be indexed in Elasticsearch
        fields = [
            'railway_name',
            'railway_description',
            'refund_policy',
        ]

        ignore_signals = False  # Enable signals to sync changes
        auto_refresh = True  # Automatically refresh the index


@registry.register_document
class TrainHallDocument(Document):
    """
    Elasticsearch Document for TrainHall Model
    """
    class Index:
        name = 'train_halls'  # Index name in Elasticsearch

    class Django:
        model = TrainHall  # Model being mapped to this Document

        # Fields to be indexed in Elasticsearch
        fields = [
            'hall_name',
            'hall_description',
        ]

        ignore_signals = False  # Enable signals to sync changes
        auto_refresh = True  # Automatically refresh the index


@registry.register_document
class TrainDocument(Document):
    """
    Elasticsearch Document for Train Model
    """
    # Related fields using ObjectField for foreign key relationships
    departure_station = fields.ObjectField(properties={
        'station_name': fields.TextField(),
        'station_code': fields.KeywordField(),
        'station_city': fields.TextField(),
    })

    arrival_station = fields.ObjectField(properties={
        'station_name': fields.TextField(),
        'station_code': fields.KeywordField(),
        'station_city': fields.TextField(),
    })

    railway_company = fields.ObjectField(properties={
        'railway_name': fields.TextField(),
        'railway_code': fields.KeywordField(),
    })

    hall = fields.ObjectField(properties={
        'hall_name': fields.TextField(),
        'hall_description': fields.TextField(),
    })

    class Index:
        name = 'trains'  # Index name in Elasticsearch

    class Django:
        model = Train  # Model being mapped to this Document

        # Fields to be indexed in Elasticsearch (including final_price)
        fields = [
            'train_number',
            'train_type',
            'capacity',
            'stars',
            'base_price',
            'tax',
            'discount',
            'final_price',
            'departure_datetime',
            'arrival_datetime',
        ]

        # Related models that we want to include in the index
        related_models = ['Station', 'RailwayCompany', 'TrainHall']

        ignore_signals = False  # Enable signals to sync changes to Elasticsearch
        auto_refresh = True  # Automatically refresh the index after changes