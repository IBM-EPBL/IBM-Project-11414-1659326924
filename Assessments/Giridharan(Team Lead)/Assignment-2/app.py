from multiprocessing import connection
from multiprocessing.sharedctypes import Value
from unittest import result
from urllib import request
from flask import Flask,request,jsonify,render_template,flash,session,redirect
import ibm_db

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key="abc123giri"

def dbconn():
    conn = None
    try:
        conn = ibm_db.pconnect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;\
            PORT=31498;PROTOCOL=TCPIP;UID=xgm40296;PWD=89gtA0GUu8Dxxjxa;SECURITY=SSL;SSLServiceCertificate=DigiCertGlobalRootCA.crt", "", "")
    except ibm_db.conn_error as e:
        print(e)
    return conn

conn = dbconn()

@app.route('/')
def girifun():
    return "Shyam : hello World"

@app.route('/login', methods=['POST', 'GET'])
def loginn():
    conn = dbconn()
    if request.method == 'POST':
        if request.form['btn'] == 'Register':
            new_email = request.form['email']
            new_username = request.form['username']
            new_rollno = request.form['rollno']
            new_password = request.form['pass']
            try:
                curr1 = "INSERT INTO USERS (email,username,rollnumber,pass) VALUES('{}','{}','{}','{}')".format(request.form["email"], request.form["username"], request.form["rollno"], request.form["pass"])
                ibm_db.exec_immediate(conn,curr1)
            except Exception as ee:
                print(ee)
                flash("username already exists!!!")
                return render_template("index.html")
            curr2 = "SELECT * FROM USERS WHERE username = ('{}')".format(new_username,)
            cur2e = ibm_db.exec_immediate(conn,curr2)
            cur2ex = ibm_db.fetch_tuple(cur2e)
            books = dict(id=cur2ex[0], email=cur2ex[1], username=cur2ex[2], rollno=cur2ex[3], password=cur2ex[4] )
            return render_template('reg.html',result=books,value=books["username"]), 201
        if request.form['btn'] == 'Log In':
            cursorr = ibm_db.exec_immediate(conn,"SELECT * FROM USERS where username = ('{}')".format(request.form['username1']))
            currex = ibm_db.fetch_tuple(cursorr)
            if currex[2] == request.form['username1']:
                if currex[4] == request.form['pass1']:
                    return render_template('welcom.html', result=currex[4])
                else:
                    print(currex)
                    return "password incorrect go back"
            return render_template("index.html")
    if request.method == 'GET':
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)