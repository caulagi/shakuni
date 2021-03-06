"""
project.routes

Bind the api's to the endpoints
"""
from flask.ext.restful import Api
from flask import render_template, g
import urllib, hashlib
 
 # Set your variables here
#from users.api import *
    
def routes_init(application):
    
    @application.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @application.errorhandler(401)
    def unauthorized(e):
        return render_template('401.html'), 401

    @application.errorhandler(403)
    def forbidden(e):
        return render_template('403.html', error=e.description), 403

    @application.errorhandler(500)
    def forbidden(e):
        return render_template('500.html'), 500

    @application.route("/")
    def index():
        if g.user:
            size = 120 
            gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(g.user.email.lower()).hexdigest() + "?"
            gravatar_url += urllib.urlencode({'d': 'retro', 's':str(size)})
            g.user.gravatar_url = gravatar_url
        return render_template("index.html", user=g.user)

    @application.route("/about")
    def about():
        return render_template("about.html")

    @application.route("/faq")
    def faq():
        return render_template("faq.html")

    import app.users.controllers as users_controller
    users_controller.init(application)
    application.register_blueprint(users_controller.users_blueprint, url_prefix="/users")

    import app.groups.controllers as groups_controller
    groups_controller.init(application)
    application.register_blueprint(groups_controller.groups_blueprint, url_prefix="/groups")

    import app.matches.controllers as matches_controller
    matches_controller.init(application)
    application.register_blueprint(matches_controller.matches_blueprint, url_prefix="/matches")

    import app.bets.controllers as bets_controller
    bets_controller.init(application)
    application.register_blueprint(bets_controller.bets_blueprint, url_prefix="/bets")

    api = Api(application)
    return api
