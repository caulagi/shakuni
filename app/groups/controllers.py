# -*- coding: utf-8 -*-
"""
    Manage the groups

    :copyright: (c) 2014 by Pradip P Caulagi.
    :license: MIT, see LICENSE for more details.
"""

import logging

from flask import render_template, g, abort, url_for, redirect, \
    request
from flask import Blueprint

#from app.groups.models import Group
from app.groups.forms import GroupForm

# setup logger
logger = logging.getLogger('shakuni-groups')

# set up blueprint
groups_blueprint = Blueprint('groups_blueprint', __name__)

def init(application):

    @groups_blueprint.route('/create', methods=['GET', 'POST'])
    def create():
        if not g.user:
            abort(401)
        form = GroupForm(request.form)
        if form.validate_on_submit():
            pass
        return render_template("groups/create.html", form=form)
        

    @groups_blueprint.route('/list')
    def list():
        pass
