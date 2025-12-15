from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)

@app.route("/add_form")
def add_form():
    return render_template("add.html")

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form["title"]
    priority = request.form["priority"]
    due_date = request.form["due_date"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO tasks (title, status, priority, due_date) VALUES (?, ?, ?, ?)",
        (title, "todo", priority, due_date)
    )
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)


