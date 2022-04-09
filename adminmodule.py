from flask import Flask, render_template, request
import sqlite3 as sql

from werkzeug.utils import redirect

connection = sql.connect("CrimeReport.db", check_same_thread=False)

admin = Flask(__name__)

@admin.route("/",methods=["POST","GET"])
def Login():
    if request.method == "POST":
        getusername=request.form["username"]
        getpassword=request.form["password"]
        print(getusername)
        print(getpassword)
        if getusername=="admin" and getpassword=="12345":
            return redirect("/viewreport")
    return  render_template("adminlogin.html")

@admin.route("/viewreport")
def view_crime_report():
    cursor = connection.cursor()
    count = cursor.execute("select * from user")
    result = cursor.fetchall()
    return render_template("viewreport.html", viewreport=result)

@admin.route("/filter")
def filter_with_dates():
    cursor = connection.cursor()
    count = cursor.execute("select * from user ORDER BY date")
    result = cursor.fetchall()
    return render_template("filter.html", filterreport=result)


if __name__=="__main__":
    admin.run()