import pytest
from models.todo import Todo
import tempfile
import os
from werkzeug.test import Client
from app import app
import json


@pytest.fixture
def client():
    db_fd, Todo.DB_PATH = tempfile.mkstemp()
    Todo.init_table()
    os.close(db_fd)
    return Client(app)


@pytest.fixture
def todos_req():
    todo1 = {'id': 1, 'content': '部屋の掃除'}
    todo2 = {'id': 2, 'content': '犬の散歩'}
    todo3 = {'id': 3, 'content': 'ご飯の準備'}
    return [todo1, todo2, todo3]


def test_empty_db(client):
    res = client.get('/todo/')
    assert res.get_json() == []


def test_add_todos(client, todos_req):
    for todo_req in todos_req:
        res = client.post('/todo/', data=json.dumps({"content": todo_req['content']}))
        assert res.get_json() == todo_req['id']

    todos_res = client.get('/todo/').get_json()
    assert todos_req == todos_res

    todo_res = client.get('/todo/1/').get_json()
    assert todos_req[0] == todo_res


def test_put_todo(client, todos_req):
    for todo_req in todos_req:
        res = client.post('/todo/', data=json.dumps({"content": todo_req['content']}))

    todo_new = {'id': 2, 'content': 'aaa'}
    res = client.put('/todo/2/', data=json.dumps({"content": todo_new['content']}))
    res = client.get('/todo/')
    assert res.get_json() == [todos_req[0], todo_new, todos_req[2]]


def test_delete_todo(client, todos_req):
    for todo_req in todos_req:
        res = client.post('/todo/', data=json.dumps({"content": todo_req['content']}))

    res = client.delete('/todo/2/')
    assert res.get_json() == dict()

    res = client.get('/todo/')
    assert res.get_json() == [todos_req[0], todos_req[2]]
