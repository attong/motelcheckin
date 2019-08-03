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

@bp.route("/")
def index():
    return redirect("/findcustomer")

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
        data = cursor.fetchall()
        # if find, redirect to checkin page
        #else add customer
        return render_template("select_customer.html",data=data)

@bp.route("/checkinform", methods=("POST",))
def checkinform():
    data = request.form.to_dict()
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
        SELECT room, type from Rooms WHERE occupied = FALSE;
        """)
    avail_rooms = cursor.fetchall()
    return render_template("checkin.html",data=data, avail_rooms=avail_rooms)

@bp.route("/checkin", methods=("POST",))
def check_in():
    data = request.form.to_dict()
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if (data['check_in_date'] >= data['check_out_date']):
        flash("Error. Check out date must be after check in date!")
        return redirect("/findcustomer")
    cursor.execute("""
        UPDATE Rooms SET Occupied = TRUE WHERE Room = {}
        """.format(data['room']))
    cursor.execute("""
        INSERT INTO Stays VALUES
        ('{fname}','{lname}','{bdate}','{checkin}','{checkout}','{status}',{room})
        """.format(fname=data['first_name'],lname=data['last_name'],bdate=data['birth_date'],checkin=data['check_in_date'],checkout=data['check_out_date'],status='Checked In', room=data['room']))
    db.commit()
    flash("Check in Successful!")
    return redirect("findcustomer")
        