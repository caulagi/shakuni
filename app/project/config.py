"""
project.conf

Configuration module holding all the options
"""

DEBUG = False

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

MONGO_DBNAME = os.environ.get("MONGOHQ_URL") or "mongodb://localhost:27017/shakuni"

THREADS_PER_PAGE = 2
CSRF_ENABLED = True
CSRF_SESSION_KEY = "secret"
SECRET_KEY = "secret"

STATIC_FOLDER = 'app/static'
TEMPLATES_FOLDER = 'app/templates'

FACEBOOK_APP_ID = os.environ.get("FACEBOOK_APP_ID") or '672966529447612'
FACEBOOK_APP_SECRET = os.environ.get("FACEBOOK_APP_SECRET") or '8e4a083bb66fc0e81d18e3acbd3b52aa'
