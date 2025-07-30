import json 
from datetime import datetime
def loadClubs():
    with open('clubs.json') as c:
         list_of_clubs = json.load(c)['clubs']
         return list_of_clubs


def loadCompetitions():
    with open('competitions.json') as comps:
         list_of_competitions = json.load(comps)['competitions']
         return list_of_competitions

competitions = loadCompetitions()
clubs = loadClubs()

def find_club_by_email(email, clubs):
    return next((club for club in clubs if club["email"] == email), None)

def exceeds_max_places_per_booking(places_requested, max_places=12):
    return places_requested > max_places



def exceed_club_points(required_places ,club_available_points): 
    return required_places > club_available_points


def find_club_by_name(club_name : str):
    return next((club for club in clubs if club["name"] == club_name))


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
