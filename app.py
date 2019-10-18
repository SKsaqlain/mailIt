from flask import Flask,request,jsonify,json
import pymysql
import requests
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

db=pymysql.connect('192.168.43.85','root','123','mailIt',cursorclass=pymysql.cursors.DictCursor)
cursor=db.cursor()


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

app.run(debug=True,host="0.0.0.0",port=1000)
