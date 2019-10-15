from flask import Flask,request,jsonify,json
import pymysql
import requests


app=Flask(__name__)
db=pymysql.connect('192.168.0.107','root','123','mailIt')
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
app.run(debug=True,host="0.0.0.0",port=1000)
