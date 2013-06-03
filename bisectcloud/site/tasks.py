import requests
from models import Pushlog, Revisions

def get_pushlog():
    pass

def _store_pushlog_in_datastore(push_json):
    for k, v in push_json.items():
        pushlog = Pushlog(push_id = k,
                          branch_name=push_json[k]['branch_name'])
        pushlog.save()
        for revision in push_json[k]['revisions']:
            revisions = Revisions(revisions=revision,
                                  pushlog=pushlog)
            revisions.save()


