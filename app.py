from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule, Submount
from werkzeug.exceptions import HTTPException
from views import todo


def hello(request: Request):
    return Response('Hello, World')


URL_MAP = Map([
    Rule('/', endpoint=hello),
    Submount('/todo', [
        Rule('/', methods=['GET'], endpoint=todo.get_all),
        Rule('/', methods=['POST'], endpoint=todo.post),
        Rule('/<int:todo_id>/', methods=['GET'], endpoint=todo.get),
        Rule('/<int:todo_id>/', methods=['PUT'], endpoint=todo.put),
        Rule('/<int:todo_id>/', methods=['DELETE'], endpoint=todo.delete)
    ])
])


def route(request: Request):
    adapter = URL_MAP.bind_to_environ(request.environ)
    try:
        endpoint, values = adapter.match()
        return endpoint(request, **values)
    except HTTPException as e:
        return e


def app(env, start_response):
    request = Request(env)
    response = route(request)
    return response(env, start_response)


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app, use_debugger=False, use_reloader=True)
