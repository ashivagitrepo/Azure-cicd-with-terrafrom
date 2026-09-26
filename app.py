from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "tasks.db"


def get_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            status TEXT DEFAULT 'To Do',
            priority TEXT DEFAULT 'Medium'
        )
    """)

    columns = [row[1] for row in conn.execute("PRAGMA table_info(tasks)")]

    if "status" not in columns:
        conn.execute(
            "ALTER TABLE tasks ADD COLUMN status TEXT DEFAULT 'To Do'"
        )

    if "priority" not in columns:
        conn.execute(
            "ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'Medium'"
        )

    conn.execute("""
        UPDATE tasks
        SET status = 'Completed'
        WHERE completed = 1 AND status = 'To Do'
    """)

    conn.commit()

    return conn


@app.route("/")
def home():
    search = request.args.get("search", "")
    status = request.args.get("status", "")
    priority = request.args.get("priority", "")

    conn = get_db()

    query = """
        SELECT id, task, completed, status, priority
        FROM tasks
        WHERE 1=1
    """

    params = []

    if search:
        query += " AND task LIKE ?"
        params.append(f"%{search}%")

    if status:
        query += " AND status = ?"
        params.append(status)

    if priority:
        query += " AND priority = ?"
        params.append(priority)

    tasks = conn.execute(query, params).fetchall()

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks,
        search=search,
        selected_status=status,
        selected_priority=priority
    )


@app.route("/add", methods=["POST"])
def add_task():
    task = request.form["task"]
    priority = request.form.get("priority", "Medium")

    conn = get_db()

    conn.execute("""
        INSERT INTO tasks (task, status, priority)
        VALUES (?, 'To Do', ?)
    """, (task, priority))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    status = request.form["status"]
    priority = request.form["priority"]

    conn = get_db()

    conn.execute("""
        UPDATE tasks
        SET status = ?, priority = ?
        WHERE id = ?
    """, (status, priority, task_id))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
