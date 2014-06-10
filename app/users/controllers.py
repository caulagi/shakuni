# -*- coding: utf-8 -*-
"""
    Integrate with Google  using openid

    :copyright: (c) 2014 by Pradip Caulagi.
    :license: MIT, see LICENSE for more details.
"""
import logging

from flask import Flask, render_template, request, g, session, flash, \
     redirect, url_for, abort
from flask import Blueprint
from flask_oauth import OAuth

from app.project import config
from app.users.models import User

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=config.FACEBOOK_APP_ID,
    consumer_secret=config.FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

# setup logger
logger = logging.getLogger('shakuni-users')

# set up blueprint
users_blueprint = Blueprint('users_blueprint', __name__)

def get_or_create_user(data):
    """Store this user"""

    try:
        u = User.objects.get(email = data.get('email'))
        u.access_token = session['oauth_token'][0]
        return u.save()
    except User.DoesNotExist:
        return User.objects.create(
            facebook_id = data.get('id'),
            name = data.get('name'),
            first_name = data.get('first_name'),
            last_name = data.get('first_name'),
            email = data.get('email'),
            gender = data.get('gender'),
            provider = "facebook",
            access_token = session['oauth_token'][0],
        )

def init(application):

    @application.before_request
    def before_request():
        g.user = None
        if 'oauth_token' in session:
            g.user = User.objects(access_token = session['oauth_token'][0]).first()

    @users_blueprint.route('/login')
    def login():
        return render_template("users/login.html")

    @users_blueprint.route('/fb-login')
    def fb_login():
        return facebook.authorize(callback=url_for('users_blueprint.facebook_authorized',
            next=request.args.get('next') or request.referrer or None,
            _external=True))


    @users_blueprint.route('/fb-login/authorized')
    @facebook.authorized_handler
    def facebook_authorized(resp):
        if resp is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )
        session['oauth_token'] = (resp['access_token'], '')
        me = facebook.get('/me')
        print me.data
        g.user = get_or_create_user(me.data)
        return redirect(url_for("users_blueprint.me"))

    @users_blueprint.route('/edit-profile', methods=['GET', 'POST'])
    def edit_profile():
        pass

    @facebook.tokengetter
    def get_facebook_oauth_token():
        return session.get('oauth_token')

    @users_blueprint.route('/logout')
    def logout():
        session.pop('oauth_token', None)
        flash(u'You have been signed out')
        return redirect(url_for("users_blueprint.login"))

    @users_blueprint.route('/me')
    def me():
        if g.user is None:
            abort(401)
        return render_template('users/me.html', user=g.user)
