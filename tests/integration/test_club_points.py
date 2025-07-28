from server import app

def test_clubs_points_route_status_code():
    with app.test_client() as client:
        response = client.get('/clubs/points')
        assert response.status_code == 200

def test_clubs_points_content():
    with app.test_client() as client:
        response = client.get('/clubs/points')
        assert b"Clubs and Points" in response.data
        assert b"Simply Lift" in response.data
        assert b"Iron Temple" in response.data
