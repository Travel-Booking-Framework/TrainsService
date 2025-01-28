from abc import ABC, abstractmethod
from Train.models import RailwayCompany
import graphene
from graphene_django.types import DjangoObjectType


class RailwayCompanyCommand(ABC):
    """Base Command class for RailwayCompany operations."""
    @abstractmethod
    def execute(self, **kwargs):
        pass

    @abstractmethod
    def undo(self, **kwargs):
        pass


class CreateRailwayCompanyCommand(RailwayCompanyCommand):
    def __init__(self):
        self.company = None  # To store the created RailwayCompany for undo

    def execute(self, railway_name, railway_description, refund_policy, railway_logo=None):
        # Validate if the railway company with the same railway_name already exists
        if RailwayCompany.objects.filter(railway_name=railway_name).exists():
            raise Exception("Railway Company with this railway_name already exists.")
        # Create the RailwayCompany and store it for undo
        self.company = RailwayCompany.objects.create(
            railway_name=railway_name,
            railway_description=railway_description,
            refund_policy=refund_policy,
            railway_logo=railway_logo
        )
        return self.company

    def undo(self):
        # Delete the created RailwayCompany
        if self.company:
            self.company.delete()


class UpdateRailwayCompanyCommand(RailwayCompanyCommand):
    def __init__(self):
        self.previous_data = None  # To store the previous state for undo
        self.company = None

    def execute(self, company_id, **kwargs):
        try:
            # Fetch the RailwayCompany and store its previous state
            self.company = RailwayCompany.objects.get(id=company_id)
            self.previous_data = {field: getattr(self.company, field) for field in kwargs}

            # Update the RailwayCompany
            for field, value in kwargs.items():
                setattr(self.company, field, value)
            self.company.save()
            return self.company
        except RailwayCompany.DoesNotExist:
            raise Exception("Railway Company with this ID does not exist.")

    def undo(self):
        # Revert the RailwayCompany to its previous state
        if self.company and self.previous_data:
            for field, value in self.previous_data.items():
                setattr(self.company, field, value)
            self.company.save()


class DeleteRailwayCompanyCommand(RailwayCompanyCommand):
    def __init__(self):
        self.deleted_data = None  # To store the deleted RailwayCompany's data for undo

    def execute(self, company_id):
        try:
            # Fetch the RailwayCompany and delete it
            company = RailwayCompany.objects.get(id=company_id)
            self.deleted_data = {
                "railway_name": company.railway_name,
                "railway_description": company.railway_description,
                "refund_policy": company.refund_policy,
                "railway_logo": company.railway_logo
            }
            company.delete()
            return f"Railway Company {company.railway_name} deleted successfully."
        except RailwayCompany.DoesNotExist:
            raise Exception("Railway Company with this ID does not exist.")

    def undo(self):
        # Recreate the deleted RailwayCompany
        if self.deleted_data:
            RailwayCompany.objects.create(**self.deleted_data)


class RailwayCompanyCommandHandler:
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


# Define GraphQL Type for RailwayCompany
class RailwayCompanyType(DjangoObjectType):
    class Meta:
        model = RailwayCompany


# Shared handler instance
handler = RailwayCompanyCommandHandler()


# Define Mutation for RailwayCompany
class RailwayCompanyMutations(graphene.ObjectType):
    create_railway_company = graphene.Field(
        RailwayCompanyType,
        railway_name=graphene.String(required=True),
        railway_description=graphene.String(),
        refund_policy=graphene.String(required=True),
        railway_logo=graphene.String()
    )

    update_railway_company = graphene.Field(
        RailwayCompanyType,
        company_id=graphene.Int(required=True),
        railway_name=graphene.String(),
        railway_description=graphene.String(),
        refund_policy=graphene.String(),
        railway_logo=graphene.String()
    )

    delete_railway_company = graphene.String(
        company_id=graphene.Int(required=True)
    )

    undo_operation = graphene.String()
    redo_operation = graphene.String()

    def resolve_create_railway_company(self, info, railway_name, railway_description, refund_policy, railway_logo=None):
        # Use Command Handler to create a RailwayCompany
        command = CreateRailwayCompanyCommand()
        return handler.execute(command, railway_name=railway_name, railway_description=railway_description, refund_policy=refund_policy, railway_logo=railway_logo)

    def resolve_update_railway_company(self, info, company_id, **kwargs):
        # Use Command Handler to update a RailwayCompany
        command = UpdateRailwayCompanyCommand()
        return handler.execute(command, company_id=company_id, **kwargs)

    def resolve_delete_railway_company(self, info, company_id):
        # Use Command Handler to delete a RailwayCompany
        command = DeleteRailwayCompanyCommand()
        return handler.execute(command, company_id=company_id)

    def resolve_undo_operation(self, info):
        # Undo the last operation
        handler.undo()
        return "Last operation undone successfully."

    def resolve_redo_operation(self, info):
        # Redo the last undone operation
        handler.redo()
        return "Last undone operation redone successfully."