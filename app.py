import email
from flask import Flask,render_template,url_for,abort, redirect,request,flash , session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Enum
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from flask_mysqldb import MySQL
import MySQLdb
import MySQLdb.cursors
import re
import sqlite3
import enum
import os
from time import sleep
from werkzeug.utils import secure_filename
import json
import datetime
from werkzeug.utils import secure_filename
import json
# Import for Migrations
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, RadioField, SelectField, IntegerField
from passlib.hash import sha256_crypt

from datetime import datetime
from flask_migrate import Migrate, migrate

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'database'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#app.secret_key = 'your secret key'

#app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/database'
#app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

values = []
class AddTrainorForm(Form):
	fname = StringField('fname', [validators.Length(min = 1, max = 100)])
	email = StringField('email', [validators.InputRequired(), validators.NoneOf(values = values, message = "Username already taken, Please try another")])
	password = PasswordField('password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message = 'Passwords aren\'t matching pal!, check \'em')
	])
	confirm = PasswordField('Confirm Password')
	phone = StringField('Phone', [validators.Length(min = 1, max = 100)])


class gender(enum.Enum):
    female = 1
    male = 2
    other = 3

class department(enum.Enum):
    mech=0
    etc=1
    com=2
    it=3

class semester(enum.Enum):
    I=0
    II=1
    III=2
    IV=3
    V=4
    VI=5
    VII=6
    VIII=7

#  id = db.Column('student_id', db.Integer, primary_key = True)
#   fname = db.Column(db.String(100),nullable=False)
#   lname = db.Column(db.String(100),nullable=False)  
#   email = db.Column(db.String(100),nullable=False)
#   phone = db.Column(db.Integer,nullable=False)
#   eno = db.Column(db.Integer)
#   rno = db.Column(db.Integer)  
#   bdate = db.Column(db.DateTime)
#   gender = db.Column(db.Enum(gender))
#   department = db.Column(db.Enum(department))
#   semester = db.Column(db.Enum(semester)) 
#   password = db.Column(db.String(200),nullable=False)
#   cpassword = db.Column(db.String(200),nullable=False)

#def __repr__(self):
 #       return f"First Name : {self.fname}, Last Name : {self.lname},Last Name : {self.lname}, Email : {self.email}, Phone : {self.phone}, Enrollment No: {self.eno} ,Roll No : {self.rno} ,Birth Date : {self.bdate}, Gender : {self.gender}, Department : {self.department},Semester : {self.semester}, Create Password : {self.password}, Confirm Password : {self.cpassword}"

@app.route("/")
def home():
    return render_template('home.html')
	
@app.route("/About")
def about():
    return render_template('about.html')

@app.route("/contact_us")
def contact():
    return render_template('contact.html')
	
@app.route("/fauclty")
def FaucltyLogin():
    return render_template('Fauclty.html')

#@app.route("/student")
#def StudentLogin():
# if(request.method=='POST'):
#    email=request.form.get('email')
 #   password=request.form.get('password')
 #   q1="SELECT * FROM students NATURAL JOIN students WHERE email=%s AND password=%s"
 #return render_template('Student.html')

@app.route("/student/registration", methods = ['GET','POST'])
def studentsres():
        if(request.method=='POST'):
          fname = request.form.get('fname') 
          lname = request.form.get('lname')
          email = request.form.get('email')
          phone = request.form.get('phone')
          eno = request.form.get('eno')
          rno = request.form.get('rno')
          bdate = request.form.get('bdate')
          gender = request.form.get('gender')
          department = request.form.get('department')
          semester = request.form.get('semester')
          password = request.form.get('password')
          cpassword = request.form.get('cpassword')
          print("writing in DB")
        cursor=mysql.cursor()
        sql="INSERT INTO students VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(fname,lname,email,phone,eno,rno))
        mysql.commit()
        msg="Your Account Created Successfully"
        return render_template('StudentRes.html',msg=msg)
        mysql.close()
       # else:
        #  return "Problem in inserting data"

    #  pic1=request.files['pic1']
     # s = Students(fname=fname, lname=lname, email=email, phone=phone, eno=eno, rno=rno, bdate=bdate, gender=gender, department=department,semester=semester,password=password, cpassword=cpassword )
   # if fname != '' and lname != '' and email !='' and phone != '' and eno != '' and rno != '' and bdate is not None and gender is not None and department is not None and semester is not None and  password != '' :
    #else:
     # db.session.add(s)
     # db.session.commit()
     # fn1=secure_filename(pic1.filename)
     # pic1.save(os.path.join(app.config['UPLOAD_FOLDER'],fn1))
   #   msg= 'Registration was successfull, please login'
   # return render_template('StudentRes.html',msg=msg)

          

@app.route("/faculty/registration")
def FacultyRes():
    values.clear()
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT email FROM database")
    b = cur.fetchall()
    for i in range(q):
        values.append(b[i]['email'])
	#app.logger.info(b[0]['username'])
	#res = values.fetchall()
	#app.logger.info(res)
    cur.close()
    form = AddTrainorForm(request.form)
    if request.method == 'POST' and form.validate():
        fname = form.fname.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        phone = form.phone.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO database(fname, email, password, phone) VALUES( %s, %s, %s, %s)", (fname,email, password,phone))
        cur.execute("INSERT INTO students(email) VALUES(%s)", [email])
        mysql.connection.commit()
        cur.close()
        flash('You recruited a new Trainor!!', 'success')
        return redirect(url_for('StudentProfile.html')) 
    return render_template('FaucltyRes.html',form=form)

@app.route('/StudentLogin', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = db.connection.cursor(db.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return result
        students = cursor.fetchone()
        # If account exists in accounts table in out database
        if students:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['rno'] = students['rno']
            session['email'] = students['email']
            # Redirect to home page
            return render_template('StudentProfile.html', msg=msg)
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('Student.html', msg=msg)

@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


if __name__ == '__main__':
    app.debug = True
    app.run()