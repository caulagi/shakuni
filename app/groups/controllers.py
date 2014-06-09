# -*- coding: utf-8 -*-
"""
    Manage the groups

    :copyright: (c) 2014 by Pradip P Caulagi.
    :license: MIT, see LICENSE for more details.
"""

import logging

from flask import Flask, render_template, request, g, session, flash, \
     redirect, url_for, abort
from flask import Blueprint

#from app.groups.models import Group

# setup logger
logger = logging.getLogger('shakuni-groups')

# set up blueprint
groups_blueprint = Blueprint('groups_blueprint', __name__)

def init(application):

    @groups_blueprint.route('/create', methods=['GET', 'POST'])
    def create():
        pass

    @groups_blueprint.route('/list')
    def list():
        pass
