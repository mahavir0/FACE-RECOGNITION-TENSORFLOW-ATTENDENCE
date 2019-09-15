import find_faces
import cv2
import sys
import sqlite3
import csv
import json
import pandas as pd  
from sklearn import svm
from sklearn.externals import joblib
from PIL import Image,ImageDraw,ImageFont
import time
from identify_face_video import face_video
from identify_face_image import face_image
from sql import *
	
def convert_date(string):
	if string.find("-")!=-1:
	 	temp = string.split('-')
	 	x = str(temp[2])+"_"+str(temp[1])+"_"+str(temp[0])
	 	return x
	return string

def take_attendence(date, filename, courseId):

	#Call function from identify_face_video.py
	found_ids = face_video(filename)
	print("i found array: ",found_ids)
	print(date)
	print(found_ids)

	processAttendance(date, courseId, found_ids)
	
	return found_ids

def take_attendence_image(date, filename, courseId):

	#Call function from identify_face_image.py
	found_ids = face_image(filename)
	print("i found array: ",found_ids)
	print(date)
	print(found_ids)

	processAttendance(date, courseId, found_ids)

	return found_ids
