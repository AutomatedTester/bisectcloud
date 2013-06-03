import os
import json
import urllib

import test_utils
import bisectcloud.site.tasks as task
from bisectcloud.site.models import *

class TaskTests(test_utils.TestCase):
    add_job = "/en-US/job/add"

    def test_we_can_call_tasks(self):
        pass

    def test_we_can_store_json_blob_in_datastore(self):
        with open(os.path.join(os.path.dirname(__file__),'pushlog.json'), 'r') as f:
            jsonblob = f.read()
        rev_len = len(Revisions.objects.all())
        push_len = len(Pushlog.objects.all())
        task._store_pushlog_in_datastore(json.loads(jsonblob))

        self.assertEqual(rev_len + 4, len(Revisions.objects.all()))
        self.assertEqual(push_len + 3, len(Pushlog.objects.all()))

    def test_we_can_store_json_blob_in_datastore_and_silently_ignore_duplicates(self):
        with open(os.path.join(os.path.dirname(__file__),'pushlog.json'), 'r') as f:
            jsonblob = f.read()
        rev_len = len(Revisions.objects.all())
        push_len = len(Pushlog.objects.all())

        task._store_pushlog_in_datastore(json.loads(jsonblob))

        self.assertEqual(rev_len + 4, len(Revisions.objects.all()))
        self.assertEqual(push_len + 3, len(Pushlog.objects.all()))

        # Just send this through again and it shouldnt error and keep the same 
        # amount of data
        task._store_pushlog_in_datastore(json.loads(jsonblob))

        self.assertEqual(rev_len + 4, len(Revisions.objects.all()))
        self.assertEqual(push_len + 3, len(Pushlog.objects.all()))

    def test_we_can_error_and_update_datastore_if_task_details_arent_about(self):
        data = {
            "hg-bad": "123123123123",
            "hg-good": "123123123123",
            "test": "fooobar",
            "platform": "ubuntu64",
            "tree": "mozilla-central"
        }
        self.client.post(self.add_job, urllib.urlencode(data), content_type='application/json' )

        task._find_revisions(data['hg-bad'], data['hg-good'])
        task_master = TaskMaster.objects.filter(bad=data['hg-bad'], good=data['hg-good'])[0]
        self.assertEqual('task errored', task_master.current_status)
