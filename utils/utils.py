import json 
from datetime import datetime
def load_clubs():
    with open('clubs.json') as c:
         list_of_clubs = json.load(c)['clubs']
         return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
         list_of_competitions = json.load(comps)['competitions']
         return list_of_competitions

competitions = load_competitions()
clubs = load_clubs()

def find_competition_by_name(name):
    for c in competitions:
        if c["name"] == name:
            return c
    return None




def is_competition_in_past(competition_date): 
    return competition_date < datetime.now()

