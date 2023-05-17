from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/auth/whoami")
def auth_whoami():
    data = {"id": session["user_id"]}
    user = User.read(data)
    return render_template("auth_whoami.html", user=user)


@app.route("/auth/login", methods=["POST"])
def auth_login():
    data = {"email": request.form["email"]}
    user = User.read_by_email(data)
    if not user:
        session.clear()
        flash("Invalid Email/Password", "auth")
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        session.clear()
        flash("Invalid Email/Password", "auth")
        return redirect("/")

    session["user"] = {"id": user.id, "first_name": user.first_name}
    return redirect("/recipes")


@app.route("/auth/logout")
def auth_logout():
    session.clear()
    return redirect("/")
