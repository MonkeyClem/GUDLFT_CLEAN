from utils.utils import find_club_by_email, loadClubs

def test_find_club_by_email_valid():
    clubs = loadClubs()
    result = find_club_by_email("john@simplylift.co", clubs)
    assert result is not None
    assert result['name'] == 'Simply Lift'

def test_find_club_by_email_invalid():
    clubs = loadClubs()
    result = find_club_by_email("notfound@email.com", clubs)
    assert result is None
