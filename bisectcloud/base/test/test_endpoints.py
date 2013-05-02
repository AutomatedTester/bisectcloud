import test_utils
import json
from bisectcloud.site.models import TaskMaster 

class EndPoints(test_utils.TestCase):
    fixtures = ['site.json']

    def test_we_can_post_payload_to_start_bisect_and_stored_in_database(self):
        data = {
            "bad": "123123123123",
            "good": "123123123123",
            "test": "fooobar",
            "platform": "ubuntu64",
            "tree": "mozilla-central"
        }
        response = self.client.post("/en-US/add_job", json.dumps(data), content_type='application/json' )
        self.assertEqual(200, response.status_code)
        self.assertEqual('Task submitted', response.content)
        self.assertEqual(1, len(TaskMaster.objects.filter(bad = '123123123123')))

    def test_should_send_an_error_if_a_get_is_done_to_add_job(self):
        response = self.client.get('/en-US/add_job')
        self.assertEqual(200, response.status_code)
        self.assertEqual('GET is not allowed to this endpoint', response.content)

    def test_should_receive_error_if_platform_not_in_database(self):
        data = {
            "bad": "123123123123",
            "good": "123123123123",
            "test": "fooobar",
            "platform": "foogbar",
            "tree": "mozilla-central"
        }
        response = self.client.post('/en-US/add_job', json.dumps(data), content_type='application/json')
        self.assertEqual("Invalid field value in plaform", response.content)
    
    def test_should_receive_error_if_tree_not_in_database(self):
        data = {
            "bad": "123123123123",
            "good": "123123123123",
            "test": "fooobar",
            "platform": "ubuntu64",
            "tree": "mozilla"
        }
        response = self.client.post('/en-US/add_job', json.dumps(data), content_type='application/json')
        self.assertEqual("Invalid field value in tree", response.content)
