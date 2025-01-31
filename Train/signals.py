from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Train, Station, RailwayCompany, TrainHall
from .documents import TrainDocument, StationDocument, RailwayCompanyDocument, TrainHallDocument


# Signal for Train model
class TrainSignalHandler:
    @staticmethod
    @receiver(post_save, sender=Train)
    def update_train_elasticsearch(sender, instance, created, **kwargs):
        """
        When a Train is created or updated, sync it with Elasticsearch.
        """
        if created:
            # If a new Train is created, index it in Elasticsearch
            TrainDocument().update(instance)
        else:
            # If a Train is updated, update the corresponding index in Elasticsearch
            TrainDocument().update(instance)

    @staticmethod
    @receiver(post_delete, sender=Train)
    def delete_train_elasticsearch(sender, instance, **kwargs):
        """
        When a Train is deleted, remove it from Elasticsearch.
        """
        TrainDocument().delete(instance)


# Signal for Station model
class StationSignalHandler:
    @staticmethod
    @receiver(post_save, sender=Station)
    def update_station_elasticsearch(sender, instance, created, **kwargs):
        """
        When a Station is created or updated, sync it with Elasticsearch.
        """
        if created:
            # If a new Station is created, index it in Elasticsearch
            StationDocument().update(instance)
        else:
            # If a Station is updated, update the corresponding index in Elasticsearch
            StationDocument().update(instance)

    @staticmethod
    @receiver(post_delete, sender=Station)
    def delete_station_elasticsearch(sender, instance, **kwargs):
        """
        When a Station is deleted, remove it from Elasticsearch.
        """
        StationDocument().delete(instance)


# Signal for RailwayCompany model
class RailwayCompanySignalHandler:
    @staticmethod
    @receiver(post_save, sender=RailwayCompany)
    def update_railway_company_elasticsearch(sender, instance, created, **kwargs):
        """
        When a RailwayCompany is created or updated, sync it with Elasticsearch.
        """
        if created:
            # If a new RailwayCompany is created, index it in Elasticsearch
            RailwayCompanyDocument().update(instance)
        else:
            # If a RailwayCompany is updated, update the corresponding index in Elasticsearch
            RailwayCompanyDocument().update(instance)

    @staticmethod
    @receiver(post_delete, sender=RailwayCompany)
    def delete_railway_company_elasticsearch(sender, instance, **kwargs):
        """
        When a RailwayCompany is deleted, remove it from Elasticsearch.
        """
        RailwayCompanyDocument().delete(instance)


# Signal for TrainHall model
class TrainHallSignalHandler:
    @staticmethod
    @receiver(post_save, sender=TrainHall)
    def update_train_hall_elasticsearch(sender, instance, created, **kwargs):
        """
        When a TrainHall is created or updated, sync it with Elasticsearch.
        """
        if created:
            # If a new TrainHall is created, index it in Elasticsearch
            TrainHallDocument().update(instance)
        else:
            # If a TrainHall is updated, update the corresponding index in Elasticsearch
            TrainHallDocument().update(instance)

    @staticmethod
    @receiver(post_delete, sender=TrainHall)
    def delete_train_hall_elasticsearch(sender, instance, **kwargs):
        """
        When a TrainHall is deleted, remove it from Elasticsearch.
        """
        TrainHallDocument().delete(instance)