from flask import Flask, request, render_template, session
import sqlite3

from flask_session import Session
from werkzeug.utils import redirect
from datetime import date

connection = sqlite3.connect("CrimeReport.db",check_same_thread=False)
table1 = connection.execute("select * from sqlite_master where type = 'table' and name = 'crime'").fetchall()
table2 = connection.execute("select * from sqlite_master where type = 'table' and name = 'user'").fetchall()

if table1 !=[]:
    print("Crime table already exists")
else:
    connection.execute('''create table crime(
                            id integer primary key autoincrement,
                            description text,
                            remarks text,
                            date text);''')
    print("Table created")
if table2 !=[]:
    print("user table already exists")
else:
    connection.execute('''create table user(
                            id integer primary key autoincrement,
                            name text,
                            address text,
                            email text,
                            phone integer,
                            password text);''')
    print("Table created")

crimereport = Flask(__name__)

crimereport.config["SESSION_PERMANENT"] = False
crimereport.config["SESSION_TYPE"] = "filesystem"
Session(crimereport)


@crimereport.route('/', methods=['GET', 'POST'])
def Login_admin():
    if request.method == 'POST':
        getUsername = request.form["admname"]
        getPassword = request.form["admpass"]
        print(getUsername)
        print(getPassword)
        if getUsername == "admin" and getPassword == "12345":
            return redirect('/dashboard')
        else:
            return redirect('/')
    return render_template("adminlogin.html")

@crimereport.route('/dashboard')
def Admin_dashboard():
    return render_template("dashboard.html")

@crimereport.route('/view')
def View_report():
    cursor = connection.cursor()
    cursor.execute("select * from crime")

    result = cursor.fetchall()
    return render_template("viewall.html",crime=result)


@crimereport.route('/sort', methods=['GET', 'POST'])
def Search_crime():
    if request.method == 'POST':
        getDate = str(request.form["date"])
        cursor = connection.cursor()
        cursor.execute("select * from crime where date='"+getDate+"'")
        result = cursor.fetchall()
        if result is None:
            print("There is no Crime on",getDate)
        else:
            return render_template("datesort.html",crime=result,status=True)
    else:
        return render_template("datesort.html",crime=[],status=False)

@crimereport.route('/register', methods=['GET', 'POST'])
def User_register():
    if request.method == 'POST':
        getName = request.form["username"]
        getAddress = request.form["address"]
        getEmail = request.form["useremail"]
        getPhone = request.form["userphone"]
        getPass = request.form["userpass"]
        print(getName,getAddress,getEmail,getPhone)
        try:
            connection.execute("insert into user(name,address,email,phone,password) \
            values('"+getName+"','"+getAddress+"','"+getEmail+"',"+getPhone+",'"+getPass+"')")
            connection.commit()
            print("Inserted Successfully")
            return redirect('/complaint')
        except Exception as err:
            print(err)
    return render_template("userreg.html")

@crimereport.route('/user', methods=['GET', 'POST'])
def Login_user():
    if request.method == 'POST':
        getEmail = request.form["useremail"]
        getPass = request.form["userpass"]
        cursor = connection.cursor()
        query = ("select * from user where email='"+getEmail+"' and password='"+getPass+"'")
        result = cursor.execute(query).fetchall()
        if len(result)>0:
            for i in result:
                getName = i[1]
                getId = i[0]
                session["name"] = getName
                session["id"] = getId
                if (getEmail == i[3] and getPass == i[5]):
                    print("password correct")
                    return redirect('/usersession')
                else:
                    return render_template("userlogin.html",status=True)
    else:
        return render_template("userlogin.html",status=False)

@crimereport.route('/userdashboard')
def user_dashboard():
    return render_template("userdashboard.html")

@crimereport.route('/usersession')
def userpage():
    if not session.get("name"):
        return redirect('/')
    else:
        return render_template("session.html")


@crimereport.route('/complaint', methods=['GET', 'POST'])
def Report_crime():
    if request.method == 'POST':
        getDescription = request.form["descrip"]
        getRemark = request.form["remark"]
        print(getDescription)
        print(getRemark)
        getDate = str(date.today())
        cursor = connection.cursor()
        query = ("insert into crime(description,remarks,date) values('"+getDescription+"','"+getRemark+"','"+getDate+"')")
        cursor.execute(query)
        connection.commit()
        print(query)
        print("Inserted Successfully")
        return redirect('/user')
    return render_template("newcomplaint.html")

@crimereport.route('/update', methods=['GET', 'POST'])
def Update_user():
    try:
        if request.method == 'POST':
            getname = request.form["newname"]
            print(getname)
            cursor = connection.cursor()
            count = cursor.execute("select * from user where name='"+getname+"'")
            result = cursor.fetchall()
            print(len(result))
            return render_template("profileedit.html", searchname = result)
        return render_template("profileedit.html")
    except Exception as err:
        print(err)


@crimereport.route('/edit', methods=['GET', 'POST'])
def User_edit():
    if request.method == 'POST':
        getName = request.form["newname"]
        getAddress = request.form["newaddress"]
        getEmail = request.form["newemail"]
        getPhone = request.form["newphone"]
        getPass = request.form["newpass"]
        try:
            query = ("update user set address='"+getAddress+"',email='"+getEmail+"',phone="+getPhone+",password='"+getPass+"' where name='"+getName+"'")
            print(query)
            connection.execute(query)
            connection.commit()
            print("Edited Successfully")
            return redirect('/view')
        except Exception as error:
            print(error)

    return render_template("profileedit.html")

@crimereport.route('/logout')
def Logout():
    session["name"] = None
    return redirect('/')

if __name__=="__main__":
    crimereport.run()