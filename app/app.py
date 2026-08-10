import os
import random
import string
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# ----------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ----------------------------------------------------
# Flask App
# ----------------------------------------------------

app = Flask(__name__)

# Database Connection
# Use Postgres when all DB env vars are present (Docker / Kubernetes / Vercel
# with a configured cloud database). Fall back to SQLite in-memory when vars
# are absent so the app still starts on Vercel before a DB is wired up.
_db_vars = (
    os.getenv("DB_USER"),
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_HOST"),
    os.getenv("DB_PORT"),
    os.getenv("DB_NAME"),
)

if all(_db_vars):
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{_db_vars[0]}:"
        f"{_db_vars[1]}@"
        f"{_db_vars[2]}:"
        f"{_db_vars[3]}/"
        f"{_db_vars[4]}"
    )
else:
    # Fallback: in-memory SQLite so the Flask app starts without crashing.
    # URL shortening will work ephemerally; data is not persisted between
    # requests in this mode. Set the five DB_* env vars to enable Postgres.
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ----------------------------------------------------
# Prometheus Metrics
# ----------------------------------------------------

url_counter = Counter(
    "shortened_urls_total",
    "Total number of shortened URLs"
)

redirect_counter = Counter(
    "redirect_requests_total",
    "Total redirect requests"
)

# ----------------------------------------------------
# Database Model
# ----------------------------------------------------

class URL(db.Model):

    __tablename__ = "urls"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    original_url = db.Column(
        db.Text,
        nullable=False
    )

    short_code = db.Column(
        db.String(10),
        unique=True,
        nullable=False
    )

    clicks = db.Column(
        db.Integer,
        default=0
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )


# ----------------------------------------------------
# Create Database Tables
# ----------------------------------------------------

with app.app_context():
    try:
        db.create_all()
    except Exception:
        # Database may not be available at import time (e.g. Vercel cold start
        # before DB env vars are set). The app still loads; DB-dependent routes
        # will return errors only if the DB is genuinely unreachable at runtime.
        pass
    except BaseException:
        pass


# ----------------------------------------------------
# Generate Random Short Code
# ----------------------------------------------------

def generate_code(length=6):

    characters = string.ascii_letters + string.digits

    return "".join(
        random.choice(characters)
        for _ in range(length)
    )


# ----------------------------------------------------
# Home Page
# ----------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    short_url = None

    if request.method == "POST":

        original_url = request.form["url"]

        short_code = generate_code()

        while URL.query.filter_by(
            short_code=short_code
        ).first():

            short_code = generate_code()

        new_url = URL(
            original_url=original_url,
            short_code=short_code
        )

        db.session.add(new_url)
        db.session.commit()

        url_counter.inc()

        short_url = request.host_url + short_code

    return render_template(
        "index.html",
        short_url=short_url
    )


# ----------------------------------------------------
# Redirect Route
# ----------------------------------------------------

@app.route("/<short_code>")
def redirect_to_url(short_code):

    url = URL.query.filter_by(
        short_code=short_code
    ).first()

    if not url:
        return "URL Not Found", 404

    url.clicks += 1

    db.session.commit()

    redirect_counter.inc()

    return redirect(url.original_url)


# ----------------------------------------------------
# Health Check
# ----------------------------------------------------

@app.route("/health")
def health():

    return {
        "status": "UP"
    }, 200


# ----------------------------------------------------
# Prometheus Metrics
# ----------------------------------------------------

@app.route("/metrics")
def metrics():

    return (
        generate_latest(),
        200,
        {
            "Content-Type": CONTENT_TYPE_LATEST
        }
    )


# ----------------------------------------------------
# Main
# ----------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )