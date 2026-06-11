import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
import psycopg2
import psycopg2.extras

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.environ["DATABASE_URL"]
API_KEY = os.environ["API_KEY"]


def timeago(dt):
    diff = datetime.now(timezone.utc) - dt
    mins = int(diff.total_seconds() / 60)
    if mins < 1:
        return "just now"
    if mins < 60:
        return f"{mins} min ago"
    hours = int(mins / 60)
    if hours < 24:
        return f"{hours}h ago"
    days = int(hours / 24)
    return f"{days}d ago"


app.jinja_env.filters["timeago"] = timeago


def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def init_db():
    for i in range(30):
        try:
            conn = get_db()
            break
        except Exception:
            if i == 29:
                raise
            import time
            time.sleep(2)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS deployments (
            id SERIAL PRIMARY KEY,
            service_name VARCHAR(100) NOT NULL,
            status VARCHAR(20) NOT NULL,
            version VARCHAR(100),
            commit_sha VARCHAR(40),
            message TEXT,
            deployed_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT * FROM deployments
        ORDER BY deployed_at DESC
        LIMIT 20
    """)
    deployments = cur.fetchall()
    cur.close()
    conn.close()

    latest = deployments[0] if deployments else None
    return render_template("index.html", deployments=deployments, latest=latest)


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/deployments", methods=["POST"])
def create_deployment():
    if request.headers.get("X-API-Key") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(force=True)
    required = ["service_name", "status"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO deployments (service_name, status, version, commit_sha, message)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            data["service_name"],
            data["status"],
            data.get("version"),
            data.get("commit_sha"),
            data.get("message"),
        ),
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "created"}), 201


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
