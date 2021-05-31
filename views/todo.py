from werkzeug.wrappers import Request, Response
from models.todo import Todo, TodoNotFound
from werkzeug.exceptions import BadRequest, NotFound
import json


def todo_to_dict(todo):
    return {'id': todo.id, 'content': todo.content}


class ValidationError(Exception):
    pass


def validate_todo(todo_dict):
    if 'content' not in todo_dict:
        raise ValidationError

    if type(todo_dict['content']) is not str:
        raise ValidationError


def get_all(request: Request):
    todos_dict = [todo_to_dict(todo) for todo in Todo.get_all()]
    todos_json = json.dumps(todos_dict, ensure_ascii=False)
    return Response(todos_json, mimetype='application/json')


def post(request: Request):
    todo_dict = request.get_json(force=True)

    try:
        validate_todo(todo_dict)
    except ValidationError:
        raise BadRequest('Todo ValidationError')

    todo_id = Todo(todo_dict['content']).insert()
    return Response(str(todo_id), mimetype='application/json')


def get(request: Request, todo_id: int):
    try:
        todo = Todo.get(todo_id)
    except TodoNotFound:
        raise NotFound('Todo NotFound')
    todo_dict = todo_to_dict(todo)
    todo_json = json.dumps(todo_dict, ensure_ascii=False)
    return Response(todo_json, mimetype='application/json')


def put(request: Request, todo_id: int):
    todo_dict = request.get_json(force=True)

    try:
        validate_todo(todo_dict)
        todo = Todo.get(todo_id)
    except ValidationError:
        raise BadRequest('Todo ValidationError')
    except TodoNotFound:
        raise NotFound('Todo NotFound')

    todo.content = todo_dict['content']
    todo.update()
    return Response('{}', mimetype='application/json')


def delete(request: Request, todo_id: int):
    try:
        todo = Todo.get(todo_id)
    except TodoNotFound:
        raise NotFound('Todo NotFound')
    todo.delete()
    return Response('{}', mimetype='application/json')
