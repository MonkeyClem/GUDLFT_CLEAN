import json 

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

def exceed_club_points(required_places ,club_available_points): 
    return required_places > club_available_points


def find_club_by_name(club_name : str):
    return next((club for club in clubs if club["name"] == club_name))
