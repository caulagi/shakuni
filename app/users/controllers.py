# -*- coding: utf-8 -*-
"""
    Integrate with Google  using openid

    :copyright: (c) 2014 by Pradip Caulagi.
    :license: MIT, see LICENSE for more details.
"""
import logging

from flask import Flask, render_template, request, g, session, flash, \
     redirect, url_for, abort
from flask.ext.openid import OpenID
from flask import Blueprint

from openid.extensions import pape

from app.users.models import User

# Declare a variable that we will initialize later
oid = None

# setup logger
logger = logging.getLogger('shakuni-users')

# set up blueprint
users_blueprint = Blueprint('users_blueprint', __name__)

def init(application):
    # setup flask-openid
    oid = OpenID(application, safe_roots=[], extension_responses=[pape.Response])

    @application.before_request
    def before_request():
        g.user = None
        if 'openid' in session:
            g.user = User.objects.filter(openid=session['openid']).first()

    @application.after_request
    def after_request(response):
        #db_session.remove()
        return response

    @users_blueprint.route('/login', methods=['GET', 'POST'])
    @oid.loginhandler
    def login():
        """Does the login via OpenID.  Has to call into `oid.try_login`
        to start the OpenID machinery.
        """
        # if we are already logged in, go back to were we came from
        if g.user is not None:
            return redirect(oid.get_next_url())
        if request.method == 'POST':
            openid = request.form.get('openid')
            if openid:
                pape_req = pape.Request([])
                return oid.try_login(openid, ask_for=['email', 'nickname'],
                                             ask_for_optional=['fullname'],
                                             extensions=[pape_req])
        return render_template('users/login.html', next=oid.get_next_url(),
                               error=oid.fetch_error())


    @oid.after_login
    def create_or_login(resp):
        """This is called when login with OpenID succeeded and it's not
        necessary to figure out if this is the users's first login or not.
        This function has to redirect otherwise the user will be presented
        with a terrible URL which we certainly don't want.
        """
        session['openid'] = resp.identity_url
        if 'pape' in resp.extensions:
            pape_resp = resp.extensions['pape']
            session['auth_time'] = pape_resp.auth_time
        user = User.objects.filter(openid=resp.identity_url).first()
        if user is not None:
            flash(u'Successfully signed in')
            g.user = user
            return redirect(url_for('users_blueprint.me'))
        return redirect(url_for('users_blueprint.create_profile', next=oid.get_next_url(),
                                name=resp.fullname or resp.nickname,
                                email=resp.email))

    @users_blueprint.route('/create-profile', methods=['GET', 'POST'])
    def create_profile():
        """If this is the user's first login, the create_or_login function
        will redirect here so that the user can set up his profile.
        """
        if g.user is not None or 'openid' not in session:
            return redirect(url_for('index'))
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            if not name:
                flash(u'Error: you have to provide a name')
            elif '@' not in email:
                flash(u'Error: you have to enter a valid email address')
            else:
                flash(u'Profile successfully created')
                User.objects.create(name=name, email=email, openid=session['openid'])
                return redirect(oid.get_next_url())
        return render_template('users/create_profile.html', next_url=oid.get_next_url())

    @users_blueprint.route('/profile', methods=['GET', 'POST'])
    def edit_profile():
        """Updates a profile"""
        if g.user is None:
            abort(401)
        form = dict(name=g.user.name, email=g.user.email)
        if request.method == 'POST':
            if 'delete' in request.form:
                db_session.delete(g.user)
                db_session.commit()
                session['openid'] = None
                flash(u'Profile deleted')
                return redirect(url_for('index'))
            form['name'] = request.form['name']
            form['email'] = request.form['email']
            if not form['name']:
                flash(u'Error: you have to provide a name')
            elif '@' not in form['email']:
                flash(u'Error: you have to enter a valid email address')
            else:
                flash(u'Profile successfully created')
                g.user.name = form['name']
                g.user.email = form['email']
                db_session.commit()
                return redirect(url_for('edit_profile'))
        return render_template('users/edit_profile.html', form=form)

    @users_blueprint.route('/logout')
    def logout():
        session.pop('openid', None)
        flash(u'You have been signed out')
        return redirect(url_for("users_blueprint.login"))

    @users_blueprint.route('/me')
    def me():
        if g.user is None:
            abort(401)
        return render_template('users/me.html', user=g.user)
