from utils.utils import find_club_by_email, loadClubs, is_competition_in_past
from server import app
from datetime import datetime, timedelta
import pytest_cov
print("pytest-cov is installed and importable.")

def test_find_club_by_email_valid():
    clubs = loadClubs()
    result = find_club_by_email("john@simplylift.co", clubs)
    assert result is not None
    assert result['name'] == 'Simply Lift'

def test_find_club_by_email_invalid():
    clubs = loadClubs()
    result = find_club_by_email("notfound@email.com", clubs)
    assert result is None

def test_is_competition_in_past_true():
    past_date = datetime.now() - timedelta(days=1)
    assert is_competition_in_past(past_date) == True

def test_is_competition_in_past_false():
    future_date = datetime.now() + timedelta(days=1)
    assert is_competition_in_past(future_date) == False

def test_logout_redirects_to_index():
    with app.test_client() as client:
        response = client.get('/logout', follow_redirects=True)
        assert b"Welcome" in response.data or response.status_code == 200

def test_booking_route_with_invalid_competition():
    with app.test_client() as client:
        response = client.get('/book/InvalidCompetition/Simply Lift', follow_redirects=True)
        assert b"Something went wrong" in response.data

def test_booking_route_with_invalid_club():
    with app.test_client() as client:
        response = client.get('/book/Fall Classic/Fake Club', follow_redirects=True)
        assert b"Something went wrong" in response.data
