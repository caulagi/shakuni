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

from dateutil.relativedelta import relativedelta

from app.groups.models import Group, MemberOf
from app.groups.forms import GroupForm, JoinGroupForm
from app.bets.models import GroupMatch
from app.matches.models import Match

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

def create_bets(group):
    """New group was created.  Associate the new group with
    each match"""
    for match in Match.objects.all():
        GroupMatch.objects.get_or_create(
            group = group,
            match = match,
            cutoff = match.start_time -relativedelta(hours=2),
        )
    
def init(application):

    @groups_blueprint.route('/create', methods=['GET', 'POST'])
    def create():
        if not g.user:
            abort(401)
        form = GroupForm(request.form)
        if form.validate_on_submit():
            group = create_group(form)
            create_bets(group)
            flash("Created group successfully")
            return redirect(url_for("groups_blueprint.show", id=group.id))
        return render_template("groups/create.html", form=form)


    @groups_blueprint.route('/list')
    def list():
        if not g.user:
            abort(401)
        try:
            m = MemberOf.objects.get(user=g.user)
            groups = m.groups
        except MemberOf.DoesNotExist:
            groups = None
        return render_template("groups/list.html", user=g.user, groups=groups)


    @groups_blueprint.route('/show/<id>')
    def show(id):
        """Show details about this group"""
        if not g.user:
            abort(401)
        group = Group.objects.get(id=id)
        group_matches = GroupMatch.objects(group=group)
        is_admin = g.user in group.admins
        return render_template("groups/show.html", group=group, user=g.user,
            group_matches=group_matches, is_admin=is_admin)


    @groups_blueprint.route('/join/<id>', methods=['GET', 'POST'])
    def join(id):
        """Show details about this group"""
        if not g.user:
            abort(401)
        if Group.objects(members__in=[g.user]):
            abort(403, "You are already a member of this group")
        group = Group.objects.get(id=id)
        form = JoinGroupForm(request.form)
        if form.validate_on_submit():
            Group.objects(id=id).update_one(push__members=g.user)
            flash("You have joined the group successfully")
            return redirect(url_for("groups_blueprint.show", id=group.id))
        return render_template("groups/join.html", form=form, group=group)
