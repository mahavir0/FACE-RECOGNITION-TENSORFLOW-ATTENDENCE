import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="hackathon19"
)


mycursor = mydb.cursor()

def getEmail():
    sql = "SELECT enrollmentNo, email FROM student_tbl order by enrollmentNo" 
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    
    emails = {}
    for i in myresult:
        emails[i[0]] = i[1]
    print(emails)
    return emails

def addFaculty(facultyId, facultyName, email, dept, mobile, password):
    sql = "INSERT INTO faculty_login_tbl (facultyId, password) VALUES (%s, %s)"
    val = (facultyId, password)
    mycursor.execute(sql, val)
    mydb.commit()
    sql = "INSERT INTO faculty_tbl (facultyId, facultyName, email, dept, mobile) VALUES (%s, %s, %s, %s, %s)"
    val = (facultyId, facultyName, email, dept, mobile)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, " faculty added.")
    return True

def addStudent(enrollmentNo, studentName, mobile, email):
    sql = "INSERT INTO student_tbl (enrollmentNo, studentName, mobile, email) VALUES (%s, %s, %s, %s)"
    val = (enrollmentNo, studentName, mobile, email)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, " student added.")

def addCourse(courseId, courseName):
    sql = "INSERT INTO course_tbl (courseId, courseName) VALUES (%s, %s)"
    val = (courseId, courseName)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, " course added.")

def addCourseStudent(courseId, enrollmentNo):
    sql = "INSERT INTO student_course_tbl (courseId, enrollmentNo) VALUES (%s, %s)"
    val = (courseId, enrollmentNo )
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, " course added.")

def getFaculty(facultyId, password):
    sql = "SELECT * FROM faculty_login_tbl WHERE facultyId ='"+facultyId+"' and password='"+password+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if len(myresult)>0:
        return True
    else:
        return False

def getCourses():
    sql = "SELECT courseId FROM course_tbl "
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    courses = []
    for course in myresult:
    	courses.append(course[0])
    return courses

def getStudentForCourse():
    sql = "SELECT enrollmentNo FROM student_tbl order by enrollmentNo"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    ids = []
    for id in myresult:
    	ids.append(id[0])
    return ids

def processAttendance(date, courseId, enrollmentNo):
    sql = "SELECT enrollmentNo FROM student_course_tbl WHERE courseId ='"+courseId+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    
    print("here")
    print(enrollmentNo)

    for student in myresult:
        print(student[0])
        if str(student[0]) in enrollmentNo:
            sql = "INSERT INTO attendance_tbl (date, courseId, enrollmentNo, status) VALUES (%s, %s, %s, %s)"
            val = (date, courseId, str(student[0]), "PRESENT" )
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, " attendance marked <PRESENT>.")
        else:
            sql = "INSERT INTO attendance_tbl (date, courseId, enrollmentNo, status) VALUES (%s, %s, %s, %s)"
            val = (date, courseId, str(student[0]), "ABSENT" )
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, " attendance marked <ABSENT>.")

# attendance by course and month
def getAttandanceByCourseMonth(courseId, month):
    monthfor = "____-"+month+"-__"
    print(monthfor)
    sql = "SELECT count(enrollmentNo), enrollmentNo FROM attendance_tbl WHERE courseId ='"+courseId+"' and date like '"+monthfor+"' group by enrollmentNo"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    return myresult


# attendance by course enrolment and month
def getAttandanceByCourseEnrollmentMonth(courseId, enrollmentNo, month):
    monthfor = "____-"+month+"-__"
    print(monthfor)
    sql = "SELECT date, status FROM attendance_tbl WHERE courseId ='"+courseId+"' and date like '"+monthfor+"' and enrollmentNo ="+str(enrollmentNo)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    attendance = []
    for entry in myresult:
        attendance.append([entry[0].isoformat(), entry[1]])
    print(attendance)
    return {attendance: attendance}

# attendance by enrollment and month
def getAttandanceByEnrollmentMonth(enrollmentNo, month):
    monthfor = "____-"+month+"-__"
    print(monthfor)
    sql = "SELECT date, status, courseId FROM attendance_tbl WHERE date like '"+monthfor+"' and enrollmentNo ="+str(enrollmentNo)+" order by date, courseId"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    attendance = {}
    date = []
    for entry in myresult:
        if entry[0].isoformat() not in date:
            attendance[entry[0].isoformat()] = {}
        attendance[entry[0].isoformat()][entry[2]] = entry[1]
    print(attendance)
    return {attendance: attendance}

# attendance by enrolment and month
def getAttandanceByEnrollmentDate(enrollmentNo, date):
    sql = "SELECT date, status, courseId FROM attendance_tbl WHERE date like '"+date+"' and enrollmentNo ="+str(enrollmentNo)+" order by courseId"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    attendance = {}
    date = []
    for entry in myresult:
        if entry[0].isoformat() not in date:
            attendance[entry[0].isoformat()] = {}
        attendance[entry[0].isoformat()][entry[2]] = entry[1]
    print(attendance)
    return {attendance: attendance}

def getAttandanceByMonth(month):
    monthfor = "____-"+month+"-__"
    print(monthfor)
    sql = "SELECT date, enrollmentNo, status, courseId FROM attendance_tbl WHERE date like '"+monthfor+"' order by courseId, date , enrollmentNo"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    attendance = {}
    date = []
    course = []
    for entry in myresult:
        if entry[3] not in course:
            course.append(entry[3])
            attendance[entry[3]] = {}
            date = []
        if entry[0].isoformat() not in date:
            date.append(entry[0].isoformat())
            attendance[entry[3]][entry[0].isoformat()] = []
        
        attendance[entry[3]][entry[0].isoformat()].append([entry[1], entry[2]])
    print(attendance)
    return attendance


# attendance by course date
def getAttandanceByCourseDate(courseId, date):
    print(date)
    sql = "SELECT enrollmentNo, status FROM attendance_tbl WHERE courseId ='"+courseId+"' and date like '"+date+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    students = []
    for stu in myresult:
        students.append(stu[0])
    print(students)
    return {students: students}

# attendance by course 
def getAttandanceByCourse(courseId):
    sql = "SELECT enrollmentNo, date, status FROM attendance_tbl WHERE courseId ='"+courseId+"' order by enrollmentNo, date"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    attendance = {}
    en = []
    for stu in myresult:
        if stu[0] not in en:
            en.append(stu[0])
            attendance[stu[0]] = {}
        attendance[stu[0]][stu[1].isoformat()] = stu[2]
    print(attendance)
    return attendance

# attendance by enrollment
def getAttandanceByEnrollment(enrollmentNo):
    sql = "SELECT courseId, date, status FROM attendance_tbl WHERE enrollmentNo ='"+str(enrollmentNo)+"' order by courseId, date"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    attendance = {}
    course = []
    for stu in myresult:
        if stu[0] not in course:
            course.append(stu[0])
            attendance[stu[0]] = {}
        attendance[stu[0]][stu[1].isoformat()] = stu[2]
    print(attendance)
    return attendance

# attendance by date
def getAttandanceByDate(date):
    sql = "SELECT courseId, enrollmentNo, status FROM attendance_tbl WHERE date like '"+date+"' order by courseId, enrollmentNo"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    attendance = {}
    course = []
    for stu in myresult:
        if stu[0] not in course:
            course.append(stu[0])
            attendance[stu[0]] = {}
        attendance[stu[0]][stu[1]] = stu[2]
    print(attendance)
    return attendance

def getAjaxCall(enrollmentNo = None, month=None, date=None, courseId =None):
    sql = ''
    if(enrollmentNo==None and month ==None and date==None and courseId==None):
        sql = "SELECT courseId, enrollmentNo, date, status FROM attendance_tbl"
    else:
        sql = "SELECT courseId, enrollmentNo, date, status FROM attendance_tbl WHERE"
        if(enrollmentNo!=None):
            sql = sql + " enrollmentNo like "+str(enrollmentNo)
            if(month!=None):
                sql = sql + " and date like '____-"+month+"-__'"
                if(date!=None):
                    sql = sql + " and date like '"+date+"'"
                    if(courseId!=None):
                        sql = sql + " and courseId like '"+courseId+"'"
        elif(month!=None):
            sql = sql + " date = '____-"+month+"-__'"
            if(date!=None):
                sql = sql + " and date like '"+date+"'"
                if(courseId!=None):
                    sql = sql + " and courseId like '"+courseId+"'"
        elif(date!=None):
            sql = sql + " date like '"+date+"'"
            if(courseId!=None):
                sql = sql + " and courseId like '"+courseId+"'"
        elif(courseId!=None):
            sql = sql + " courseId like '"+courseId+"'"
    print(sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    print(list(myresult))
    final =[]
    for x in myresult:
        x=list(x)
        x[2]=x[2].isoformat()
        final.append(x)
    print(final)
    return final
    

#addFaculty(337, "Trushar", "tppatel5798.gmail.com", "IT", 9876543210, "123456")
#addAttendance("2018-04-06", "2150704", [170010116026])
#getAttandanceByCourseMonth("2150704", '04')
#getAttandanceByCourseDate("2150704", '2019-04-18')
#getAttandanceByCourseEnrollmentMonth("2150704", 170010116026, '04')
#getAttandanceByMonth('04')

#getAttandanceByEnrollmentMonth(170010116026, '04')
#getAttandanceByEnrollmentDate(170010116026, '2019-04-18')
#getAttandanceByCourse('2150704')
#getAttandanceByEnrollment(170010116026)
#getAttandanceByDate('2019-04-25')
#getAjaxCall(enrollmentNo="170010116026")