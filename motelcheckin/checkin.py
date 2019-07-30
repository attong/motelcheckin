from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint("checkin", __name__)

    
@bp.route("/checkin/<id>", methods=("GET", "POST"))
def check_in(id):
    if request.method == "GET":
        return render_template("checkin.html") 
        