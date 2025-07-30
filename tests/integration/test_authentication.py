from server import app

def test_valid_email():
    with app.test_client() as client:
        response = client.post('/show_summary', data={'email': 'john@simplylift.co'})
        assert response.status_code == 200
        assert b"Welcome" in response.data or b"Points" in response.data  

def test_invalid_email_redirect():
    with app.test_client() as client:
        response = client.post('/show_summary', data={'email': 'invalid@email.com'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"ERROR : Unknown e-mail" in response.data


# def test_logout_route_should_redirect_to_index():
#     with app.test_client() as client:
#         response = client.get('/logout', follow_redirects=True)
#         assert response.status_code == 200
#         assert b"Welcome" in response.data or b"Login" in response.data

def test_logout_redirects_to_index():
    with app.test_client() as client:
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b"Welcome" in response.data or b"GUDLFT" in response.data
