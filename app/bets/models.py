"""
bets.models

Models relating to bets placed
"""
import datetime
from mongoengine import *
from decimal import Decimal

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

    def time_remaining(self):
        return self.cutoff - datetime.datetime.now()

    def amount_bet(self, user):
        """If the user has bet any amount on this match,
        return the amount, or 0"""
        try:
            return Bet.objects.get(group_match = self, user=user).amount
        except Bet.DoesNotExist:
            return Decimal(0)

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
        
    def pot(self):
        bets = Bet.objects(group_match = self.group_match)
        return sum(map(lambda x: x.amount, bets))

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
        return u"%s: %s" % (str(self.user), str(self.team))
