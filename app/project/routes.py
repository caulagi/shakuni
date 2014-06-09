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
    def page_not_found(e):
        return render_template('401.html'), 401

    @application.route("/")
    def index():
        if g.user:
            default = "http://www.example.com/default.jpg"
            size = 40
            gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(g.user.email.lower()).hexdigest() + "?"
            gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
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

    api = Api(application)
    return api
