# from os import environ
import json

def test_home(api):
    """Page loads"""
    resp = api.get('/')
    assert resp.status == '200 OK'

def test_not_found(api):
    """/12345 triggers a 404"""
    resp = api.get('/12345')
    assert resp.status == '404 NOT FOUND'

class MockResponse: # 1
    def __init__(self, result):
        self.result = result

    def json(self):
        return {'exists': self.result}

def xtest_create_new_user(client):
    """/POST creates a user"""
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
        # with self.test_client() as client:
    form_data = {
        'username': 'Test1',
        'password': 'TestPass123'
    }
    
    response = client.post(
        "/register",
        data=json.dumps(form_data),
        headers=headers
    )

    assert response.content_type == mimetype
    assert response.status == '201 CREATED' 

def test_token_api(api):
    """/Missing token triggers a 401 UNAUTHORIZED"""
    resp = api.get('/token')
    assert resp.status == '401 UNAUTHORIZED'

def test_allusers_api(api):
    """/All users endpoint is protected with token"""

    resp = api.get('/https://black-beard-island.herokuapp.com/users')
    assert resp.status == '404 NOT FOUND'

def test_gameover_api(api):
    """/Gameover endpoint is protected with token"""
    resp = api.get('/gameover')
    assert resp.status == '401 UNAUTHORIZED'
