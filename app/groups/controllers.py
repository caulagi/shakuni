# -*- coding: utf-8 -*-
"""
    Manage the groups

    :copyright: (c) 2014 by Pradip P Caulagi.
    :license: MIT, see LICENSE for more details.
"""

import logging

from flask import render_template, g, abort, url_for, redirect, \
    request, flash
from flask import Blueprint

from app.groups.models import Group, MemberOf
from app.groups.forms import GroupForm

# setup logger
logger = logging.getLogger('shakuni-groups')

# set up blueprint
groups_blueprint = Blueprint('groups_blueprint', __name__)


def update_members(form, group):
    """Add the group to the reverse document (MembersOf)"""

    doc = MemberOf.objects(user = g.user)
    if doc:
        doc.update_one(push__groups = g.user)
    else:
        MemberOf.objects.create(
            user = g.user,
            groups = [group]
        )
    return group


def create_group(form):
    """Create a group and do the necessary book keeping"""

    group = Group.objects.create(
        name = form.name.data,
        slug = form.slug.data,
        currency = form.currency.data,
        admins = [g.user],
        members = [g.user],
    )
    return update_members(form, group)
    
def init(application):

    @groups_blueprint.route('/create', methods=['GET', 'POST'])
    def create():
        if not g.user:
            abort(401)
        form = GroupForm(request.form)
        if form.validate_on_submit():
            group = create_group(form)
            flash("Created group successfully")
            return redirect(url_for("groups_blueprint.show", id=group.id))
        return render_template("groups/create.html", form=form)


    @groups_blueprint.route('/list')
    def list():
        if not g.user:
            abort(401)
        m = MemberOf.objects.get(user=g.user)
        return render_template("groups/list.html", user=m.user, groups=m.groups)


    @groups_blueprint.route('/show/<id>')
    def show(id):
        """Show details about this group"""
        if not g.user:
            abort(401)
        group = Group.objects.get(id=id)
        return render_template("groups/show.html", group=group)
