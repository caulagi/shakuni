"""
bets.models

Models relating to bets placed
"""
import datetime
from mongoengine import *

from app.groups.models import Group
from app.users.models import User
from app.matches.models import Match
from app.project.config import CURRENCIES

class GroupMatch(Document):
    """Associate each match with the group"""

    group = ReferenceField(Group)
    match = ReferenceField(Match)
    cutoff = DateTimeField()
    created = DateTimeField(default=datetime.datetime.now())
    
    meta = {
        'indexes': ['group', 'match'] 
    }
    
    def __str__(self):
        return "%s: %s" % (self.match, self.group)


class Bet(Document):
    """Bet that a user has placed"""
    
    OUTCOME = (
        (-1, 'Team 2 wins'),
        (0, 'Draw'),
        (1, 'Team 1 wins'),
    )

    group_match = ReferenceField(GroupMatch)
    user = ReferenceField(User)
    amount = DecimalField()
    currency = StringField(max_length=3, choices=CURRENCIES)
    outcome = IntField(choices=OUTCOME)
    created = DateTimeField(default=datetime.datetime.now())

    meta = {
        'indexes': ['user']
    }

    def __str__(self):
        return "%s: %s" % (self.bet, self.user)
        

class WinnerBet(Document):
    """Bet placed at the beginning of the tournament on who
    will win the worldcup"""

    user = ReferenceField(User)
    team = ReferenceField(User)
    amount = DecimalField()
    currency = StringField(max_length=3, choices=CURRENCIES)
    cutoff = DateTimeField()
    created = DateTimeField(default=datetime.datetime.now())

    meta = {
        'indexes': ['user', 'team']
    }

    def __str__(self):
        return "%s -> %s" % (self.user, self.team)
