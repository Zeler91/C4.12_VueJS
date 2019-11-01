import bottle
from truckpad.bottle.cors import CorsPlugin, enable_cors

app = bottle.Bottle() 

class TodoItem:
    def __init__(self, description, unique_id):
        self.description = description
        self.is_completed = False
        self.uid = unique_id

    def __str__(self):
        return self.description.lower()

    def to_dict(self):
        return {
            "description": self.description,
            "is_completed": self.is_completed,
            "uid": self.uid
        }


tasks_db = {
    uid: TodoItem(desc, uid)
    for uid, desc in enumerate(
        start=1,
        iterable=[
            "прочитать книгу",
            "учиться жонглировать 30 минут",
            "помыть посуду",
            "поесть",
        ],
    )
}


@enable_cors 
@app.route("/api/tasks/") 
def index():
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    tasks = [task.to_dict() for task in tasks_db.values()]
    return {"tasks": tasks}

@enable_cors
@app.route("/api/tasks/", method="POST")
def add_task():
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    desc = bottle.request.json['description']
    is_completed = bottle.request.json['is_completed']
    if len(desc) > 0:
        if tasks_db:
            new_uid = max(tasks_db.keys()) + 1
        else:
            new_uid = 1
        t = TodoItem(desc, new_uid)
        t.is_completed = is_completed
        tasks_db[new_uid] = t
    return "OK"

@enable_cors
@app.route("/api/tasks/init", method="POST")
def add_task():
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    tasks_db.clear()
    print(bottle.request.json);
    for request in bottle.request.json:
        desc = request['description']
        is_completed = request['is_completed']
        if len(desc) > 0:
            new_uid = request["uid"]
            t = TodoItem(desc, new_uid)
            t.is_completed = is_completed
            tasks_db[new_uid] = t
    return "OK"

@enable_cors
@app.route("/api/tasks/<uid:int>", method=["GET","POST", "PUT", "DELETE"])
def show_or_modify_task(uid):
    if bottle.request.method == "GET":
        return tasks_db[uid].to_dict()
    # elif bottle.request.method == "POST":
    #     bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    #     desc = bottle.request.json['description']
    #     is_completed = bottle.request.json['is_completed']
    #     if len(desc) > 0:
    #         tasks_db[uid] = TodoItem(desc, uid)
    #     return "OK"
    elif bottle.request.method == "PUT":
        if "description" in bottle.request.json:
            tasks_db[uid].description = bottle.request.json['description']
        if "is_completed" in bottle.request.json:
            tasks_db[uid].is_completed = bottle.request.json['is_completed']
        return f"Modified task {uid}"
    elif bottle.request.method == "DELETE":
        bottle.response.headers['Access-Control-Allow-Origin'] = '*'
        if tasks_db[uid]:
            tasks_db.pop(uid)
            return f"Deleted task {uid}"


# ..

app.install(CorsPlugin(origins=['http://localhost:8000'])) 

if __name__ == "__main__":
    bottle.run(app, host="localhost", port=5000) 