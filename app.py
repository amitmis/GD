#!/home/amit/anaconda3/envs/sci/bin/python3
# import pymysql
from flask import Flask, render_template, request, redirect, make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import pymysql
from werkzeug.utils import secure_filename
import os


import json
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,template_folder='template')

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'infogooddeed',
    MAIL_PASSWORD=  'gooddeed@2020'
)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/deeds'
app.config['UPLOAD_FOLDER'] = '//home//amit//Gooddeeds//GD//static//uploads//deed_img'
app.config['UPLOAD_FOLDER1'] = '//home//amit//Gooddeeds//GD//static//uploads//profile_img'
dbconn = pymysql.connect("localhost","root","","deeds")
cursor = dbconn.cursor()
db = SQLAlchemy(app)

class Deed_post(db.Model):

    Name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(12),primary_key=True,nullable=False)
    Text = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(12), nullable=True)
    # fname= db.Column(db.String(60), nullable=True)
    # pname = db.Column(db.String(60), nullable=True)
    S_NO =  db.Column(db.Integer, nullable=True)
    # Contact = db.Column(db.String(12), nullable=True)
    Location = db.Column(db.String(60), nullable=True)
@app.route("/")
def home():
    return render_template("index.html")



@app.route('/enterDeed', methods = ['POST'])
def enterDeed():
    # req = request.get_json()
    name = request.form['name']
    email = request.form['email']
    location = request.form['location']
    # deed = request.form['userDeed']
    userDeed = request.form['deed']
    userImage = request.file['imageUser']
    deedImage = request.file['imageDeed']
    # os.path.join(base_path + "/static/images", file.filename)
    # file.save(file_path)
    entry = Deed_post(Name=name, Text=userDeed, Email=email, Date=datetime.now(),Location=location)
    db.session.add(entry)
    db.session.commit()
    print(name, email,location)
    cursor.execute("select * from deed_post")
    res = cursor.fetchall()

    row_headers = [x[0] for x in cursor.description]  # this will extract row headers
    json_data = []
    for result in res:
        json_data.append(dict(zip(row_headers, result)))

    language = request.args.get('name')  # if key doesn't exist, returns None
    x= json.dumps(json_data, indent=4, sort_keys=True, default=str)


    return json.dumps(json_data, indent=4, sort_keys=True, default=str)



app.run(debug=True)