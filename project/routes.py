from project import app
from flask import render_template
from project.models import User


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile/<username>")
def display_profile(username):
    user = User.query.filter_by(username=username).one()
    return render_template("profile.html", user=user)


@app.route("/about")
def about():
    return render_template("about.html")
