from abc import ABC, abstractmethod
from Train.models import Train
import graphene
from graphene_django.types import DjangoObjectType


class TrainCommand(ABC):
    """Base Command class for Train operations."""
    @abstractmethod
    def execute(self, **kwargs):
        pass

    @abstractmethod
    def undo(self, **kwargs):
        pass


class CreateTrainCommand(TrainCommand):
    def __init__(self):
        self.train = None  # To store the created Train for undo

    def execute(self, train_number, departure_datetime, arrival_datetime,
                departure_station, arrival_station, railway_company,
                train_type, capacity, hall, stars, base_price, tax, discount):
        # Validate if the train with the same number already exists
        if Train.objects.filter(train_number=train_number).exists():
            raise Exception("Train with this number already exists.")
        # Create the Train and store it for undo
        self.train = Train.objects.create(
            train_number=train_number,
            departure_datetime=departure_datetime,
            arrival_datetime=arrival_datetime,
            departure_station=departure_station,
            arrival_station=arrival_station,
            railway_company=railway_company,
            train_type=train_type,
            capacity=capacity,
            hall=hall,
            stars=stars,
            base_price=base_price,
            tax=tax,
            discount=discount
        )
        return self.train

    def undo(self):
        # Delete the created Train
        if self.train:
            self.train.delete()


class UpdateTrainCommand(TrainCommand):
    def __init__(self):
        self.previous_data = None  # To store the previous state for undo
        self.train = None

    def execute(self, train_id, **kwargs):
        try:
            # Fetch the Train and store its previous state
            self.train = Train.objects.get(id=train_id)
            self.previous_data = {field: getattr(self.train, field) for field in kwargs}

            # Update the Train
            for field, value in kwargs.items():
                setattr(self.train, field, value)
            self.train.save()
            return self.train
        except Train.DoesNotExist:
            raise Exception("Train with this ID does not exist.")

    def undo(self):
        # Revert the Train to its previous state
        if self.train and self.previous_data:
            for field, value in self.previous_data.items():
                setattr(self.train, field, value)
            self.train.save()


class DeleteTrainCommand(TrainCommand):
    def __init__(self):
        self.deleted_data = None  # To store the deleted Train's data for undo

    def execute(self, train_id):
        try:
            # Fetch the Train and delete it
            train = Train.objects.get(id=train_id)
            self.deleted_data = {
                "train_number": train.train_number,
                "departure_datetime": train.departure_datetime,
                "arrival_datetime": train.arrival_datetime,
                "departure_station": train.departure_station,
                "arrival_station": train.arrival_station,
                "railway_company": train.railway_company,
                "train_type": train.train_type,
                "capacity": train.capacity,
                "hall": train.hall,
                "stars": train.stars,
                "base_price": train.base_price,
                "tax": train.tax,
                "discount": train.discount
            }
            train.delete()
            return f"Train {train.train_number} deleted successfully."
        except Train.DoesNotExist:
            raise Exception("Train with this ID does not exist.")

    def undo(self):
        # Recreate the deleted Train
        if self.deleted_data:
            Train.objects.create(**self.deleted_data)


class TrainCommandHandler:
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


# Define GraphQL Type for Train
class TrainType(DjangoObjectType):
    class Meta:
        model = Train


# Shared handler instance
handler = TrainCommandHandler()


# Define Mutation for Train
class TrainMutations(graphene.ObjectType):
    create_train = graphene.Field(
        TrainType,
        train_number=graphene.String(required=True),
        departure_datetime=graphene.String(required=True),
        arrival_datetime=graphene.String(required=True),
        departure_station=graphene.Int(required=True),
        arrival_station=graphene.Int(required=True),
        railway_company=graphene.Int(required=True),
        train_type=graphene.String(required=True),
        capacity=graphene.Int(required=True),
        hall=graphene.Int(required=True),
        stars=graphene.Int(required=True),
        base_price=graphene.Float(required=True),
        tax=graphene.Float(required=True),
        discount=graphene.Float(required=True)
    )

    update_train = graphene.Field(
        TrainType,
        train_id=graphene.Int(required=True),
        train_number=graphene.String(),
        departure_datetime=graphene.String(),
        arrival_datetime=graphene.String(),
        base_price=graphene.Float(),
        tax=graphene.Float(),
        discount=graphene.Float()
    )

    delete_train = graphene.String(
        train_id=graphene.Int(required=True)
    )

    undo_operation = graphene.String()
    redo_operation = graphene.String()

    def resolve_create_train(self, info, **kwargs):
        # Use Command Handler to create a Train
        command = CreateTrainCommand()
        return handler.execute(command, **kwargs)

    def resolve_update_train(self, info, train_id, **kwargs):
        # Use Command Handler to update a Train
        command = UpdateTrainCommand()
        return handler.execute(command, train_id=train_id, **kwargs)

    def resolve_delete_train(self, info, train_id):
        # Use Command Handler to delete a Train
        command = DeleteTrainCommand()
        return handler.execute(command, train_id=train_id)

    def resolve_undo_operation(self, info):
        # Undo the last operation
        handler.undo()
        return "Last operation undone successfully."

    def resolve_redo_operation(self, info):
        # Redo the last undone operation
        handler.redo()
        return "Last undone operation redone successfully."