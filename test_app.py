def test_home(api):
    """Page loads"""
    resp = api.get('/')
    assert resp.status == '200 OK'

def xtest_no_url(api):
    """/12345 triggers a 404"""
    resp = api.get('/12345')
    assert resp.status == '404 NOT FOUND'

def xtest_takes_url(api):
    """/POST creates a user"""
    form_data = {
        'username': 'Test1',
        'password': 'TestPass123'
    }
    resp = api.post('/register', data=form_data)
    assert resp.status == '201 CREATED'
    # assert b'localhost' in resp.data