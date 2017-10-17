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




if __name__ == '__main__':
    # make the tests conveniently executable
    unittest.main()
