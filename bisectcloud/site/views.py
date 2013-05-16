"""Example views. Feel free to delete this app."""

import logging
import json

from django.shortcuts import render
from django.http import HttpResponse

import commonware
from funfactory.log import log_cef
from mobility.decorators import mobile_template
from session_csrf import anonymous_csrf
from models import TreeInfo, Platform, TaskMaster


log = commonware.log.getLogger('playdoh')


@mobile_template('{mobile/}home.html')
def home(request, template=None):
    """Main example view."""
    data = {}  # You'd add data here that you're sending to the template.
    data['treeinfo'] = TreeInfo.objects.all()
    data['platforms'] = Platform.objects.all()
    log.debug("I'm alive!")
    return render(request, template, data)

def add_job(request):
    if request.method == 'GET':
        return HttpResponse('GET is not allowed to this endpoint')
    doc = json.loads(request.body)

    platforms_data = Platform.objects.all()
    platform = [plat.name for plat in platforms_data]
    if doc['platform'] not in platform:
        return HttpResponse('Invalid field value in plaform')

    trees_data = TreeInfo.objects.all()
    trees = [tree.name for tree in trees_data]
    if doc['tree'] not in trees:
        return HttpResponse('Invalid field value in tree')

    try:
        taskmaster = TaskMaster(bad=doc['bad'],
                                good = doc['good'],
                                test = doc['test'],
                                platform = [platform for platform in platforms_data \
                                           if doc['platform'] == platform.name][0],
                                tree = [tree for tree in trees_data if doc['tree'] == tree.name][0])
        taskmaster.save()
        return HttpResponse('Task submitted')
    except Exception as e:
        return HttpResponse('There has been an error while saving. %s' % e)

def cancel_job(request):
    if request.method == 'GET':
        return HttpResponse('GET is not allowed to this endpoint')
    doc = json.loads(request.body)
    if not doc.has_key('id'):
        return HttpResponse('Data not recognised')
    try:
        task_item = TaskMaster.objects.get(id=doc['id'])
        task_item.cancelled = True
        return HttpResponse("Task has been cancelled")
    except TaskMaster.DoesNotExist:
        return HttpResponse("Task ID not found so can't be cancelled")

