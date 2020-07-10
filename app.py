#!/home/amit/anaconda3/envs/sci/bin/python3
# import pymysql
from flask import Flask, render_template, request, redirect, make_response,url_for,jsonify
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
app.config['UPLOAD_FOLDER'] = '//home//amit//Gooddeeds//GD//static//uploads//profile_img'
app.config['UPLOAD_FOLDER1'] = '//home//amit//Gooddeeds//GD//static//uploads//deed_img'
dbconn = pymysql.connect("localhost","root","","deeds")
cursor = dbconn.cursor()
db = SQLAlchemy(app)

class Deed_post(db.Model):

    Name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(12),primary_key=True,nullable=False)
    Text = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(12), nullable=True)
    Usr_Img= db.Column(db.String(60), nullable=True)
    Deed_Img = db.Column(db.String(60), nullable=True)
    S_NO =  db.Column(db.Integer, nullable=True)
    # Contact = db.Column(db.String(12), nullable=True)
    Location = db.Column(db.String(60), nullable=True)
@app.route("/")
def home():
    # cursor.execute("select * from deed_post order by S_NO desc")
    # res = cursor.fetchall()
    res = Deed_post.query.order_by(Deed_post.S_NO.desc()).all()

    return render_template("index.html",data=res)



@app.route("/enterDeed",methods=['POST'])
def enterDeed():
    # req = request.get_json()
    name = request.form['name']
    email = request.form['email']
    location = request.form['location']
    # deed = request.form['userDeed']
    userDeed = request.form['deed']
    userImage = request.files['imageUser']
    deedImage = request.files['imageDeed']
    n = userImage.filename
    n1 = deedImage.filename
    userImage.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(userImage.filename)))
    deedImage.save(os.path.join(app.config['UPLOAD_FOLDER1'], secure_filename(deedImage.filename)))

    entry = Deed_post(Name=name, Text=userDeed, Email=email, Date=datetime.now(),Location=location,Usr_Img=n,Deed_Img=n1)
    db.session.add(entry)
    db.session.commit()
    # print(name, email,location)
    mail.send_message('You are doing Great ' + name + " !",
                      sender=email,
                      recipients=[email],
                      body= "Hi " + name + "!" +  "\nMay your kindness and generosity return to you a hundredfold. \nYou are such a wonderful blessing to many people. \nThank you so much, and may you continue your good work every single day. There are not enough words that can express just how much we appreciate your kindness and generosity\n\n\nWith Care, \nTeam  Gooddeeds" )

    cursor.execute("select * from deed_post order by S_NO desc")
    res = cursor.fetchone()


    row_headers = [x[0] for x in cursor.description]  # this will extract row headers
    json_data = []
    # for result in res:
    json_data.append(dict(zip(row_headers, res)))

    # language = request.args.get('name')  # if key doesn't exist, returns None
    x= json.dumps(json_data, indent=4, sort_keys=True, default=str)
    print(x)

    # return json.dumps(json_data, indent=4, sort_keys=True, default=str)
    # return redirect(url_for('home'))
    res = make_response(jsonify({'message': 'JSON Received'}), 200)

    return res



app.run(debug=True)