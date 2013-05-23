import test_utils
import json
from bisectcloud.site.models import TaskMaster 
import urllib
from django.core import serializers

class EndPoints(test_utils.TestCase):
    fixtures = ['site.json']
    add_job = "/en-US/job/add"
    cancel_job = "/en-US/job/cancel"
    jobs = "/en-US/job"

    def test_we_can_post_payload_to_start_bisect_and_stored_in_database(self):
        data = {
            "hg-bad": "123123123123",
            "hg-good": "123123123123",
            "test": "fooobar",
            "platform": "ubuntu64",
            "tree": "mozilla-central"
        }
        response = self.client.post(self.add_job, urllib.urlencode(data), content_type='application/json' )
        self.assertEqual(200, response.status_code)
        self.assertEqual('Task submitted', response.content)
        self.assertEqual(1, len(TaskMaster.objects.filter(bad='123123123123')))

    def test_should_send_an_error_if_a_get_is_done_to_add_job(self):
        response = self.client.get(self.add_job)
        self.assertEqual(200, response.status_code)
        self.assertEqual('GET is not allowed to this endpoint', response.content)

    def test_should_receive_error_if_platform_not_in_database(self):
        data = {
            "hg-bad": "123123123123",
            "hg-good": "123123123123",
            "test": "fooobar",
            "platform": "foogbar",
            "tree": "mozilla-central"
        }
        response = self.client.post(self.add_job, urllib.urlencode(data), content_type='application/json')
        self.assertEqual("Invalid field value in plaform", response.content)

    def test_should_receive_error_if_tree_not_in_database(self):
        data = {
            "hg-bad": "123123123123",
            "hg-good": "123123123123",
            "test": "fooobar",
            "platform": "ubuntu64",
            "tree": "mozilla"
        }
        response = self.client.post(self.add_job, urllib.urlencode(data), content_type='application/json')
        self.assertEqual("Invalid field value in tree", response.content)

    def test_should_be_able_to_cancel_bisects(self):
        data = {
            "id": 1
        }
        response = self.client.post(self.cancel_job, urllib.urlencode(data), content_type='application/type')
        self.assertEqual(200, response.status_code)
        self.assertEqual("Task has been cancelled", response.content)

    def test_should_error_gracefully_if_job_doesnt_exist(self):
        data = {
            "id": 100000000000
        }
        response = self.client.post(self.cancel_job, urllib.urlencode(data), content_type='application/type')
        self.assertEqual(200, response.status_code)
        self.assertEqual("Task ID not found so can't be cancelled", response.content)

    def test_should_error_if_user_sends_data_in_wrong_shape(self):
        data = {
            "willNeverExist": "what are you doing????"
        }
        response = self.client.post(self.cancel_job, urllib.urlencode(data), content_type='application/type')
        self.assertEqual(200, response.status_code)
        self.assertEqual("Data not recognised", response.content)

    def test_that_a_get_to_cancel_job_returns_error_message(self):
        response = self.client.get(self.cancel_job)
        self.assertEqual(200, response.status_code)
        self.assertEqual("GET is not allowed to this endpoint", response.content)

    def test_that_we_get_error_message_when_we_post_to_top_jobs(self):
        response = self.client.post(self.jobs, urllib.urlencode({}), content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual("POST is not allowed to this endpoint", response.content)

    def test_that_we_get_data_back_from_get_to_top_jobs(self):
        response = self.client.get(self.jobs)
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(1, len(data['records']))
