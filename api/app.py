import time
import redis
from flask import Flask, jsonify, abort, make_response
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()
cache = redis.Redis(host='redis', port=6379)

tasks = [
  {
    "id": 1,
    "task": "task0"
  },
  {
    "id": 2,
    "task": "task1"
  }
]

@auth.get_password
def get_password(username):
  if username == "minhthai":
    return "python"
  return None

@auth.error_handler
def unauthorized():
  return make_response(jsonify({ "error": "Unauthorized access"}), 401)

def get_hit_count():
  retries = 5
  while True:
    try:
      return cache.incr('hits')
    except redis.exceptions.ConnectionError as exc:
      if retries == 0:
        raise exc
      retries -= 1
      time.sleep(0.5)

@app.route("/")
def hello():
    count = get_hit_count()
    return 'Hello world! I have been seen {} time.\n'.format(count)

@app.route("/api/v1/tasks", methods=["GET"])
@auth.login_required
def get_tasks():
  return jsonify({ "tasks": tasks }) 

@app.route("/api/v1/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
  task = [task for task in tasks if task["id"] == task_id]
  if len(task) == 0:
    abort(404)
  return jsonify({ 'task': task[0] })

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({ "error": "Not found"}), 404)

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)