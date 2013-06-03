from django.db import IntegrityError

import requests
from models import Pushlog, Revisions


def get_pushlog():
    datazilla_request = \
        requests.get('https://datazilla.mozilla.org/refdata/pushlog/list/?days_ago=1&branches=Mozilla-Inbound')
    _store_pushlog_in_datastore(datazilla_request.json())


def _store_pushlog_in_datastore(push_json):
    for k, v in push_json.items():
        try:
            pushlog = Pushlog(push_id = k,
                              branch_name=push_json[k]['branch_name'])
            pushlog.save()
            for revision in push_json[k]['revisions']:
                revisions = Revisions(revisions=revision,
                                      pushlog=pushlog)
                revisions.save()
        except IntegrityError:
            # Since we can only get the data for 1 day we should just ignore
            # when we get duplicates. This will just fail silently. Other
            # errors will faill through silently.
            pass

