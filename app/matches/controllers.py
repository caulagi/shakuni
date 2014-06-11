# -*- coding: utf-8 -*-
"""
    Manage the team and match pages

    :copyright: (c) 2014 by Pradip P Caulagi.
    :license: MIT, see LICENSE for more details.
"""

import logging

from flask import render_template, g, abort, url_for, redirect, \
    request, flash
from flask import Blueprint

from app.matches.models import Player, Team

# setup logger
logger = logging.getLogger('shakuni-matches')

# set up blueprint
matches_blueprint = Blueprint('matches_blueprint', __name__)


def init(application):

    @matches_blueprint.route('/team/<id>')
    def team(id):
        """Show details about this team"""
        try:
            team = Team.objects.get(id=id)
        except Team.DoesNotExist:
            abort(404)
        return render_template("matches/team.html", team=team)

    @matches_blueprint.route('/player/<id>')
    def player(id):
        """Show details about this player"""
        try:
            player = Player.objects.get(id=id)
        except Team.DoesNotExist:
            abort(404)
        return render_template("matches/player.html", player=player)
