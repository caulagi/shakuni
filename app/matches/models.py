"""
matches.models

Models relating to the matches
"""
from mongoengine import *
    
class Player(Document):
    """Name and club for a player"""

    name = StringField(max_length=64, required=True)
    jersey = IntField()
    club = StringField(max_length=32)
    position = StringField(max_length=2)

    def __str__(self):
        return self.name

class Team(Document):
    """Hold the players in a team"""

    country = StringField(max_length=32, required=True)
    code = StringField(max_length=2, required=True)
    players = ListField(ReferenceField(Player))

    def __str__(self):
        return self.country

class Match(Document):
    """Details about the actual match"""

    team1 = ReferenceField(Team)
    team2 = ReferenceField(Team)
    start_time = DateTimeField(required=True)
    venue = StringField(max_length=64)
    match_number = IntField()
    
    def __str__(self):
        return '%s vs %s' % (self.team1, self.team2)
