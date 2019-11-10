from flask import Flask,request,jsonify,json
import pymysql
import requests
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

db=pymysql.connect('192.168.137.171','root','123','mailIt',cursorclass=pymysql.cursors.DictCursor)
cursor=db.cursor()

def clear_db():
	sql="delete from email;"
	try:
		cursor.execute(sql)
		db.commit();
	except:
		pass
	sql="delete from user;"
	try:
		cursor.execute(sql)
		db.commit()
	except:
		pass

email=["apple","mango","orange","banana","cat","bat","hat"]



def fill_db():
	for ele in email:
		
