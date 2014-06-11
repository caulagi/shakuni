"""
Load the team and match data that is already available
"""
import csv
import os

from itertools import ifilter
from dateutil.relativedelta import *
from dateutil.parser import parse
from app.project.instance import application
from app.matches.models import Player, Team, Match

def save_match(row):
    start_time = parse(row[1])
    return Match.objects.get_or_create(
        match_number = row[0],
        team1 = Team.objects.get(country = row[2]),
        team2 = Team.objects.get(country = row[3]),
        start_time = start_time,
        venue = row[4],
    )

def save_team(name):
    p = name.rstrip('.txt').split('-')
    name = ' '.join(map(str.capitalize, p[1:]))
    return Team.objects.get_or_create(
        country = name,
        code = p[0],
    )
    
def save_player(row):
    return Player.objects.get_or_create(
        jersey = row[0],
        position = row[1],
        name = row[2],
        club = row[3],
    )

def load_teams():
    for name in os.listdir(os.path.join('data', 'squads')):
        team, created = save_team(name)
        players = []
        with open(os.path.join('data', 'squads', name), 'r') as f:
            print "Loading %s" % f
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                player, created = save_player(row)
                players.append(player)
            team.players = players
            team.save()

def load_matches():
    print "Loading matches"
    with open("data/schedule.csv", "r") as f:
        reader = csv.reader(ifilter(lambda row: not row.startswith('#'), f), delimiter='|')
        for row in reader:
            if not row:
                continue
            save_match(row)
            

def run():
    load_teams()
    load_matches()

if __name__ == "__main__":
    run()
