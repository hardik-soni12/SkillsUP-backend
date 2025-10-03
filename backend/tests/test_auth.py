import json

def test_user_registration(client):
    # data for our test
    new_user_data = {
        "username":"still_riooo",
        "email":"still.riooo@gmail.com",
        "password":"password",
        "confirm_password":"password",
        "bio":"Testing the PyTest."
    }

    response = client.post(
        '/auth/register',
        data=json.dumps(new_user_data),
        content_type='application/json'
    )

    assert response.status_code == 201
    assert response.json['user']['username'] == 'still_riooo'

def test_user_registration_fails_if_username_taken(client):
    existing_user_data={
        'username':'hardik9156',
        'email':'hardik9156@gmail.com',
        'password':'password',
        'confirm_password':'password',
        'bio':''
    }

    client.post(
        '/auth/register',
        data=json.dumps(existing_user_data),
        content_type='application/json'
    )

    new_user_data_with_duplicate_username ={
        'username':'hardik9156',
        'email':'hardsoni9156@gmail.com',
        'password':'password',
        'confirm_password':'password',
        'bio':''
    }

    response = client.post(
        '/auth/register',
        data=json.dumps(new_user_data_with_duplicate_username),
        content_type='application/json'
    )

    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error']=='username already taken'
    

def test_login_success(client):
    user_to_login = {
        'username':'riooo',
        'email':'riooo@gmail.com',
        'password':'password',
        'confirm_password':'password',
        'bio':''
    }

    client.post(
        '/auth/register',
        data=json.dumps(user_to_login),
        content_type='application/json'
    )

    login_credentials={
        'email':'riooo@gmail.com',
        'password':'password'
    }

    response = client.post(
        '/auth/login',
        data=json.dumps(login_credentials),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.json['user']['username']=='riooo'
    assert "access_token" in response.json


def test_login_fails_with_wrong_password(client):
    user_to_test={
        'username':'hardik23',
        'email':'hardik23@gmail.com',
        'password':'password',
        'confirm_password':'password',
        'bio':''
    }

    client.post('/auth/register', data=json.dumps(user_to_test))

    wrong_credentials={
        'email':'hardik23@gmail.com',
        'password':'password123'
    }

    response=client.post(
        '/auth/login',
        data=json.dumps(wrong_credentials),
        content_type='application/json'
    )

    assert response.status_code == 401
    assert 'error' in response.json
    assert response.json['error'] == 'Invalid credentials'