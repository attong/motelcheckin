from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint("checkin", __name__)

@bp.route("/findcustomer", methods=("GET", "POST"))
def check_in(id):
    if request.method == "GET":
        return render_template("find_customer.html")
    elif request.method == "POST":
    	# if find, redirect to checkin page
    	#else add customer
    	return "finding customer!"

@bp.route("/addcustomer", methods=("GET","POST"))

@bp.route("/checkin/<id>", methods=("GET", "POST"))
def check_in(id):
    if request.method == "GET":
        return render_template("checkin.html") 
        