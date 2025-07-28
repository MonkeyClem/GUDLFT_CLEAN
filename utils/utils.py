import json 

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
