import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required.'),
        ('cj', '', b'Your username is too short.'),
        ('test', '', b'Your password is required.'),
        ('test', 'test', b'Your password must have at least 8 characters, an upper case letter, a lower case letter and a digit.'),
        ('fmercury', 'Test#6^0', b'Your username is already taken - please supply another'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to CS235Flix!' in response.data


def test_login_required_to_comment(client):
    response = client.post('/comment')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_comment(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the comment page.
    response = client.get('/comment?article=2')

    response = client.post(
        '/comment',
        data={'comment': 'Who needs quarantine?', 'article_id': 2, 'rating': 1}
    )
    assert response.headers['Location'] == 'http://localhost/movies/2'


@pytest.mark.parametrize(('comment', 'messages'), (
        ('Who thinks Trump is a fuckwit?', (b'Your review must not contain profanity')),
        ('Hey', (b'Your review is too short')),
        ('ass', (b'Your review is too short', b'Your review must not contain profanity')),
))
def test_comment_with_invalid_input(client, auth, comment, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an article.
    response = client.post(
        '/comment',
        data={'comment': comment, 'article_id': 2}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_articles_without_tag(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_tag')
    assert response.status_code == 200

    # Check that without providing a date query parameter the page includes no movies.
    assert b'No results' in response.data

def test_articles_with_comment(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies/1')
    assert response.status_code == 200

    # Check that all comments for specified movies are included on the page.
    assert b'Yeah Freddie, bad news' in response.data


def test_articles_with_tag(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_tag?tag=Action')
    assert response.status_code == 200

    # Check that all movies tagged with 'Action' are included on the page.
    assert b'Guardians of the Galaxy' in response.data
    assert b'Rogue One' in response.data
    assert b'Colossal' in response.data

def test_articles_with_invalid_tag(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_tag?tag=Macarena')
    assert response.status_code == 200

    # Check that no movies are tagged with 'Macarena'.
    assert b'No results' in response.data
