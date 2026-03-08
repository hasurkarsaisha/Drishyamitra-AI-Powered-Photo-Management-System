def test_register(client):
    response = client.post('/auth/register', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert 'access_token' in response.json

def test_register_duplicate_username(client):
    client.post('/auth/register', json={
        'username': 'duplicate',
        'email': 'user1@example.com',
        'password': 'password123'
    })
    
    response = client.post('/auth/register', json={
        'username': 'duplicate',
        'email': 'user2@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert 'already exists' in response.json['error']

def test_login(client):
    client.post('/auth/register', json={
        'username': 'loginuser',
        'email': 'login@example.com',
        'password': 'password123'
    })
    
    response = client.post('/auth/login', json={
        'username': 'loginuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_invalid_credentials(client):
    response = client.post('/auth/login', json={
        'username': 'nonexistent',
        'password': 'wrongpass'
    })
    assert response.status_code == 401

def test_get_current_user(client, auth_headers):
    response = client.get('/auth/me', headers=auth_headers)
    assert response.status_code == 200
    assert 'username' in response.json
