from flask_app import app
from flask import render_template, request, redirect, session


@app.route("/")
def index():
    if "user" in session:
        return redirect("/recipes")
    else:
        return render_template("index.html")
