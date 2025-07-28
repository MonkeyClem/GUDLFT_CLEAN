import json 

def loadClubs():
    with open('clubs.json') as c:
         list_of_clubs = json.load(c)['clubs']
         return list_of_clubs


def loadCompetitions():
    with open('competitions.json') as comps:
         list_of_competitions = json.load(comps)['competitions']
         return list_of_competitions


def exceeds_max_places_per_booking(places_requested, max_places=12):
    return places_requested > max_places
