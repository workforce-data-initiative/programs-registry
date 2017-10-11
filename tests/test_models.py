# test suite for the models
import unittest
import os

from app import create_app, db
from app.models import Organization, Service, Program, Location, \
                       ServiceLocation, PhysicalAddress
from instance import config


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        registry_app = create_app(config_name="testing")
        self.app = registry_app

        self.client = self.app.test_client
        # bind the app to the application context
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            # os.ulink(self.app.config.get('DATABASE_URL'))


class OrganizationTestCase(BaseTestCase):
    """This class represents the Organization model test case."""

    def test_organization_instance_creation(self):
        """Test that the organization model can be created."""
        org_data = {
            "name": "Test-Org",
            "description": "Test Description"
        }
        old_count = Organization.query.count()
        organization = Organization(**org_data)
        organization.save()
        new_count = Organization.query.count()
        self.assertNotEqual(new_count, old_count)


class ProgramTestCase(BaseTestCase):
    """This class represents the program model test case."""

    def test_program_instance_creation(self):
        """Test that a program can be created."""
        program_data = {
            "name": "Test program",
            "organization_id": 1,
        }
        old_count = Program.query.count()
        program = Program(**program_data)
        program.save()
        new_count = Program.query.count()
        self.assertNotEqual(old_count, new_count)


class ServiceModelTestCase(BaseTestCase):
    """This class represents the service model test case."""

    def test_service_instance_creation(self):
        """Test that a given service under an org can be created."""
        org_data= {
            "name": "A good org",
            "description": "A big org"
        }
        program_data = {
            "name": "Test program",
            "organization_id": 1,
        }
        # Create the org and program
        organization = Organization(**org_data)
        organization.save()
        program = Program(**program_data)
        program.save()

        service_data = {
            "name": "A good service",
            "organization_id": organization.id,
            "program_id": program.id
        }

        old_count = Service.query.count()
        service = Service(**service_data)
        service.save()
        new_count = Service.query.count()
        self.assertNotEqual(new_count, old_count)


class LocationModelTestCase(BaseTestCase):
    """This class represents the location model test case."""

    def test_location_instance_creation(self):
        """Test that a location can be created."""

        # first, create the organization
        org_data = {
            "name": "An org",
            "description": "A really big org"
        }
        organization = Organization(**org_data)
        organization.save()

        location_data = {
            "name": "BrightHive",
            "organization_id": organization.id,
            "alternate_name": "another name",
            "description": "Making sense of data"
        }
        old_count = Location.query.count()
        location_instance = Location(**location_data)
        location_instance.save()
        new_count = Location.query.count()
        self.assertNotEqual(new_count, old_count)


class PhysicalAddressModelTestCase(BaseTestCase):
    """This class represents the physical address model test case."""

    def test_physical_address_instance_creation(self):
        """Test that an instance of physical address can be created."""

        # first, create the organization
        org_data = {
            "name": "An org",
            "description": "A really big org"
        }
        organization = Organization(**org_data)
        organization.save()

        # then, create the location
        location_data = {
            "name": "BrightHive",
            "organization_id": organization.id,
            "alternate_name": "another name",
            "description": "Making sense of data"
        }

        location_instance = Location(**location_data)
        location_instance.save()

        # then create the physical address of the org
        physical_address_data = {
            "location_id": location_instance.id,
            "address": "123 State St",
            "city": "Chicago",
            "state": "Illinois",
            "postal_code": "60621",
            "country": "US"
        }
        old_count = PhysicalAddress.query.count()
        address = PhysicalAddress(**physical_address_data)
        address.save()
        new_count = PhysicalAddress.query.count()
        self.assertNotEqual(new_count, old_count)

