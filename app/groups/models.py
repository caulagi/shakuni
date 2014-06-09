"""
groups.models

Models relating to handling a group of users
"""

from mongoengine import *
from app.users.models import User
    
class Group(Document):
    """A groups consists of admins and members"""
    
    name = StringField(max_length=128, required=True)
    slug = StringField(max_length=128)
    currency = StringField(max_length=3, required=True)
    admins = ListField(ReferenceField(User))
    members = ListField(ReferenceField(User))

    def __str__(self):
        return self.name


class MemberOf(Document):
    """A reverse lookup: Get all groups for the user"""

    user = ReferenceField(User)
    groups = ListField(ReferenceField(Group))

    def __str(self):
        return ','.join(g.name for g in self.groups)
