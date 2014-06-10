"""
project.conf

Configuration module holding all the options
"""

DEBUG = True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

MONGO_DBNAME = os.environ.get("MONGOHQ_URL") or "mongodb://localhost:27017/shakuni"

THREADS_PER_PAGE = 2
CSRF_ENABLED = True
CSRF_SESSION_KEY = "secret"
SECRET_KEY = "secret"

STATIC_FOLDER = 'app/static'
TEMPLATES_FOLDER = 'app/templates'
