from flask import Flask, render_template, url_for, request,redirect, make_response, flash
from dbconnect import connection
import MySQLdb
import json
import numpy as np
from forms import RegistrationForm, LoginForm
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = '24a92cbc4352146a46e0c61b51a13dca'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@app.route("/")
@app.route("/home", methods = ['GET','POST'])
def home():
    if(request.method == 'POST'):
        details = request.form
        semester_id = details['semesterId']
        print(semester_id)
        return redirect('/timetable/'+semester_id)
    db, cursor = connection()
    cursor.execute('''SELECT * FROM collegeEntry''')
    colleges = cursor.fetchall()
    db.close()
    return render_template('home.html', colleges=colleges)


@app.route("/course/<int:college_id>/", methods=["GET"])
def get_course(college_id):
    db, cursor = connection()
    cursor.execute('''SELECT * FROM courseEntry WHERE collegeID = %s''',(college_id,))
    courses = cursor.fetchall()
    data = [(x[0], x[1], x[2]) for x in courses]
    print(data)
    db.close()
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    print (response)
    return response

@app.route("/branch/<int:course_id>/", methods=["GET"])
def get_branch(course_id):
    db, cursor = connection()
    cursor.execute('''SELECT * FROM branchEntry WHERE courseID = %s''',(course_id,))
    courses = cursor.fetchall()
    data = [(x[0], x[1], x[2]) for x in courses]
    print(data)
    db.close()
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    print (response)
    return response


@app.route("/semester/<int:branch_id>/", methods=["GET"])
def get_semester(branch_id):
    db, cursor = connection()
    cursor.execute('''SELECT * FROM semesterEntry WHERE branchID = %s''',(branch_id,))
    semesters = cursor.fetchall()
    data = [(x[0], x[1], x[2]) for x in semesters]
    print(data)
    db.close()
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    print (response)
    return response

@app.route("/timetable/<int:semester_id>/", methods = ['GET','POST'])
def timetable(semester_id):
    db, cursor = connection()
    cursor.execute('''SELECT * FROM dayEntry WHERE semesterID = %s''',(semester_id,))
    days = cursor.fetchall()
    data = [(x[0],x[1],x[2]) for x in days]
    days=[]
    for x in data:
        id=x[0]
        cursor.execute('''SELECT * FROM tableEntry WHERE dayID = %s''',(id,))
        table = cursor.fetchall()
        days.append([(x[0],x[1],x[2],x[3],x[4],x[5]) for x in table])
    
    print(days)
    days = list(map(list, zip(*days)))
    # days = [[row[i] for row in days] for i in range(len(days[0]))]
    print(" ")
    print(days)    
    db.close()
    return render_template('timetable.html', id=semester_id,tables=days)


@app.route("/select/<string:name>/<int:uid>",methods = ['GET','POST'])
def select(name,uid):
    if(name=='college'):
        if(request.method == 'POST'):
            details = request.form
            college = details['collegeName']
            course = details['courseName']
            branch = details['branchName']
            semester = details['semester']
             

            db, cursor = connection()
            cursor.execute('''INSERT INTO collegeEntry(collegeName) values(%s)''',(college,))
            id = cursor.lastrowid
            cursor.execute('''INSERT INTO courseEntry(collegeID, courseName) values(%s, %s)''' ,(int(id),course))
            id = cursor.lastrowid
            cursor.execute('''INSERT INTO branchEntry(courseID, branchName) values(%s, %s)''' ,(int(id),branch))
            id = cursor.lastrowid
            cursor.execute('''INSERT INTO semesterEntry(branchID, semesterName) values(%s, %s)''' ,(int(id),semester))
            semid = cursor.lastrowid
            for days in ['Monday','Tuesday','Wednesday','Thursday','Friday']: 
                cursor.execute('''INSERT INTO dayEntry(semesterID, dayName) values(%s, %s)''' ,(int(semid),days))
                id = cursor.lastrowid
                for i in range(10):
                    dayStart=details[days+'/starttime/'+str(i)]
                    dayEnd=details[days+'/endtime/'+str(i)]
                    subject=details[days+'/subject/'+str(i)]
                    roomNo=details[days+'/roomno/'+str(i)]
                    cursor.execute('''INSERT INTO tableEntry(dayID, subject, dayStart, dayEnd, roomNo) values(%s, %s, %s, %s, %s)''' ,(int(id),subject,dayStart,dayEnd,roomNo))
            db.commit()
            db.close()
            return redirect('/')
        

    elif(name=='course'):
        if(request.method == 'POST'):
            details = request.form
            course = details['courseName']
            branch = details['branchName']
            semester = details['semester']
            db, cursor = connection()
            id=uid
            cursor.execute('''INSERT INTO courseEntry(collegeID, courseName) values(%s, %s)''' ,(int(id),course))
            id = cursor.lastrowid
            cursor.execute('''INSERT INTO branchEntry(courseID, branchName) values(%s, %s)''' ,(int(id),branch))
            id = cursor.lastrowid
            cursor.execute('''INSERT INTO semesterEntry(branchID, semesterName) values(%s, %s)''' ,(int(id),semester))
            semid = cursor.lastrowid
            for days in ['Monday','Tuesday','Wednesday','Thursday','Friday']: 
                cursor.execute('''INSERT INTO dayEntry(semesterID, dayName) values(%s, %s)''' ,(int(semid),days))
                id = cursor.lastrowid
                for i in range(10):
                    dayStart=details[days+'/starttime/'+str(i)]
                    dayEnd=details[days+'/endtime/'+str(i)]
                    subject=details[days+'/subject/'+str(i)]
                    roomNo=details[days+'/roomno/'+str(i)]
                    cursor.execute('''INSERT INTO tableEntry(dayID, subject, dayStart, dayEnd, roomNo) values(%s, %s, %s, %s, %s)''' ,(int(id),subject,dayStart,dayEnd,roomNo))
            db.commit()
            db.close()
            return redirect('/')
        db, cursor = connection()
        cursor.execute('''SELECT * FROM collegeEntry WHERE collegeID = %s''',(uid,))
        colleges=cursor.fetchone()
        collegeName = colleges[1]
        db.close()
        return render_template('select.html',collegeName=collegeName)

    elif(name=='branch'):
        if(request.method == 'POST'):
            details = request.form
            branch = details['branchName']
            semester = details['semester']
            db, cursor = connection()
            id=uid
            cursor.execute('''INSERT INTO branchEntry(courseID, branchName) values(%s, %s)''' ,(int(id),branch))
            id = cursor.lastrowid
            cursor.execute('''INSERT INTO semesterEntry(branchID, semesterName) values(%s, %s)''' ,(int(id),semester))
            semid = cursor.lastrowid
            for days in ['Monday','Tuesday','Wednesday','Thursday','Friday']: 
                cursor.execute('''INSERT INTO dayEntry(semesterID, dayName) values(%s, %s)''' ,(int(semid),days))
                id = cursor.lastrowid
                for i in range(10):
                    dayStart=details[days+'/starttime/'+str(i)]
                    dayEnd=details[days+'/endtime/'+str(i)]
                    subject=details[days+'/subject/'+str(i)]
                    roomNo=details[days+'/roomno/'+str(i)]
                    cursor.execute('''INSERT INTO tableEntry(dayID, subject, dayStart, dayEnd, roomNo) values(%s, %s, %s, %s, %s)''' ,(int(id),subject,dayStart,dayEnd,roomNo))
            db.commit()
            db.close()
            return redirect('/')
        db, cursor = connection()
        cursor.execute('''SELECT * FROM courseEntry WHERE courseID = %s''',(uid,))
        courses=cursor.fetchone()
        courseName = courses[2]
        cursor.execute('''SELECT * FROM collegeEntry WHERE collegeID = %s''',(courses[1],))
        colleges=cursor.fetchone()
        collegeName = colleges[1]
        db.close()
        return render_template('select.html',collegeName=collegeName,courseName=courseName)

    elif(name=='semester'):
        if(request.method == 'POST'):
            details = request.form
            semester = details['semester']
            db, cursor = connection()
            id=uid
            cursor.execute('''INSERT INTO semesterEntry(branchID, semesterName) values(%s, %s)''' ,(int(id),semester))
            semid = cursor.lastrowid
            for days in ['Monday','Tuesday','Wednesday','Thursday','Friday']: 
                cursor.execute('''INSERT INTO dayEntry(semesterID, dayName) values(%s, %s)''' ,(int(semid),days))
                id = cursor.lastrowid
                for i in range(10):
                    dayStart=details[days+'/starttime/'+str(i)]
                    dayEnd=details[days+'/endtime/'+str(i)]
                    subject=details[days+'/subject/'+str(i)]
                    roomNo=details[days+'/roomno/'+str(i)]
                    cursor.execute('''INSERT INTO tableEntry(dayID, subject, dayStart, dayEnd, roomNo) values(%s, %s, %s, %s, %s)''' ,(int(id),subject,dayStart,dayEnd,roomNo))
            db.commit()
            db.close()
            return redirect('/')
        db, cursor = connection()
        cursor.execute('''SELECT * FROM branchEntry WHERE branchID = %s''',(uid,))
        branches=cursor.fetchone()
        branchName = branches[2]
        cursor.execute('''SELECT * FROM courseEntry WHERE courseID = %s''',(branches[1],))
        courses=cursor.fetchone()
        courseName = courses[2]
        cursor.execute('''SELECT * FROM collegeEntry WHERE collegeID = %s''',(courses[1],))
        colleges=cursor.fetchone()
        collegeName = colleges[1]
        db.close()
        return render_template('select.html',collegeName=collegeName,courseName=courseName,branchName=branchName)

    return render_template('select.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if(form.validate_on_submit() and request.method == 'POST'):
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db, cursor = connection()
        x=cursor.execute('''SELECT * FROM users WHERE username = %s''',(username,))
        if(int(x)>0):
            flash("Username already exists")
            return render_template('register.html', title='Register', form=form)
        else:
            cursor.execute('''INSERT INTO users(username, password, email) values(%s, %s, %s)''' ,(username, password, email))
            db.commit()
            db.close()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@login_manager.user_loader
def load_user(userID):
    db, cursor = connection()
    cursor.execute('''SELECT * FROM users WHERE userID = %s''',(int(userID),))
    users = cursor.fetchone()
    id= users[0]
    username = users[1]
    email = users[2]
    password = users[3]
    user = User(id,username,email,password)
    db.close()
    return user

class User(UserMixin):
    id = 1
    username = ''
    email = ''
    password = ''
    def __init__(self,id,username,email,password):
        self.id=id
        self.username=username
        self.email=email
        self.password=password

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


@app.route("/login", methods=['GET', 'POST'])
def login():
    if (current_user.is_authenticated):
        return redirect(url_for('home'))
    form = LoginForm()
    if(form.validate_on_submit() and request.method == 'POST'):
        email = form.email.data
        db, cursor = connection()
        cursor.execute('''SELECT * FROM users WHERE email = %s''',(email,))
        users = cursor.fetchone()
        id= users[0]
        username = users[1]
        email = users[2]
        password = users[3]
        user = User(id,username,email,password)
        if(bcrypt.check_password_hash(password, form.password.data)):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/about")
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)