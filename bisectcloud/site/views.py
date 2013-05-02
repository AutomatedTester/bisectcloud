"""Example views. Feel free to delete this app."""

import logging

from django.shortcuts import render

import bleach
import commonware
from funfactory.log import log_cef
from mobility.decorators import mobile_template
from session_csrf import anonymous_csrf
from models import TreeInfo, Platform


log = commonware.log.getLogger('playdoh')


@mobile_template('{mobile/}home.html')
def home(request, template=None):
    """Main example view."""
    data = {}  # You'd add data here that you're sending to the template.
    data['treeinfo'] = TreeInfo.objects.all()
    data['platforms'] = Platform.objects.all()
    log.debug("I'm alive!")
    return render(request, template, data)


