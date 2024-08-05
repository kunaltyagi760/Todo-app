from api import app, db
# import stripe
# import requests
import os
import urllib.request
from werkzeug.utils import secure_filename 
from flask import Flask, jsonify, request, render_template, redirect
from api import models
from api.models import db, Todo
from flask import send_from_directory, url_for, send_file

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from flask import request, jsonify
from api.queries import resolve_todos, resolve_todo
from api.mutations import resolve_create_todo, resolve_mark_done, \
    resolve_delete_todo, resolve_update_premium, resolve_create_user, \
    resolve_create_worktype, resolve_delete_work, resolve_addimg, \
    resolve_update_todo, resolve_mutate_worktype
from api.queries import resolve_worktypes, resolver_works, resolve_users, \
    resolve_user, resolve_todos_user

query = ObjectType("Query")

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

query.set_field("todos", resolve_todos)
query.set_field("todo", resolve_todo)
query.set_field("works", resolve_worktypes)
query.set_field("work", resolver_works)
query.set_field("users", resolve_users)
query.set_field("user", resolve_user)
query.set_field("usersTodos", resolve_todos_user)

mutation = ObjectType("Mutation")
mutation.set_field("updatepremium", resolve_update_premium)
mutation.set_field("markDone", resolve_mark_done)
mutation.set_field("createTodo", resolve_create_todo)
mutation.set_field("createUser", resolve_create_user)
mutation.set_field("createWorks", resolve_create_worktype)
mutation.set_field("deleteTodo", resolve_delete_todo)
mutation.set_field("deleteWorks", resolve_delete_work)
mutation.set_field("addImage", resolve_addimg)
mutation.set_field("updateTodo", resolve_update_todo)
mutation.set_field("updateWork", resolve_mutate_worktype)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)

PLAYGROUND_HTML = """
<!DOCTYPE html>
<html>

<head>
  <meta charset=utf-8/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GraphQL Playground</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/css/index.css" />
  <link rel="shortcut icon" href="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/favicon.png" />
  <script src="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/js/middleware.js"></script>
</head>

<body>
  <div id="root"/>
  <script type="text/javascript">
    window.addEventListener('load', function (event) {
      const root = document.getElementById('root');
      GraphQLPlayground.init(root, { endpoint: '/graphql' })
    })
  </script>
</body>

</html>
"""

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True)

