# test suite for API views
import unittest
import os
import json

from app import create_app, db
from instance import config


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.org_data = {
            "name": "BHive",
            "description": "A bee hive of data for social good"
        }
        self.program_data = {
            "name": "Sample Program",
        }
        self.service_data = {
            "name": "Service",
            "organization_id": 1,
            "program_id": 1,
            "email": "service@mail.com",
            "url": "service.com",
            "fees": "1000",
            "status": "On"
        }

        self.location_data = {
            "name": "Chicago",
            "organization_id": 1,
            "description": "The windy city",
            "transportation": "Train, Uber",
            "longitude": "N41.8781",
            "latitude": "W87.6298"
        }

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client
        db.create_all()

    def tearDown(self):
        with self.app_context:
            db.session.remove()
            db.drop_all()
            self.app_context.pop()
            os.unlink(self.app.config.get('DATABASE'))



class OrganizationViewTestCase(BaseTestCase):
    """This class represents the Organization view test case."""

    def test_view_can_create_organization(self):
        """Test that the view can handle post requests to create an org."""
        res = self.client().post('/api/organizations/', data=self.org_data)
        self.assertEqual(res.status_code, 201)
        self.assertIn("BHive", str(res.data))

    def test_view_can_get_all_organizations(self):
        """Test that the view can get all created orgs."""
        another_org = {
            "name": "Andela",
            "description": "Train the next gen of tech leaders"
        }
        self.client().post('/api/organizations/', data=self.org_data)
        self.client().post('/api/organizations/', data=another_org)

        # now get all the created orgs
        response = self.client().get('/api/organizations/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Andela", str(response.data))

    def test_view_can_update_organization(self):
        """Test that view handle a PUT request to make a change on the org."""
        res = self.client().post('/api/organizations/', data=self.org_data)
        self.assertEqual(res.status_code, 201)
        self.assertIn("BHive", str(res.data))
        results = json.loads(res.data.decode())
        new_data = {
            "name": "BrightHive"
        }
        response = self.client().put('/api/organizations/{}'.format(results['id']),
                                     data=new_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("BrightHive", str(response.data))

    def test_view_can_delete_organization(self):
        """Test that the view can handle a DELETE request to delete an org."""
        res = self.client().post('/api/organizations/', data=self.org_data)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        response = self.client().delete('/api/organizations/{}'.format(results['id']))
        self.assertEqual(response.status_code, 202)


class ProgramViewTestCase(BaseTestCase):
    """This class represents the tests for the method view for the
    programs."""

    def test_view_can_create_program(self):
        """Test that the view can handle a POST request to create a program."""
        # first create the org to own the program
        org_res = self.client().post('/api/organizations/', data=self.org_data)
        org_id = json.loads(org_res.data.decode())['id']
        # then, create the program under the org
        self.program_data['organization_id'] = org_id
        res = self.client().post('/api/organizations/{}/programs/'.format(org_id),
                           data=self.program_data)
        self.assertEqual(res.status_code, 201)
        self.assertIn("Sample Program", str(res.data))

    def test_view_can_get_all_programs(self):
        """Test that the view can handle a GET(all) programs request."""
        # first, create the org that owns the program
        res = self.client().post('/api/organizations/', data=self.org_data)
        results = json.loads(res.data.decode())
        org_id = results['id']
        # first create the programs
        self.program_data['organization_id'] = org_id
        another_prog = {
            "organization_id": org_id,
            "name": "Another Program"
        }
        # then, create the programs under the org
        prog_res0 = self.client().post(
            '/api/organizations/{}/programs/'.format(org_id),
            data=self.program_data)
        self.assertEqual(prog_res0.status_code, 201)
        prog_res1 = self.client().post(
            '/api/organizations/{}/programs/'.format(org_id),
            data=another_prog)
        self.assertEqual(prog_res1.status_code, 201)

        # finally, get all
        res = self.client().get('/api/organizations/{}/programs/'.format(org_id))
        self.assertEqual(res.status_code, 200)
        # self.assertIn("Another Program", str(res.data))
        self.assertIn("Sample Program", str(res.data))

    def test_view_can_get_program_by_id(self):
        """Test that the view can handle a GET(single) program by id."""
        res = self.client().post('/api/organizations/', data=self.org_data)
        org_id = json.loads(res.data.decode())['id']

        self.program_data['organization_id'] = org_id
        # create the program
        program_res = self.client().post(
            '/api/organizations/{}/programs/'.format(org_id),
            data=self.program_data)

        # get the program using its id
        program_id = json.loads(program_res.data.decode())['id']
        get_res = self.client().get(
            '/api/organizations/{}/programs/{}'.format(org_id, program_id))
        self.assertEqual(get_res.status_code, 200)
        self.assertIn("Sample Program", str(get_res.data))

    def test_view_can_update_program(self):
        """Test that the view can handle a PUT request to update a program."""
        res = self.client().post('/api/organizations/', data=self.org_data)
        org_id = json.loads(res.data.decode())['id']

        self.program_data['organization_id'] = org_id
        # create the program
        program_res = self.client().post(
            '/api/organizations/{}/programs/'.format(org_id),
            data=self.program_data)

        # update the program given its id
        updated_program = {
            "name": "Updated Program"
        }
        program_id = json.loads(program_res.data.decode())['id']
        response = self.client().put(
            '/api/organizations/{}/programs/{}'.format(org_id, program_id),
            data=updated_program)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated Program", str(response.data))

    def test_view_can_delete_program(self):
        """Test that the view can handle DELETE request to remove a
        program."""
        res = self.client().post('/api/organizations/', data=self.org_data)
        org_id = json.loads(res.data.decode())['id']

        self.program_data['organization_id'] = org_id
        # create the program
        program_res = self.client().post(
            '/api/organizations/{}/programs/'.format(org_id),
            data=self.program_data)

        # update the program given its id
        program_id = json.loads(program_res.data.decode())['id']
        response = self.client().delete(
            '/api/organizations/{}/programs/{}'.format(org_id, program_id))
        self.assertEqual(response.status_code, 202)
        # test to see if its been deleted
        rv = self.client().get('/api/organizations/1/programs/1')
        self.assertEqual(rv.status_code, 404)


class ServiceViewTestCase(BaseTestCase):
    """This class represents the tests for the service method view."""
    def create_org(self):
        self.org_data = {
            "name": "BHive",
            "description": "A bee hive of data for social good"
        }
        return self.client().post('/api/organizations/', data=self.org_data)

    def create_program(self):
        self.program_data = {
        "name": "Program",
        "organization_id": 1
        }
        return self.client().post('/api/organizations/1/programs/',
                                  data=self.program_data)

    def test_view_can_create_service(self):
        """Test that the view can handle POST request to create a service"""
        # create the org and its program
        self.create_org()
        self.create_program()

        # create the service under a program
        service_res = self.client().post(
            '/api/organizations/1/programs/1/services/',
            data=self.service_data)
        self.assertEqual(service_res.status_code, 201)
        self.assertIn("service.com", str(service_res.data))

    def test_view_allows_service_creation_without_program_id(self):
        """Test that the view can handle POST request for a service without a
        program id
        """
        self.create_org()
        service_with_no_prog_id = {
            "name": "Service",
            "organization_id": 1,
            "email": "service@mail.com",
            "url": "service.com",
            "fees": "1000",
            "status": "On"
        }
        service = self.client().post(
            '/api/organizations/1/services/',
            data=service_with_no_prog_id)
        self.assertEqual(service.status_code, 201)


    def test_view_can_get_a_service(self):
        """Test that the view can handle GET request for  existing
        service using its ID.
        """
        # create the org and program
        self.create_org()
        self.create_program()

        # create the service
        service_res = self.client().post(
            '/api/organizations/1/programs/1/services/',
            data=self.service_data)
        # get the service by id
        res = self.client().get('/api/organizations/1/programs/1/services/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Service", str(res.data))

    def test_view_can_get_all_services(self):
        """Test that the view can handle GET request for all existing
        services.
        """
        # create org and program
        self.create_org()
        self.create_program()

        # create service
        service_res = self.client().post(
            '/api/organizations/1/programs/1/services/',
            data=self.service_data)
        # get all the services
        res = self.client().get('/api/organizations/1/programs/1/services/')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Service", str(res.data))

    def test_view_can_update_service(self):
        """Test that a view can handle a PUT request to update a service."""
        # create the org and program
        self.create_org()
        self.create_program()

        # create the service
        service_res = self.client().post(
            '/api/organizations/1/programs/1/services/',
            data=self.service_data)
        # update the service with new data
        new_data = {
            "name": "Updated Service",
            "url": "updatedurl.com"
        }
        res = self.client().put(
            '/api/organizations/1/programs/1/services/1',
            data=new_data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Updated Service", str(res.data))

    def test_view_can_delete_service(self):
        """Test view handles DELETE request to delete a service correctly."""
        self.create_org()
        self.create_program()

        self.client().post(
            '/api/organizations/1/programs/1/services/',
            data=self.service_data)
        res = self.client().delete(
            '/api/organizations/1/programs/1/services/1')
        self.assertEqual(res.status_code, 202)
        self.assertNotIn("Service", str(res.data))
         # check to see if it's deleted
        response = self.client().get('/api/organizations/1/programs/1/services/1')
        self.assertEqual(response.status_code, 404)



class LocationViewTestCase(BaseTestCase):
    """This class represents the tests for the location method view."""

    def create_org(self):
        self.org_data = {
            "name": "BHive",
            "description": "A bee hive of data for social good"
        }

        return self.client().post('/api/organizations/',
                                  data=self.org_data)

    def test_view_can_create_location(self):
        """Test view handles a POST request to create a location entry."""

        self.create_org()

        res = self.client().post('/api/organizations/1/locations/',
                           data=self.location_data)
        self.assertEqual(res.status_code, 201)
        self.assertIn("Chicago", str(res.data))

    def test_view_can_get_a_location(self):
        """Test view handles a GET (one) request correctly."""

        self.create_org()

        #create the location
        self.client().post('/api/organizations/1/locations/',
                           data=self.location_data)
        # get the location using its id
        res = self.client().get('/api/organizations/1/locations/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Chicago", str(res.data))

    def test_view_can_get_all_locations(self):
        """Test view handles a GET(all) request for a given org."""

        self.create_org()

        # create locations
        self.client().post('/api/organizations/1/locations/',
                           data=self.location_data)
        res = self.client().get('/api/organizations/1/locations/')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Chicago", str(res.data))

    def test_view_can_update_a_location(self):
        """Test view handles a PUT request to update a location."""
        self.create_org()

        new_data = {
            "name": "Chicago Loop"
        }
        # create location
        self.client().post('/api/organizations/1/locations/',
                           data=self.location_data)
        # update the location
        res = self.client().put('/api/organizations/1/locations/1',
                                data=new_data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Chicago Loop", str(res.data))

    def test_view_can_delete_location(self):
        """Test view handles a DELETE request to delete a location."""

        self.create_org()
        # create a location
        self.client().post('/api/organizations/1/locations/',
                           data=self.location_data)
        # delete a location
        res = self.client().delete('/api/organizations/1/locations/1')
        self.assertEqual(res.status_code, 202)
        self.assertNotIn("Chicago", str(res.data))
        self.assertEqual({}, json.loads(res.data.decode()))
        # check to see if it's deleted
        response = self.client().get('/api/organizations/1/locations/1')
        self.assertEqual(response.status_code, 404)


class PhysicalAddressViewTestCase(BaseTestCase):
    """This class represents the tests for the location method view."""

    address_data = {
        "location_id": 1,
        "address": "",
        "city": "Chicago",
        "state": "IL",
        "postal_code": "60601",
        "country": "US"
    }

    def create_org(self):
        """Reusable utility to create an organization."""
        self.org_data = {
            "name": "BHive",
            "description": "A bee hive of data for social good"
        }

        return self.client().post('/api/organizations/',
                                  data=self.org_data)

    def create_location(self):
        """Reusable utility to create location."""
        return self.client().post('/api/organizations/1/locations/',
                                  data=self.location_data)

    def test_view_can_create_address(self):
        """Test view handles a POST request to create a physical address entry."""

        self.create_org()
        self.create_location()
        # create the physical address
        res = self.client().post('/api/organizations/1/locations/1/addresses/',
                           data=self.address_data)
        self.assertEqual(res.status_code, 201)
        self.assertIn("Chicago", str(res.data))

    def test_view_can_get_an_address(self):
        """Test view handles a GET (one) request for a physical address correctly."""

        self.create_org()
        self.create_location()

        #create the address
        res = self.client().post('/api/organizations/1/locations/1/addresses/',
                                 data=self.address_data)

        # get the address using its id
        res = self.client().get('/api/organizations/1/locations/1/addresses/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Chicago", str(res.data))

    def test_view_can_get_all_addresses(self):
        """Test view handles a GET(all) physical address request for a given location."""

        self.create_org()
        self.create_location()

        # create physical address
        self.client().post('/api/organizations/1/locations/1/addresses/',
                           data=self.address_data)
        res = self.client().get('/api/organizations/1/locations/1/addresses/')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Chicago", str(res.data))

    def test_view_can_update_a_physical_address(self):
        """Test view handles a PUT request to update a location's address."""

        self.create_org()
        self.create_location()

        new_data = {
            "postal_code": "60603"
        }
        # create address
        self.client().post('/api/organizations/1/locations/1/addresses/',
                           data=self.address_data)
        # update the address
        res = self.client().put('/api/organizations/1/locations/1/addresses/1',
                                data=new_data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("60603", str(res.data))

    def test_view_can_delete_a_physical_address(self):
        """Test view handles a DELETE request to delete an address."""

        self.create_org()
        self.create_location()
        # create an address
        self.client().post('/api/organizations/1/locations/1/addresses/',
                           data=self.address_data)
        # delete the address
        res = self.client().delete('/api/organizations/1/locations/1/addresses/1')
        self.assertEqual(res.status_code, 202)
        self.assertNotIn("Chicago", str(res.data))
        self.assertEqual({}, json.loads(res.data.decode()))
        # check to see if it's deleted
        response = self.client().get(
            '/api/organizations/1/locations/1/addresses/1')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    # make the tests conveniently executable
    unittest.main()
