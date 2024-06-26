import functools
import json
import jwt
from pprint import pprint

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .api import ChillerSDK

bp = Blueprint("user", __name__, url_prefix="/user")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("user.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    jwt_token = session.get("jwt_token")

    if jwt_token is None:
        g.user = None
    else:
        payload = jwt.decode(jwt_token['token'], options={"verify_signature": False})
        g.user = payload
        assert "name" in g.user
        assert "id" in g.user


@bp.route("/create", methods=("POST",))
def create():
    """Create a new user.

    """
    w = ChillerSDK()

    rf = request.form
    key = "username"

    if key not in rf or rf[key] is None or len(rf[key]) == 0:
        error = "Username is required."
    else:
        success, error = w.user_create(rf[key])
        if success:
            return login_processing(rf[key])

    if error is not None:
        flash(error)
    return redirect(url_for("user.login"))


def login_processing(username):
    """
    do all login processing for user
    called from both create and login
    """
    w = ChillerSDK()

    jwt_token, msg = w.get_user_login(username)
    if jwt_token is not None:
        session.clear()
        session["jwt_token"] = jwt_token.to_dict()
        return redirect(url_for("movies.list"))
    else:
        flash(msg)
        return redirect(url_for("user.login"))


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":

        rf = request.form
        key = "username"

        if key not in rf or rf[key] is None or len(rf[key]) == 0:
            flash("Username is required.")
        else:
            return login_processing(request.form["username"])

    return render_template("user/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("user.login"))
