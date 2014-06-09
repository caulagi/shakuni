"""
users.models

Schema for users we will store
"""
from mongoengine import *
    
class User(Document):
    """A User object"""
    
    name  = StringField(max_length=128, required=True)
    email = StringField(max_length=128, required=True)
    openid = StringField(max_length=128, required=True)

    meta = {
        'indexes': ['email']
    }

    def __str__(self):
        return self.name
