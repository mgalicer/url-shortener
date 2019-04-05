import pytest, json
from app import app

base_url = 'http://127.0.0.1:5000/'

# app should create a short link for arbitrary URL's
def test_create_link():        
    response = app.test_client().post(
        '/',
        data=json.dumps({'long_link': 'https://google.com/',}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))
    
    assert response.status_code == 200
    assert 'short_link' in data

# app should return a custom short link when specified 
def test_custom_link():
    short_link = 'nyt'
    response = app.test_client().post('/',
        data=json.dumps({
            'long_link': 'https://www.nytimes.com/',
            'custom_short_link': short_link
        }),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))
    assert f'{base_url}{short_link}' == data['short_link']

# app should redirect when given a short url that exists in db
def test_redirect():
    response = app.test_client().get('/nyt')
    assert response.status_code == 302

# app should provide stats for a given short link
def test_stats():
    response = app.test_client().get('/stats/nyt')
    assert response.status_code == 200
    
    data = json.loads(response.get_data(as_text=True))
    assert 'created at' in data
    assert 'total visits' in data
    assert 'histogram' in data
