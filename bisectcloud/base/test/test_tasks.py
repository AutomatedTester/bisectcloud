import os
import json


import test_utils
import bisectcloud.site.tasks as task
from bisectcloud.site.models import *

class TaskTests(test_utils.TestCase):

    def test_we_can_call_tasks(self):
        pass

    def test_we_can_store_json_blob_in_datastore(self):
        with open(os.path.join(os.path.dirname(__file__),'pushlog.json'), 'r') as f:
            jsonblob = f.read()

        task._store_pushlog_in_datastore(json.loads(jsonblob))

        self.assertEqual(4, len(Revisions.objects.all()))
        self.assertEqual(3, len(Pushlog.objects.all()))

