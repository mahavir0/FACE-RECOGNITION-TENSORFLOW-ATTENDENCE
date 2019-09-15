from flask import Flask, render_template,request,redirect,url_for,flash
from flask_responses.responses import json_response
from flask import jsonify
import os
from werkzeug import secure_filename
import sqlite3
from create_student import add
from run_faces import take_attendence
from run_faces import take_attendence_image
from add_courses import add_cou
from add_student_courses import add_s_courses
import json
import plotly
import pandas as pd
from passlib.hash import sha256_crypt
from sql import *
#from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['logged_in']=False
#app.wsgi_app = ProxyFix(app.wsgi_app)

UPLOAD_FOLDER_IMAGE = 'Image'
app.config['UPLOAD_FOLDER_IMAGE'] = UPLOAD_FOLDER_IMAGE

UPLOAD_FOLDER_VIDEO = 'Video'
app.config['UPLOAD_FOLDER_VIDEO'] = UPLOAD_FOLDER_VIDEO

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/home', methods=['GET','POST'])
def home(name=None):
	courses = getCourses()
	ids = getStudentForCourse()
	return render_template('index.html', courses=courses, ids=ids)

@app.route('/details', methods=['GET','POST'])
def details(name=None):
	courses = getCourses()
	ids = getStudentForCourse()
	return render_template('details.html', courses=courses, ids=ids)

@app.route('/', methods=['GET','POST'])
def login(name=None):
	if request.method=='GET':
		return render_template('login.html')
	else:
		facultyId = str(request.form['facultyId'])
		password = str(request.form['password'])
		login = getFaculty(facultyId, password)
		if login == True:
			return redirect(url_for('home'))
		else:
			return redirect(url_for('login'))

@app.route('/signup', methods=['GET','POST'])
def signup(name=None):
	if request.method=='GET':
		return render_template('signup.html')
	else:
		facultyId = str(request.form['facultyId'])
		facultyName = str(request.form['facultyName'])
		email = str(request.form['email'])
		dept = str(request.form['dept'])
		mobile = str(request.form['mobile'])
		password = str(request.form['password'])

		add = addFaculty(facultyId, facultyName, email, dept, mobile, password )

		if add == True:
			return redirect(url_for('login'))
		else:
			return redirect(url_for('signup'))

@app.route('/addStudentBack', methods=['GET','POST'])
def addStudentBack():
	if request.method=='POST':
		files = request.files.getlist('file[]')
		enrollmentNo = request.form['enrollmentNo']
		studentName = request.form['studentName']
		email = request.form['email']
		mobile = request.form['mobile']

		directory = './train_img/'+str(enrollmentNo)
		os.makedirs(directory)
		filecount = 0
		for file in files:
			filecount+=1
			filename = secure_filename(request.form['enrollmentNo']+str(filecount)+'.'+file.filename.rsplit('.', 1)[1].lower())
			print(filename)
			file.save(os.path.join(directory, filename))
		addStudent(enrollmentNo, studentName, mobile, email)
		return redirect(url_for('home'))
	else: 
		return redirect(url_for('home'))

@app.route('/addCourseBack', methods=['GET','POST'])
def addCourseBack():
	if request.method=='POST':
		courseId = request.form['courseId']
		courseName = request.form['courseName']

		addCourse(courseId, courseName)
		return redirect(url_for('home'))
	else: 
		return redirect(url_for('home'))

@app.route('/addStudentCourseBack', methods=['GET','POST'])
def addStudentCourseBack():
	if request.method=='POST':
		courseId = request.form['courseId']
		enrollmentNo = request.form['enrollmentNo']

		addCourseStudent(courseId, enrollmentNo)
		return redirect(url_for('home'))
	else: 
		return redirect(url_for('home'))

@app.route('/processVideo', methods=['GET','POST'])
def processVideo():
	if request.method=='POST':
		file = request.files['file']
		if file:
			print(file.filename)
		date = str(request.form['date'])
		courseId = str(request.form['courseId'])
		filename = secure_filename(date+'.'+file.filename.split('.')[-1].lower())
		file.save(os.path.join(app.config['UPLOAD_FOLDER_VIDEO'], filename))
		filename = os.path.join(app.config['UPLOAD_FOLDER_VIDEO'], filename)
		found_ids = take_attendence(date,filename,courseId)

		return redirect(url_for('json12',found=found_ids))
	else: 
		return redirect(url_for('home'))

@app.route('/processImage', methods=['GET','POST'])
def processImage():
	if request.method=='POST':
		print(request.files)
		file = request.files['file']
		if file:
			print(file.filename)
		date = str(request.form['date'])
		courseId = str(request.form['courseId'])
		filename = secure_filename(date+'.'+file.filename.split('.')[-1].lower())
		file.save(os.path.join(app.config['UPLOAD_FOLDER_IMAGE'], filename))
		filename = os.path.join(app.config['UPLOAD_FOLDER_IMAGE'], filename)
		found_ids = take_attendence_image(date,filename,courseId)

		return redirect(url_for('json12',found=found_ids))
	else: 
		return redirect(url_for('home'))

@app.route('/attendenceByMonth/<month>', methods=['GET','POST'])
def attendenceByMonth(month=None):
	attendence = getAttandanceByMonth(month)
	print("asda")
	print(attendence)
	return render_template('attendencebymonth.html', attendence=attendence)

@app.route('/attendenceByDate/<date>', methods=['GET','POST'])
def attendenceByDate(date=None):
	attendence = getAttandanceByDate(date)
	print("asda")
	print(attendence)
	return render_template('attendencebydate.html', attendence=attendence)

@app.route('/attendenceByCourse/<course>', methods=['GET','POST'])
def attendenceByCourse(course=None):
	attendence = getAttandanceByCourse(course)
	print("asda")
	print(attendence)
	return render_template('attendencebycourse.html', attendence=attendence)

@app.route('/attendenceByEnrollment/<enrollment>', methods=['GET','POST'])
def attendenceByEnrollment(enrollment=None):
	attendence = getAttandanceByEnrollment(enrollment)
	print("asda")
	print(attendence)
	return render_template('attendencebyenrollment.html', attendence=attendence)

@app.route('/attendenceByCourseDate/<course>/<date>', methods=['GET','POST'])
def attendenceByCourseDate(course=None, date=None):
	attendence = getAttandanceByCourseDate(course,date)
	print("asda")
	print(attendence)
	return render_template('attendencebycoursedate.html', attendence=attendence)

@app.route('/attendenceByCourseMonth/<course>/<month>', methods=['GET','POST'])
def attendenceByCourseMonth(course=None, month=None):
	attendence = getAttandanceByCourseMonth(course,month)
	print("asda")
	print(attendence)
	return render_template('attendencebycoursemonth.html', attendence=attendence)

@app.route('/attendenceByEnrollmentMonth/<enrollment>/<month>', methods=['GET','POST'])
def attendenceByEnrollmentMonth(enrollment=None, month=None):
	attendence = getAttandanceByEnrollmentMonth(enrollment,month)
	print("asda")
	print(attendence)
	return render_template('attendencebyenrollmentmonth.html', attendence=attendence)

@app.route('/attendenceByEnrollmentDate/<enrollment>/<date>', methods=['GET','POST'])
def attendenceByEnrollmentDate(enrollment=None, date=None):
	attendence = getAttandanceByEnrollmentDate(enrollment,date)
	print("asda")
	print(attendence)
	return render_template('attendencebyenrollmentdate.html', attendence=attendence)

@app.route('/attendenceByCourseEnrollmentMonth/<course>/<enrollment>/<month>', methods=['GET','POST'])
def attendenceByCourseEnrollmentMonth(course=None, enrollment=None, month=None):
	attendence = getAttandanceByCourseEnrollmentMonth(course,enrollment,month)
	print("asda")
	print(attendence)
	return render_template('attendencebycourseenrollmentmonth.html', attendence=attendence)

@app.route('/json/<found>', methods=['GET','POST'])
def json12(found=None):
    return json_response({'found_ids': found}, status_code=200)

@app.route('/mail', methods=['GET','POST'])
def mail():
	import smtplib
	print("Start")

	# list of email_id to send the mail
	li = getEmail()
	message = ''
	for i in li:
		x = getAttandanceByEnrollment(i)
		message = message + '\n' + str(i) + '\n'
		for y in x:
			message = message + '\n' + str(y) + '\n'
			for z in x[y]:
				message = message + z +' - '+ x[y][z] + '\n'
		print(message)
		# creates SMTP session
		print("enter")
		s = smtplib.SMTP('smtp.gmail.com', 587)
		# start TLS for security
		s.starttls()
		# Authentication
		s.login("mahavirpatel0@gmail.com", "nikhilpatel")
		# message to be sent
		print("Message sent")
		# sending the mail
		s.sendmail("mahavirpatel0@gmail.com", li[i], message)
		message = ''
		# terminating the session
		print("Exit")
		s.quit()
	return redirect(url_for('home'))

@app.route('/ajax/<enrollmentNo>/<month>/<date>/<courseId>', methods=['GET','POST'])
def ajax(enrollmentNo=None, month=None,date=None, courseId=None):
	myresult = getAjaxCall(enrollmentNo=enrollmentNo,month=month,date=date, courseId=courseId)
	return jsonify({"result": myresult})

if __name__ == '__main__':
	app.config['logged_in']=False
	app.run(debug=False,host="192.168.137.1",port="5000")
