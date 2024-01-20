#app.py
from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import pymysql 
import re 
import MySQLdb
import MySQLdb.cursors
import enum
from datetime import datetime
 
app = Flask(__name__)
 
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'velip'
 
mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'database'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

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

@app.route("/")
def home():
    return render_template('home.html')
	
@app.route("/About")
def about():
    return render_template('about.html')

@app.route("/contact_us")
def contact():
    return render_template('contact.html')
	
@app.route("/faculty")
def FaucltyLogin():
    return render_template('Faculty.html')

@app.route('/StudentLogin', methods=['GET', 'POST'])
def login():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        Email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM student WHERE Email = %s AND password = %s', (Email, password))
        # Fetch one record and return result
        student = cursor.fetchone()
   
    # If account exists in accounts table in out database
        if student:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['Eno'] = student['Eno']
            session['Email'] = student['Email']
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('profile'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
    return render_template('Student.html', msg=msg)
 
@app.route('/join')
def join(): 
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM student WHERE Eno = %s', [session['Eno']])
        student = cursor.fetchone()
        # Show the profile page with account info
        return render_template('StudentJoin.html', student=student)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/StudentLogin/View', methods=['GET', 'POST'])
def View():
    # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:
        
        # User is loggedin show them the home page
        return render_template('studentatten.html', Email=session['Email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/student/registration', methods=['GET', 'POST'])
def register():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Fname' in request.form and 'Lname' in request.form and 'Email' in request.form and 'Pno' in request.form and 'Eno' in request.form and 'Rno' in request.form and 'Bdate' in request.form and 'Gender' in request.form and 'Department' in request.form and 'Semester' in request.form   and 'password' in request.form and 'Cpassword' in request.form:
        # Create variables for easy access
        Fname = request.form['Fname']
        Lname = request.form['Lname']
        Email = request.form['Email']
        Pno = request.form['Pno']
        Eno = request.form['Eno']
        Rno = request.form['Rno']
        Bdate = request.form['Bdate']
        Gender = request.form['Gender']
        Department = request.form['Department']
        Semester = request.form['Semester']
        password = request.form['password']
        Cpassword = request.form['Cpassword']
   
  #Check if account exists using MySQL
        cursor.execute('SELECT * FROM student WHERE Eno = %s', (Eno))
        student = cursor.fetchone()
        # If account exists show error and validation checks
        if student:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            msg = 'Invalid email address!'
        elif not Fname or not password or not Email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO student VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)', (Fname, Lname, Email, int(Pno), int(Eno), Rno, Bdate, Gender, Department, Semester, password, Cpassword))
            conn.commit()
   
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('StudentRes.html', msg=msg)

@app.route("/StutentLog")
def StudentLog():
    # Check if user is loggedin
    if 'loggedin' in session:
        
        # User is loggedin show them the home page
        return render_template('home.html', Email=session['Email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('eno', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/profile')
def profile(): 
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM student WHERE Eno = %s', [session['Eno']])
        student = cursor.fetchone()
        notice = cursor.fetchone()
        # Show the profile page with account info
        return render_template('StudentProfile.html', student=student,notice=notice)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
  
@app.route('/FacultyLogin', methods=['GET', 'POST'])
def Facultylogin():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Email' in request.form and 'Password' in request.form:
        # Create variables for easy access
        Email = request.form['Email']
        Password = request.form['Password']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM faculty WHERE Email = %s AND Password = %s', (Email, Password))
        # Fetch one record and return result
        faculty = cursor.fetchone()
   
    # If account exists in accounts table in out database
        if faculty:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['PNo'] = faculty['PNo']
            session['Email'] = faculty['Email']
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('Facultyprofile'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
    return render_template('Faculty.html', msg=msg)
 

@app.route('/faculty/registration', methods=['GET', 'POST'])
def facultyregister():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Fname' in request.form and 'Lname' in request.form and 'Email' in request.form and 'PNo' in request.form and 'Department' in request.form and 'Gender' in request.form  and 'Password' in request.form and 'Cpassword' in request.form:
        # Create variables for easy access
        Fname = request.form['Fname']
        Lname = request.form['Lname']
        Email = request.form['Email']
        PNo = request.form['PNo']
        Department = request.form['Department']
        Gender = request.form['Gender']
        Password = request.form['Password']
        Cpassword = request.form['Cpassword']
   
  #Check if account exists using MySQL
        cursor.execute('SELECT * FROM faculty WHERE Email = %s', (Email))
        faculty = cursor.fetchone()
        # If account exists show error and validation checks
        if faculty:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            msg = 'Invalid email address!'
        elif not Fname or not Password or not Email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO faculty VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)', (Fname, Lname, Email, int(PNo), Department, Gender, Password, Cpassword))
            conn.commit()
   
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('FacultyRes.html', msg=msg)

@app.route("/FacultyLog")
def FacultyLog():
    # Check if user is loggedin
    if 'loggedin' in session:
        
        # User is loggedin show them the home page
        return render_template('home.html', Email=session['Email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('Facultylogin'))

@app.route('/Facultylogout')
def Facultylogout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('PNo', None)
   session.pop('Email', None)
   # Redirect to login page
   return redirect(url_for('Facultylogin'))

@app.route('/Facultyprofile')
def Facultyprofile(): 
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM faculty WHERE PNo = %s', [session['PNo']])
        faculty = cursor.fetchone()
        # Show the profile page with account info
        return render_template('FacultyProfile.html', faculty=faculty)
    # User is not loggedin redirect to login page
    return redirect(url_for('Facultylogin'))

@app.route('/FacultyLogin/CreateLect')
def create(): 
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM faculty WHERE PNo = %s', [session['PNo']])
        faculty = cursor.fetchone()
        # Show the profile page with account info
        return render_template('TeacherLect.html', faculty=faculty)
    # User is not loggedin redirect to login page
    return redirect(url_for('Facultylogin'))

@app.route('/FacultyLogin/View', methods=['GET', 'POST'])
def facultyview():
    # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:
        
        # User is loggedin show them the home page
        return render_template('studentatten.html', Email=session['Email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('Facultylogin'))

@app.route('/FacultyLogin/Notice')
def notice(): 
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM faculty WHERE PNo = %s', [session['PNo']])
        faculty = cursor.fetchone()
        # Show the profile page with account info
        return render_template('Notice.html', faculty=faculty)
    # User is not loggedin redirect to login page
    return redirect(url_for('Facultylogin'))

@app.route('/message', methods=['GET', 'POST'])
def message():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'message' in request.form:
        message = request.form['message']
        cursor.execute('INSERT INTO notice VALUES (NULL, %s,%s)',(message,datetime.now()))
        conn.commit()
    return redirect(url_for('notice'))

if __name__ == '__main__':
  app.debug = True
  app.run()