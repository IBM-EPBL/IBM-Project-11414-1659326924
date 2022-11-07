from multiprocessing.sharedctypes import Value
from unittest import result
from urllib import request
from flask import Flask,request,jsonify,render_template

app = Flask(__name__)

user_list = [
    {
        "id":0,
        "email":"giri123@gmail.com",
        "username":"giri627",
        "rollno":221,
        "pass":"giri2001"
    }
]

@app.route('/')
def girifun():
    return "Giri : hello World"

@app.route('/login', methods=['POST', 'GET'])
def loginn():
    if request.method == 'POST':
        if request.form['btn'] == 'Register':
            new_email = request.form['email']
            new_username = request.form['username']
            new_rollno = request.form['rollno']
            new_password = request.form['pass']
            new_id = user_list[-1]['id']+1

            new_obj = {
                "id": new_id,
                "email": new_email,
                "username": new_username,
                "rollno": new_rollno,
                "pass": new_password
            }
            user_list.append(new_obj)
            return render_template('reg.html',result=new_obj,value=new_obj['username'])
        if request.form['btn'] == 'Log In':
            for usr in user_list:
                if usr['username'] == request.form['username1']:
                    if usr['pass'] == request.form['pass1']:
                        return render_template('welcom.html', result=usr['username'])
                    else:
                        return "password incorrect"
            return render_template("index.html")
    if request.method == 'GET':
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)