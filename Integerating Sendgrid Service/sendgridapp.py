from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# mail
try:
    sg = SendGridAPIClient('Your API key')
except Exception as e:
    print(e)


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
        curbud = ibm_db.exec_immediate(conn,"SELECT budget FROM USERS where user_id = ('{}')".format(x))
        budexp = ibm_db.fetch_tuple(curbud)
        for z in budexp:
            budget = int(z)
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
