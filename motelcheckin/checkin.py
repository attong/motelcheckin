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
import json


from db import get_db

bp = Blueprint("checkin", __name__)

@bp.route("/")
def index():
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
        SELECT * FROM stays right join 
        (SELECT rooms.room, min(check_in_date) FROM stays right join rooms on stays.room=rooms.room GROUP BY rooms.room) AS X on stays.room = X.room;

        """)
    return redirect("/findcustomer")

@bp.route("/addcustomer/", methods=("GET", "POST"))
def add_customer():
    if request.method == "GET":
        return render_template("add_customer.html")
    elif request.method == "POST":
        try:
            data = request.form
            if (data['driverslicense']==''):
                license = 'null'
            else:
                license = "'"+data['driverslicense']+"'"
            if (data['notes']==''):
                notes='null'
            else:
                notes = "'"+data['notes']+"'"
            db = get_db()
            cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("""
                 INSERT INTO Customers VALUES ('{fname}','{lname}','{bdate}',{license},{notes})
                 """.format(fname=data['firstname'],lname=data['lastname'], bdate=data['birthdate'],license=license,notes=notes))
            db.commit()
            flash("Add Customer Successful!")
            return redirect("/findcustomer")
        except:
            flask("Insertion failed. Please verify data is correct")
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
            (upper(identification) = upper('{id}') OR '{id}' = '')
            """.format(fname=data['firstname'],lname=data['lastname'], bdate=bdate,bdate2=data['birthdate'],id=data['id']))
        data = cursor.fetchall()
        # if find, redirect to checkin page
        #else add customer
        print(data)
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
    print(data)
    if (data['check_in_date'] >= data['check_out_date']):
        flash("Error. Check out date must be after check in date!")
        return redirect("/findcustomer")
    try:
        room= json.loads(data['room'])
        print(room['room'])
        cursor.execute("""
            UPDATE Rooms SET Occupied = TRUE WHERE Room = {}
            """.format(room['room']))
        cursor.execute("""
            INSERT INTO Stays (cu_id,check_in_date,check_out_date,status,numadults,numchildren,num_pets, room) VALUES
            ({cu_id},'{checkin}','{checkout}','{status}',{adults},{children}, {pets}, {room}) RETURNING stay_id;
            """.format(cu_id = data['cu_id'],checkin=data['check_in_date'],checkout=data['check_out_date'],status='Checked In', adults=data['adults'], children=data['children'], pets=data['pets'], room = room['room']))
        print("here")
        print(""" INSERT INTO Stays (cu_id,check_in_date,check_out_date,status,numadults,numchildren,num_pets, room) VALUES
            ({cu_id},'{checkin}','{checkout}','{status}',{adults},{children}, {pets}, {room}) RETURNING stay_id;
            """.format(cu_id = data['cu_id'],checkin=data['check_in_date'],checkout=data['check_out_date'],status='Checked In', adults=data['adults'], children=data['children'], pets=data['pets'], room = room['room']))
        stay_id = cursor.fetchone()
        stay_id = dict(stay_id)['stay_id']
        cursor.execute("""
            INSERT INTO Stayperiods VALUES
            ({stay_id},{cu_id},'{checkin}','{checkout}', {price})
            """.format(stay_id=stay_id,cu_id = data['cu_id'],checkin=data['check_in_date'],checkout=data['check_out_date'],price=data['price']))
        db.commit()
        flash("Check in Successful!")
        return redirect("findcustomer")
    except Exception as temp:
        print(temp)
        flash("checkin failed. Please retry")
        return redirect("findcustomer")
        