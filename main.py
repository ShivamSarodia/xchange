from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/create-task")
def create_task():
    return render_template('create_task.html')

@app.route("/login-back", methods = ['POST'])
def login():
    print(request.form["accessToken"])
    if request.method == "POST":
        uid = request.form["uid"]
        accessToken = request.form["accessToken"]
        fullname = request.form["fullName"]

        if len(query_db("select * from users where fb_user_id = ?", [uid])) == 0: #if the user doesn't exist
              print("Adding new user")
              query_db("insert into users (fb_user_id, fullname) values (?, ?)", [uid, fullname])

        return "Login success"
    else:
        print("Not a POST")
    return ""

@app.route("/make-task-back", methods = ['POST'])
def make_task():
    if request.method == "POST":
        status = "pending"
        title = request.form["title"]
        description = request.form["description"]
        salary = request.form["salary"]
        lat = request.form["lat"]
        lon = request.form["longi"]
        poster_id = request.form["uid"]

        query_db("insert into tasks (status, title, description, salary, lat, lon, poster_id) values (?, ?, ?, ?, ?, ?, ?)", [status, title, description, salary, lat, lon, poster_id])

        return ""
    else:
        print("Not a POST")
        return ""

##### DATABASE STUFF ######

DATABASE = 'db/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('db/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    get_db().commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    print("Closed connection")
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug = True)
 
