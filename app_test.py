# test_app.py
import pytest
from app import app, todos

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    todos.clear() 

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Todo List' in response.data

def test_add_todo(client):
    response = client.post('/add', data={'todo': 'Test todo'})
    assert response.status_code == 302
    assert len(todos) == 1
    assert todos[0]['task'] == 'Test todo'

def test_edit_todo(client):
    client.post('/add', data={'todo': 'Original todo'})
    response = client.post('/edit/0', data={'todo': 'Updated todo'})
    assert response.status_code == 302
    assert todos[0]['task'] == 'Updated todo'

def test_check_todo(client):
    client.post('/add', data={'todo': 'Test todo'})
    response = client.get('/check/0')
    assert response.status_code == 302
    assert todos[0]['done'] 

def test_delete_todo(client):
    client.post('/add', data={'todo': 'Test todo'})
    response = client.get('/delete/0')
    assert response.status_code == 302
    assert len(todos) == 0
