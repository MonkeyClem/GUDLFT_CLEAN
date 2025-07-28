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


def is_points_balance_valid(club: dict, places_required: int) -> bool:
    club_points = int(club['points'])
    if club_points >= places_required:
        club['points'] = str(club_points - places_required) 
        return True
    return False

def validate_places_request(places_required: int, available_places: int) -> str:
    if places_required <= 0:
        return "ERROR: You must book at least 1 place."
    if places_required > available_places:
        return "ERROR: Not enough places available in this competition."
    return ""
