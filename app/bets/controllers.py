# -*- coding: utf-8 -*-
"""
    Manage the bet and related functions

    :copyright: (c) 2014 by Pradip P Caulagi.
    :license: MIT, see LICENSE for more details.
"""

import logging
import datetime

from flask import render_template, g, abort, url_for, redirect, \
    request, flash
from flask import Blueprint

from app.bets.models import GroupMatch, Bet
from app.bets.forms import BetForm

# setup logger
logger = logging.getLogger('shakuni-bets')

# set up blueprint
bets_blueprint = Blueprint('bets_blueprint', __name__)


def create_bet(form, group_match):
    try:
        bet = Bet.objects.get(
            group_match = group_match, user = g.user,
        )
        bet.amount = form.amount.data
        bet.outcome = form.outcome.data
        return bet.save()
    except Bet.DoesNotExist:
        return Bet.objects.create(
            group_match = group_match,
            user = g.user,
            amount = form.amount.data,
            outcome = form.outcome.data,
            currency = group_match.group.currency
        )

def init(application):

    @bets_blueprint.route('/<id>/list')
    def list(id):
        """List all the bets for this match and group"""
        if not g.user:
            abort(401)
        try:
            group_match = GroupMatch.objects.get(id=id)
        except GroupMatch.DoesNotExist:
            return abort(403, "Not a valid match")
        bets = Bet.objects(group_match = group_match)
        return render_template("bets/list.html", bets=bets)

    @bets_blueprint.route('/<id>/create', methods=['GET', 'POST'])
    def create(id):
        """Place a bet"""
        if not g.user:
            abort(401)
        try:
            group_match = GroupMatch.objects.get(id=id)
        except GroupMatch.DoesNotExist:
            abort(403, "Not a valid match")
        if datetime.datetime.now() > group_match.cutoff:
            abort(403, "We no longer accept bets for this match")
            
        form = BetForm(request.form)
        bets = Bet.objects(group_match = group_match)
        if form.validate_on_submit():
            create_bet(form, group_match)
            flash("You have joined the group successfully")
            return redirect(url_for("bets_blueprint.list", id=group_match.id))
        return render_template("bets/create.html", group_match=group_match,
            form=form, bets=bets)
