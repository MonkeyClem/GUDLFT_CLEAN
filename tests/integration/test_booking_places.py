from server import app

def test_booking_invalid_competition_should_redirect():
    with app.test_client() as client:
        response = client.post('/purchase_places', data={
            'club': 'Simply Lift',
            'competition': 'Non Existing Competition',
            'places': '1'
        }, follow_redirects=True)
        assert b"ERROR: Competition not found." in response.data

def test_booking_zero_places_should_fail():
    with app.test_client() as client:
        response = client.post('/purchase_places', data={
            'club': 'Simply Lift',
            'competition': 'Test Weight',
            'places': '0'
        }, follow_redirects=True)
        print(response.data.decode())
        assert b"You must book at least 1 place" in response.data


def test_booking_more_than_available_should_fail():
    with app.test_client() as client:
        response = client.post('/purchase_places', data={
            'club': 'Simply Lift',
            'competition': 'Test Weight',
            'places': '12'
        }, follow_redirects=True)
        assert b"Not enough places available" in response.data

def test_booking_more_than_12_places_should_fail():
    with app.test_client() as client:
        response = client.post('/purchase_places', data={
            'club': 'Simply Lift',
            'competition': 'Test Weight',
            'places': '13'
        }, follow_redirects=True)
        assert b"You cannot book more than 12 places per competition." in response.data


def test_booking_insufficient_points_should_fail():
    with app.test_client() as client:
        response = client.post('/purchase_places', data={
            'club': 'She Lifts',
            'competition': 'Test Weight',
            'places': '10'
        }, follow_redirects=True)
        print(response.data.decode())  # <- Important, pour lire proprement le contenu
        assert b"You do not have enough points to book these places." in response.data

def test_booking_past_competition_should_fail():
    with app.test_client() as client:
        response = client.post('/purchase_places', data={
            'club': 'Simply Lift',
            'competition': 'Fall Classic',  
            'places': '1'
        }, follow_redirects=True)
        assert b"This competition is not available anymore" in response.data

def test_book_invalid_club_or_competition_should_flash():
    with app.test_client() as client:
        response = client.get('/book/InvalidComp/InvalidClub', follow_redirects=True)
        assert b"Something went wrong-please try again" in response.data

def test_successful_booking_should_succeed():
    with app.test_client() as client:
        response = client.post('/purchase_places', data={
            'club': 'Simply Lift',
            'competition': 'Test Weight',
            'places': '1'
        }, follow_redirects=True)
        assert b"Great-booking complete!" in response.data
        
def test_booking_with_invalid_competition_and_club_should_fail():
    with app.test_client() as client:
        response = client.get('/book/InvalidCompetition/InvalidClub', follow_redirects=True)
        assert b"Something went wrong-please try again" in response.data

def test_booking_invalid_club_or_competition_should_flash_error():
    with app.test_client() as client:
        response = client.get('/book/InvalidCompetition/InvalidClub', follow_redirects=True)
        assert response.status_code == 200
        assert b"Something went wrong-please try again" in response.data

def test_successful_booking_should_flash_success_message():
    with app.test_client() as client:
        response = client.post('/purchase_places', data={
            'club': 'Simply Lift',
            'competition': 'Test Weight',
            'places': '1'
        }, follow_redirects=True)
        assert b"Great-booking complete!" in response.data




##Séparer       
def test_display_points_route():
    with app.test_client() as client:
        response = client.get('/clubs/points')
        assert response.status_code == 200
        assert b"Clubs and Points" in response.data

