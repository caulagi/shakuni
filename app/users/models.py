"""
users.models

Schema for users we will store
"""
from mongoengine import *
    
class User(Document):
    """A User object"""
    
    name  = StringField(max_length=128, required=True)
    email = StringField(max_length=128, required=True)
    first_name = StringField(max_length=128, required=True)
    last_name = StringField(max_length=128, required=True)
    facebook_id = StringField(max_length=128, required=True)
    gender = StringField(max_length=12)
    provider = StringField(max_length=12)
    access_token = StringField(max_length=255)

    meta = {
        'indexes': ['email']
    }

    def __str__(self):
        return self.name
