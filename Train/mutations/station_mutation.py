from abc import ABC, abstractmethod
from Train.models import Station
import graphene
from graphene_django.types import DjangoObjectType


class StationCommand(ABC):
    """Base Command class for Station operations."""
    @abstractmethod
    def execute(self, **kwargs):
        pass

    @abstractmethod
    def undo(self, **kwargs):
        pass


class CreateStationCommand(StationCommand):
    def __init__(self):
        self.station = None  # To store the created Station for undo

    def execute(self, station_name, station_city, station_province):
        # Validate if the station already exists
        if Station.objects.filter(station_name=station_name, station_city=station_city, station_province=station_province).exists():
            raise Exception("Station with this station_name, station_city, and station_province already exists.")
        # Create the Station and store it for undo
        self.station = Station.objects.create(
            station_name=station_name,
            station_city=station_city,
            station_province=station_province
        )
        return self.station

    def undo(self):
        # Delete the created Station
        if self.station:
            self.station.delete()


class UpdateStationCommand(StationCommand):
    def __init__(self):
        self.previous_data = None  # To store the previous state for undo
        self.station = None

    def execute(self, station_id, **kwargs):
        try:
            # Fetch the Station and store its previous state
            self.station = Station.objects.get(id=station_id)
            self.previous_data = {field: getattr(self.station, field) for field in kwargs}

            # Update the Station
            for field, value in kwargs.items():
                setattr(self.station, field, value)
            self.station.save()
            return self.station
        except Station.DoesNotExist:
            raise Exception("Station with this ID does not exist.")

    def undo(self):
        # Revert the Station to its previous state
        if self.station and self.previous_data:
            for field, value in self.previous_data.items():
                setattr(self.station, field, value)
            self.station.save()


class DeleteStationCommand(StationCommand):
    def __init__(self):
        self.deleted_data = None  # To store the deleted Station's data for undo

    def execute(self, station_id):
        try:
            # Fetch the Station and delete it
            station = Station.objects.get(id=station_id)
            self.deleted_data = {
                "station_name": station.station_name,
                "station_city": station.station_city,
                "station_province": station.station_province
            }
            station.delete()
            return f"Station {station.station_name} deleted successfully."
        except Station.DoesNotExist:
            raise Exception("Station with this ID does not exist.")

    def undo(self):
        # Recreate the deleted Station
        if self.deleted_data:
            Station.objects.create(**self.deleted_data)


class StationCommandHandler:
    def __init__(self):
        self.undo_stack = []  # Stack to store executed Commands
        self.redo_stack = []  # Stack to store undone Commands

    def execute(self, command, **kwargs):
        # Execute the Command and store it in the undo stack
        result = command.execute(**kwargs)
        self.undo_stack.append(command)
        self.redo_stack.clear()  # Clear redo stack since a new operation is performed
        return result

    def undo(self):
        # Undo the last operation
        if not self.undo_stack:
            raise Exception("Nothing to undo.")
        command = self.undo_stack.pop()
        command.undo()
        self.redo_stack.append(command)

    def redo(self):
        # Redo the last undone operation
        if not self.redo_stack:
            raise Exception("Nothing to redo.")
        command = self.redo_stack.pop()
        command.execute()
        self.undo_stack.append(command)
        
        
# Define GraphQL Type for Station
class StationType(DjangoObjectType):
    class Meta:
        model = Station


# Shared handler instance
handler = StationCommandHandler()


# Define Mutation for Station
class StationMutations(graphene.ObjectType):
    create_station = graphene.Field(
        StationType,
        station_name=graphene.String(required=True),
        station_city=graphene.String(required=True),
        station_province=graphene.String(required=True)
    )

    update_station = graphene.Field(
        StationType,
        station_id=graphene.Int(required=True),
        station_name=graphene.String(),
        station_city=graphene.String(),
        station_province=graphene.String()
    )

    delete_station = graphene.String(
        station_id=graphene.Int(required=True)
    )

    undo_operation = graphene.String()
    redo_operation = graphene.String()

    def resolve_create_station(self, info, station_name, station_city, station_province):
        # Use Command Handler to create a Station
        command = CreateStationCommand()
        return handler.execute(command, station_name=station_name, station_city=station_city, station_province=station_province)

    def resolve_update_station(self, info, station_id, **kwargs):
        # Use Command Handler to update a Station
        command = UpdateStationCommand()
        return handler.execute(command, station_id=station_id, **kwargs)

    def resolve_delete_station(self, info, station_id):
        # Use Command Handler to delete a Station
        command = DeleteStationCommand()
        return handler.execute(command, station_id=station_id)

    def resolve_undo_operation(self, info):
        # Undo the last operation
        handler.undo()
        return "Last operation undone successfully."

    def resolve_redo_operation(self, info):
        # Redo the last undone operation
        handler.redo()
        return "Last undone operation redone successfully."