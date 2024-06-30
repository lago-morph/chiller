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

from pprint import pprint

@bp.route("/list", methods=("GET",))
@login_required
def list():
    """
    get the movies in this user's list
    """
    w = ChillerSDK()
    error = None

    movielist, msg = w.get_movies_list(g.user["id"])
    if movielist is None:
        movielist = []
        error = msg

    if error is not None:
        flash(error)

    return render_template("movies/list.html", movielist=movielist)


@bp.route("/add", methods=("POST",))
@login_required
def add():
    """add a movie to the current user's list
    """
    w = ChillerSDK()
    error = None

    rf = request.form
    key = "title"

    if key not in rf or rf[key] is None or len(rf[key]) == 0:
        error = "Movie title is required"
    else:
        success, msg = w.movies_add(g.user["id"], rf[key])
        if not success:
            error = msg

    if error is not None:
        flash(error)

    return redirect(url_for("movies.list"))
