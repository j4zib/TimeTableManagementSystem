from flask import Flask, render_template, url_for, request,redirect, make_response
from dbconnect import connection
import MySQLdb
import json
app = Flask(__name__)



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
    # db, cursor = connection()
    # cursor.execute('''SELECT * FROM collegeEntry''')
    # colleges = cursor.fetchall()
    # db.close()
    print ("worked")
    return render_template('timetable.html', id=semester_id)


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


@app.route("/about")
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)