from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app.lib.auth_functions import auth_required


@app.route("/recipes")
@auth_required
def get_recipes():
    all_recipes = Recipe.read_all()
    return render_template("user_recipe_list.html", all_recipes=all_recipes)


@app.route("/recipes/<int:id>")
@auth_required
def get_recipe(id):
    data = {"id": id}
    one_recipe = Recipe.read(data)
    return render_template("view_recipe.html", one_recipe=one_recipe)


@app.route("/recipes/new")
@auth_required
def new_recipe():
    return render_template("/create_recipe.html")


@app.route("/recipes/create", methods=["POST"])
@auth_required
def create_recipe():
    session["name"] = request.form["name"]
    session["description"] = request.form["description"]
    session["instructions"] = request.form["instructions"]
    session["cook_date"] = request.form["cook_date"]
    session["is_under_30_min"] = request.form["is_under_30_min"]
    messages = Recipe.validate(request.form)
    # print(messages)
    if messages:
        for flash_message in messages:
            print(flash_message)
            flash(flash_message["message"], flash_message["category"])
        return redirect("/recipes/new")
    else:
        data = {**request.form, "user_id": session["user"]["id"]}
        Recipe.create(data)
        session.pop("name")
        session.pop("description")
        session.pop("instructions")
        session.pop("cook_date")
        session.pop("is_under_30_min")
        return redirect("/recipes")


@app.route("/recipes/<int:id>/update", methods=["POST"])
@auth_required
def update_recipe(id):
    session["name"] = request.form["name"]
    session["description"] = request.form["description"]
    session["instructions"] = request.form["instructions"]
    session["cook_date"] = request.form["cook_date"]
    session["is_under_30_min"] = request.form["is_under_30_min"]
    messages = Recipe.validate(request.form)
    # print(messages)
    if messages:
        for flash_message in messages:
            print(flash_message)
            flash(flash_message["message"], flash_message["category"])
        return redirect(f"/recipes/{id}/edit")
    else:
        data = {**request.form, "id": id}
        Recipe.update(data)
        session.pop("name")
        session.pop("description")
        session.pop("instructions")
        session.pop("cook_date")
        session.pop("is_under_30_min")
        return redirect("/recipes")


@app.route("/recipes/<int:id>/edit")
@auth_required
def edit_recipe(id):
    data = {"id": id}
    one_recipe = Recipe.read(data)
    return render_template("edit_recipe.html", one_recipe=one_recipe)


@app.route("/recipes/<int:id>/delete")
@auth_required
def delete_recipe(id):
    data = {"id": id}
    Recipe.delete(data)
    return redirect("/recipes")
