from flask import Flask,flash,request,jsonify,json,redirect, render_template,url_for
import pymysql
import requests
from flask_cors import CORS

import os
#import magic
import urllib.request
# from app import app
from werkzeug.utils import secure_filename

import re
import string
import math
import json
import pickle
from sklearn import feature_extraction, model_selection, naive_bayes, metrics, svm
from spam_filter2 import SpamDetector,predict
import time
import threading



app=Flask(__name__)
CORS(app)

db=pymysql.connect('192.168.0.105','root','123','mailIt',cursorclass=pymysql.cursors.DictCursor)
cursor=db.cursor()

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#200-success #400-login failed.
@app.route("/login",methods=['POST'])
def login():
	email=request.form['email']
	password=request.form['password']
	print(email,password)
	sql="select * from user where email='%s' and password='%s';"%(email,password)
	if(cursor.execute(sql)>0):
		print("user and password matched")
		resp=jsonify()
		resp.status_code=200
		return resp
	else:
		resp=jsonify(["login-failed"])
		resp.status_code=400
		return resp

#function to get all the emails received by a user.
#200-success|400-failure
@app.route("/getData/<email>",methods=['GET'])
def getData(email):
	print(email)
	#query to extract all the emails received
	sql="select send_email,subject,body,date,spam,star from email where recv_email='%s'"%(str(email))
	cursor.execute(sql)
	rows=cursor.fetchall()
	resp=jsonify()
	message=[]
	if(len(rows)>0):
		for row in  rows:
			print(type(row),row)
			l=dict();
			l['send_email']=row['send_email']
			l['subject']=row['subject']
			l['body']=row['body']
			l['date']=row['date']
			l['spam']=row['spam']
			l['star']=row['star']
			message.append(l)
		resp.status_code=200
	else:
		resp.status_code=400
	resp=jsonify(message)
	return resp
	
	return resp

@app.route("/signup",methods=['POST','GET'])
def signup():
	if(request.method=="POST"):
		username=request.form['username']
		password=request.form["password"]
		email=request.form["email"]
		print(username,password,email)
		message={}
		resp=jsonify(message)
		resp.status_code=200
		return resp
	elif(request.method=="GET"):
		email=request.args["email"]
		sql="select * from user where email='%s'"%(email)
		resp=""
		if(cursor.execute(sql)>0):
			resp=jsonify({})
			resp.status_code=400
		else:
			resp=jsonify({})
			resp.status_code=200
		return resp

	else:
		pass

#send email
@app.route("/compose_send",methods=["POST"])
def compose_send():
	req_data=request.get_json()
	print(req_data)
	#genereating id 
	id_=0
	sql="select max(id) from email"
	if(cursor.execute(sql)>0):
		id_=int(cursor.fetchone()['max(id)'])+1
	sql="insert into email(id,send_email,recv_email,subject,body) values(%d,'%s','%s','%s','%s')"%(id_,req_data["send_email"],req_data["recv_email"],req_data["subject"],req_data["body"])
	if(cursor.execute(sql)>0):
		print("email sent")
	#inserting data into spam_log database  to be check for later
	sql="insert into spam_check_log values('%d')"%(id_)
	if(cursor.execute(sql)>0):
		print("emailed logged for further check")
	db.commit()
	resp=jsonify({})
	resp.status_code=200
	return resp


def spam_check():
	while(1):
		print("Spam check active")
		sql="select * from spam_check_log"
		if(cursor.execute(sql)>0):
			ids=list(cursor.fetchall()[0].values())
			sql="select id,subject,body from  email where id in (%s)"%(','.join(list(map(str,ids))))
			if(len(ids)>0 and cursor.execute(sql)>0):
				data=cursor.fetchall()
				data_list=list()
				#order of ids
				ids=list()
				for ele in data:
					#print(ele)
					ids.append(ele['id'])
					data_list.append("Subject:{}\n{}".format(ele["subject"],ele["body"]))

				#checking whether the mailes are spam or not.
				labels=predict(data_list)
				print("labels {}".format(labels))
				spam_id=[val for i,val in enumerate(ids) if labels[i]==1]
				sql="update email set spam=1 where id in ('%s')"%(','.join(list(map(str,spam_id))))
				if(cursor.execute(sql)>0):
					print("spam set")
				db.commit()
				
				#deleting entires from  spma_check_log file
				sql="delete from spam_check_log where id in ('%s')"%(','.join(list(map(str,spam_id))))
				if(cursor.execute(sql)>0):
					print("log cleared")
				db.commit()
		else:
			print("EMPTY LOG")

		time.sleep(10)
		print("Spam check done")


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/editor')
def upload_form():
	# return render_template('upload.html')
	return render_template("online-editor.html")

@app.route('/editor', methods=['POST'])
def upload_file():
	# print("here")
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
			print(file_path)
			file.save(file_path)
			flash('File successfully uploaded')
			message=[file_path]
			resp=jsonify(message)
			resp.status_code=200
			return resp
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)
# t=threading.Thread(target=spam_check)
# t.start()
app.run(debug=True,host="0.0.0.0",port=1000)
