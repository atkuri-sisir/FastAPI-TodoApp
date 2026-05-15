
from routers.todos import get_db, get_current_user
from .utils import *
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all(test_todo):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False,
                                'title': 'Learn to code!',
                                'description': 'Need to learn everyday',
                                'id': 1,
                                'priority': 5,
                                'owner_id': 1}]


def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == 200
    assert response.json() == {'complete': False,
                                'title': 'Learn to code!',
                                'description': 'Need to learn everyday',
                                'id': 1,
                                'priority': 5,
                                'owner_id': 1}


def test_read_one_authenticated_not_found():
    response = client.get("/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


def test_create_todo(test_todo):
    request_data = {
        'title': 'New test todo',
        'description': 'New test todo description',
        'priority': 5,
        'complete': False
    }

    response = client.post("/todo/", json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.title == 'New test todo').first()
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')


def test_update_todo(test_todo):
    request_data = {
        'title': 'Updated todo',
        'description': 'Updated todo description',
        'priority': 5,
        'complete': False
    }

    response = client.put("/todo/1", json = request_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'Updated todo'


def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'Updated todo',
        'description': 'Updated todo description',
        'priority': 5,
        'complete': False
    }

    response = client.put("/todo/999", json = request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


def test_delete_todo(test_todo):
    response = client.delete('/todo/1')
    assert response.status_code == 204
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo(test_todo):
    response = client.delete('/todo/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}