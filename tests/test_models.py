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

    def test_organization_creation(self):
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

    def test_program_creation(self):
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

    def test_service_creation(self):
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



