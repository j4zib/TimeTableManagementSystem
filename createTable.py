import MySQLdb
from dbconnect import connection

db, cursor = connection()

cursor.execute('''drop table tableEntry''')
cursor.execute('''drop table dayEntry''')
cursor.execute('''drop table semesterEntry''')
cursor.execute('''drop table branchEntry''')
cursor.execute('''drop table courseEntry''')
cursor.execute('''drop table collegeEntry''')

cursor.execute('''CREATE TABLE collegeEntry(
    collegeID INT AUTO_INCREMENT PRIMARY KEY,
    collegeName VARCHAR(50))''')

cursor.execute('''CREATE TABLE courseEntry(
    courseID INT AUTO_INCREMENT PRIMARY KEY,
    collegeID INT,
    FOREIGN KEY(collegeID) REFERENCES collegeEntry(collegeID) ON DELETE CASCADE,
    courseName VARCHAR(50))''')

cursor.execute('''CREATE TABLE branchEntry(
    branchID INT AUTO_INCREMENT PRIMARY KEY,
    courseID INT,
    FOREIGN KEY(courseID) REFERENCES courseEntry(courseID) ON DELETE CASCADE,
    branchName VARCHAR(50))''')

cursor.execute('''CREATE TABLE semesterEntry(
    semesterID INT AUTO_INCREMENT PRIMARY KEY,
    branchID INT,
    FOREIGN KEY(branchID) REFERENCES branchEntry(branchID) ON DELETE CASCADE,
    semesterName VARCHAR(50))''')

cursor.execute('''CREATE TABLE dayEntry(
    dayID INT AUTO_INCREMENT PRIMARY KEY,
    semesterID INT,
    FOREIGN KEY(semesterID) REFERENCES semesterEntry(semesterID) ON DELETE CASCADE,
    dayName VARCHAR(50))''')

cursor.execute('''CREATE TABLE tableEntry(
    tableID INT AUTO_INCREMENT PRIMARY KEY,
    dayID INT,
    FOREIGN KEY(dayID) REFERENCES dayEntry(dayID) ON DELETE CASCADE,
    subject VARCHAR(50),
    dayStart VARCHAR(50),
    dayEnd VARCHAR(50),
    roomNo VARCHAR(50))''')

db.close()