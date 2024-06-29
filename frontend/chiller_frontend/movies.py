from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from .api import ChillerSDK

from .user import login_required

bp = Blueprint("movies", __name__, url_prefix="/movies")

@bp.route("/list", methods=("GET",))
@login_required
def list():
    """
    get the movies in this user's list
    """
    api = ChillerSDK()
    error = None

    movielist, msg = api.m.movies_list(g.user["id"])
    if movielist is None:
        movielist = []
        error = msg

    flash(error)

    return render_template("movies/list.html")


@bp.route("/add", methods=("POST",))
@login_required
def add():
    """add a movie to the current user's list
    """
    api = ChillerSDK()
    error = None

    title = request.form["title"]

    if not title:
        error = "Movie title is required"

    if error is None:
        success, msg = api.m.movies_add(g.user["id"], title)
        if not success:
            error = msg

    flash(error)

    return redirect(url_for("movies.list"))
