from functools import wraps
from flask import redirect, session, flash


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            flash("You must be logged in to access the page.", "page")
            return redirect("/")
        else:
            return f(*args, **kwargs)

    return decorated
