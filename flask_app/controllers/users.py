from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/users/create", methods=["POST"])
def create_user():
    session["first_name"] = request.form["first_name"]
    session["last_name"] = request.form["last_name"]
    session["email"] = request.form["email"]
    messages = User.validate(request.form)
    # print(messages)
    if messages:
        for flash_message in messages:
            print(flash_message)
            flash(flash_message["message"], flash_message["category"])
        return redirect("/")
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    user_id = User.create(data)
    session["user_id"] = user_id
    session.pop("first_name")
    session.pop("last_name")
    session.pop("email")
    flash("Your account has been created. You can log in.", "page")
    return redirect("/")
