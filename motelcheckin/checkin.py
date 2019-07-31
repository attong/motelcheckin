from datetime import datetime

import pandas as pd
import psycopg2.extras
import re
import uuid

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify
from flask import session
from flask import abort


from db import get_db

bp = Blueprint("checkin", __name__)

@bp.route("/findcustomer", methods=("GET", "POST"))
def find_customer():
    if request.method == "GET":
        return render_template("find_customer.html")
    elif request.method == "POST":
        data = request.form
        db = get_db()
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if (data['birthdate']==''):
            bdate = '01-01-1200'
        else:
            bdate = data['birthdate']
        cursor.execute("""
            SELECT * FROM customers WHERE 
            (upper(first_name) = upper('{fname}') OR '{fname}' = '') AND
            (upper(last_name) = upper('{lname}') OR '{lname}' = '') AND 
            (birth_date - '{bdate}' = 0 OR '{bdate2}' = '') AND
            (upper(driving_license_number) = upper('{license}') OR '{license}' = '')
            """.format(fname=data['firstname'],lname=data['lastname'], bdate=bdate,bdate2=data['birthdate'],license=data['driverslicense']))
        data = dict(cursor.fetchall())
        # if find, redirect to checkin page
        #else add customer
        return render_template("select_customer.html",data=data)

# @bp.route("/selectcustomer", methods=("GET","POST"))

@bp.route("/checkin/<id>", methods=("GET", "POST"))
def check_in(id):
    if request.method == "GET":
        return render_template("checkin.html")
    else:
        return "Hi"
        