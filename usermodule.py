from flask import Flask, request, render_template,session
import sqlite3 as sql
from flask_session import Session
from werkzeug.utils import redirect

connection = sql.connect("CrimeReport.db", check_same_thread=False)

listofuser = connection.execute("select name from sqlite_master where type='table' AND name='user'").fetchall()

if listofuser != []:
    print("Table exist already")
else:
    connection.execute('''create table user(
                             ID integer primary key autoincrement,
                             name text,
                             address text,
                             email text,
                             phone integer,
                             password text,
                             date text,
                             description text,
                             remark text                            
                             )''')
    print("Table Created Successfully")

user=Flask(__name__)
user.config["SESSION_PERMANENT"] = False
user.config["SESSION_TYPE"] = "filesystem"
Session(user)

@user.route("/",methods=["POST","GET"])
def user_registration_details():
    if request.method == "POST":
        getname = request.form["name"]
        getaddress = request.form["address"]
        getemail = request.form["email"]
        getphone = request.form["phone"]
        getpassword = request.form["password"]
        try:
            connection.execute("insert into user(name,address,email,phone,password)\
                                   values('" + getname + "','" + getaddress + "','" + getemail + "'," + getphone + ",'" + getpassword + "')")
            connection.commit()
            print("User Data Added Successfully.")
        except Exception as e:
            print(e)

        return redirect("/userlogin")

    return render_template("user_registration.html")

@user.route("/userlogin",methods=["POST","GET"])
def user_login():
    global result
    if request.method == "POST":
        getemail = request.form["email"]
        getpassword = request.form["password"]
        cursor = connection.cursor()
        query = "select * from user where email='"+getemail+"' and password='"+getpassword+"'"
        print(query)
        result = cursor.execute(query).fetchall()
        if len(result) > 0:
            for i in result:
                getname=i[1]
                getid=i[0]
                session["name"]=getname
                session["id"]=getid

            return redirect("/session")
    return render_template("userlogin.html")

@user.route("/complaint",methods=["POST","GET"])
def complaint_report():
    if request.method == "POST":
        getdate = request.form["date"]
        getremark = request.form["remark"]
        getdescription = request.form["description"]
        try:
            connection.execute("insert into user(date,remark,description)\
                               values('"+getdate+"','"+getremark+"','"+getdescription+"')")
            connection.commit()
            print("Inserted Successfully")
        except Exception as e:
            print(e)

    return render_template("complaint.html")

@user.route("/edit",methods=["GET","POST"])
def edit_profile():
    if request.method == "POST":
        getemail = request.form["email"]
        getname = request.form["name"]
        getaddress = request.form["address"]
        getphone = request.form["phone"]
        getpassword = request.form["password"]
        try:
            query = "update user set name='"+getname+"',address='"+getaddress+"',phone="+getphone+",password='"+getpassword+"'  where email='"+getemail+"'"
            print(query)
            connection.execute(query)
            connection.commit()
            print("Updated Successfully")
        except Exception as e:
            print(e)

    return render_template("edit.html")

@user.route("/logout")
def user_logout():
    return render_template("userlogin.html")

@user.route("/session")
def user_session():
    if not session.get("name"):
        return redirect("/userlogin")
    else:
        return render_template("session.html")

@user.route("/updatesearch",methods = ["GET","POST"])
def update_search_patient():
    if request.method == "POST":
        getemail = request.form["email"]
        print(getemail)
        cursor = connection.cursor()
        count = cursor.execute("select * from user where email='"+getemail+"'")
        result = cursor.fetchall()
        print(len(result))
        return render_template("edit.html", userupdate=result)

    return render_template("edit.html")

if __name__ == "__main__":
    user.run()