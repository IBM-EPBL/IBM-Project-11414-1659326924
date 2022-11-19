from flask import Flask, render_template, request, redirect, url_for, session, flash
import ibm_db
import re
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# app
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '987654321789456123'

# mail
try:
    sg = SendGridAPIClient('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')
except Exception as e:
    print(e)

#dbconn
def dbconn():
    conn = None
    try:
        conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;\
            PORT=31498;PROTOCOL=TCPIP;UID=xgm40296;PWD=89gtA0GUu8Dxxjxa;SECURITY=SSL;SSLServiceCertificate=DigiCertGlobalRootCA.crt", "", "")
    except Exception as e:
        print(e)
    return conn

conn = dbconn()

# base
@app.route('/')
def welcom():
    return render_template('homepage.html')

# signup
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST','GET'])
def signupp():
    if request.method == 'POST':
        print(request.form)
        new_email = request.form['email']
        new_username = request.form['user']
        new_password = request.form['pass']
        repass = request.form['pass'] == request.form['repass']
        if repass == False:
            flash("passwords do not match")
            return render_template('signup.html')
        try:
            curr1 = "INSERT INTO USERS (email,username,pass) VALUES('{}','{}','{}')".format(request.form["email"], request.form["user"],  request.form["pass"])
            ibm_db.exec_immediate(conn,curr1)
        except Exception as ee:
            print(ee)
            flash("username already exists!!!")
            return render_template("signup.html")
        curr2 = "SELECT * FROM USERS WHERE username = ('{}')".format(new_username,)
        cur2e = ibm_db.exec_immediate(conn,curr2)
        cur2ex = ibm_db.fetch_tuple(cur2e)
        books = dict(id=cur2ex[0], email=cur2ex[1], username=cur2ex[2],  password=cur2ex[3] )
        flash("Registration successful. Please login")
        return render_template('login.html'), 201

# login
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST','GET'])
def loginn():
    if request.method == 'POST':
        print("ur absolutely pathetic dude")
        cursorr = ibm_db.exec_immediate(conn,"SELECT * FROM USERS where username = ('{}')".format(request.form['user']))
        currex = ibm_db.fetch_tuple(cursorr)
        print(currex)
        if type(currex) is bool:
            flash("user does not exist")
            return redirect(url_for('signup'))
        if currex[2] == request.form['user']:
            if currex[3] == request.form['pass']:
                session["user"] = request.form['user']
                return redirect(url_for('dash'))
            else:
                print(currex)
                flash("password incorrect go back")
                return redirect(url_for("loginn"))
        return render_template("login.html")

# dashboard
@app.route('/dashboard')
def dash():
    if "user" in session:
        usr = session['user']
        ur = ibm_db.exec_immediate(conn,"SELECT user_id FROM USERS where username = ('{}')".format(usr))
        uid = ibm_db.fetch_tuple(ur)
        for i in uid:
            x = int(i)
        curexp = ibm_db.exec_immediate(conn,"SELECT sum(expense) FROM EXPENSES where user_id = ('{}')".format(x))
        totexp = ibm_db.fetch_tuple(curexp)
        for j in totexp:
            y = int(j)
        curey = ibm_db.exec_immediate(conn,"SELECT email FROM USERS where username = ('{}')".format(usr))
        curem = ibm_db.fetch_tuple(curey)
        for k in curem:
            email = str(k)
        if y > budget:
            message = Mail(
            from_email='admin@123.com',
            to_emails=email,
            subject='Your Expenses are getting higher',
            html_content='Your expenses have crossed the monthly budget')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        curall = ibm_db.exec_immediate(conn,"SELECT expense,expense_detail FROM EXPENSES where user_id = ('{}')".format(x))
        curem = ibm_db.fetch_assoc(curall)
        items_list = []
        while curem != False:
            items_list.append(curem)
            curem = ibm_db.fetch_assoc(curall)
        print(curem)
        #items_list = [{'1': 'Hello', '2': 'World'}, {'1': 'World', '2': 'Hello'}]
        return render_template('dashboard.html',totexp = y,columns=['EXPENSE', 'EXPENSE_DETAIL'], items=items_list)
    else:
        flash("user not logged in")
        return redirect(url_for("login"))

# add expense
@app.route('/dashboard', methods=['POST','GET'])
def addexpense():
    if request.method == 'POST':
        usr = session['user']
        ur = ibm_db.exec_immediate(conn,"SELECT user_id FROM USERS where username = ('{}')".format(usr))
        uid = ibm_db.fetch_tuple(ur)
        for i in uid:
            x = int(i)
        try:
            curr1 = "INSERT INTO EXPENSES (user_id,expense,expense_detail) VALUES('{}','{}','{}')".format(x, request.form["expense"],  request.form["details"])
            curx = ibm_db.exec_immediate(conn,curr1)
        except Exception as ee:
            print(ee)
        return redirect(url_for('dash'))

# logout
@app.route('/logout')
def logout():
    session.pop("user", None)
    flash("logout successfull")
    return redirect(url_for('login'))

if __name__ =="__main__":
    app.run(debug=True)