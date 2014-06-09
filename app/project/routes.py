"""
project.routes

Bind the api's to the endpoints
"""
from flask.ext.restful import Api
from flask import render_template
#from users.api import *
    
def routes_init(application):
    
    @application.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    import app.users.controllers as users_controller
    users_controller.init(application)
    application.register_blueprint(users_controller.users_blueprint, url_prefix="/users")

    api = Api(application)
    return api
