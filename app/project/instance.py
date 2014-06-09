"""
project.instance

Create and expose the Flask application
"""
from flask import Flask, render_template

def create_app():
    application = Flask('app')

    from app.project import config
    application.config.from_object(config)

    from app.project.database import db_init
    application.db = db_init()

    from app.project.routes import routes_init
    routes_init(application)

    return application

application = create_app()
