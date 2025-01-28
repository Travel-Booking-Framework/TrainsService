from abc import ABC, abstractmethod
from Train.models import TrainHall
import graphene
from graphene_django.types import DjangoObjectType


class TrainHallCommand(ABC):
    """Base Command class for TrainHall operations."""
    @abstractmethod
    def execute(self, **kwargs):
        pass

    @abstractmethod
    def undo(self, **kwargs):
        pass


class CreateTrainHallCommand(TrainHallCommand):
    def __init__(self):
        self.train_hall = None  # To store the created TrainHall for undo

    def execute(self, hall_name, hall_description=None):
        # Validate if the train hall with the same hall_name already exists
        if TrainHall.objects.filter(hall_name=hall_name).exists():
            raise Exception("Train Hall with this hall_name already exists.")
        # Create the TrainHall and store it for undo
        self.train_hall = TrainHall.objects.create(
            hall_name=hall_name,
            hall_description=hall_description
        )
        return self.train_hall

    def undo(self):
        # Delete the created TrainHall
        if self.train_hall:
            self.train_hall.delete()


class UpdateTrainHallCommand(TrainHallCommand):
    def __init__(self):
        self.previous_data = None  # To store the previous state for undo
        self.train_hall = None

    def execute(self, hall_id, **kwargs):
        try:
            # Fetch the TrainHall and store its previous state
            self.train_hall = TrainHall.objects.get(id=hall_id)
            self.previous_data = {field: getattr(self.train_hall, field) for field in kwargs}

            # Update the TrainHall
            for field, value in kwargs.items():
                setattr(self.train_hall, field, value)
            self.train_hall.save()
            return self.train_hall
        except TrainHall.DoesNotExist:
            raise Exception("Train Hall with this ID does not exist.")

    def undo(self):
        # Revert the TrainHall to its previous state
        if self.train_hall and self.previous_data:
            for field, value in self.previous_data.items():
                setattr(self.train_hall, field, value)
            self.train_hall.save()


class DeleteTrainHallCommand(TrainHallCommand):
    def __init__(self):
        self.deleted_data = None  # To store the deleted TrainHall's data for undo

    def execute(self, hall_id):
        try:
            # Fetch the TrainHall and delete it
            train_hall = TrainHall.objects.get(id=hall_id)
            self.deleted_data = {
                "hall_name": train_hall.hall_name,
                "hall_description": train_hall.hall_description
            }
            train_hall.delete()
            return f"Train Hall {train_hall.hall_name} deleted successfully."
        except TrainHall.DoesNotExist:
            raise Exception("Train Hall with this ID does not exist.")

    def undo(self):
        # Recreate the deleted TrainHall
        if self.deleted_data:
            TrainHall.objects.create(**self.deleted_data)


class TrainHallCommandHandler:
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
        
        
# Define GraphQL Type for TrainHall
class TrainHallType(DjangoObjectType):
    class Meta:
        model = TrainHall


# Shared handler instance
handler = TrainHallCommandHandler()


# Define Mutation for TrainHall
class TrainHallMutations(graphene.ObjectType):
    create_train_hall = graphene.Field(
        TrainHallType,
        hall_name=graphene.String(required=True),
        hall_description=graphene.String()
    )

    update_train_hall = graphene.Field(
        TrainHallType,
        hall_id=graphene.Int(required=True),
        hall_name=graphene.String(),
        hall_description=graphene.String()
    )

    delete_train_hall = graphene.String(
        hall_id=graphene.Int(required=True)
    )

    undo_operation = graphene.String()
    redo_operation = graphene.String()

    def resolve_create_train_hall(self, info, hall_name, hall_description=None):
        # Use Command Handler to create a TrainHall
        command = CreateTrainHallCommand()
        return handler.execute(command, hall_name=hall_name, hall_description=hall_description)

    def resolve_update_train_hall(self, info, hall_id, **kwargs):
        # Use Command Handler to update a TrainHall
        command = UpdateTrainHallCommand()
        return handler.execute(command, hall_id=hall_id, **kwargs)

    def resolve_delete_train_hall(self, info, hall_id):
        # Use Command Handler to delete a TrainHall
        command = DeleteTrainHallCommand()
        return handler.execute(command, hall_id=hall_id)

    def resolve_undo_operation(self, info):
        # Undo the last operation
        handler.undo()
        return "Last operation undone successfully."

    def resolve_redo_operation(self, info):
        # Redo the last undone operation
        handler.redo()
        return "Last undone operation redone successfully."