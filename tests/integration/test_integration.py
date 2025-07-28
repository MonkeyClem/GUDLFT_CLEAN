from server import app

def test_booking_zero_places_should_fail():
    with app.test_client() as client:
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Fall Classic',
            'places': '0'
        }, follow_redirects=True)
        assert b"You must book at least 1 place" in response.data

def test_booking_negative_places_should_fail():
    with app.test_client() as client:
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Fall Classic',
            'places': '-3'
        }, follow_redirects=True)
        assert b"You must book at least 1 place" in response.data

def test_booking_more_than_available_should_fail():
    with app.test_client() as client:
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Fall Classic',
            'places': '999'
        }, follow_redirects=True)
        assert b"Not enough places available" in response.data