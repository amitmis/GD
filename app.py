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
db = SQLAlchemy(app)
cursor = dbconn.cursor()

class Deed_post(db.Model):

    Name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(12),primary_key=True,nullable=False)
    Text = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(12), nullable=True)
    fname= db.Column(db.String(60), nullable=True)
    pname = db.Column(db.String(60), nullable=True)
    S_NO =  db.Column(db.Integer, nullable=True)
    # Contact = db.Column(db.String(12), nullable=True)

@app.route("/")
def home():
    return render_template("index.html")






@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    # try:
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        desc= request.form.get('desc')
        f = request.files['img']
        f1 = request.files['img1']
        n = f.filename
        n1 = f1.filename
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        f1.save(os.path.join(app.config['UPLOAD_FOLDER1'], secure_filename(f1.filename)))
        # phone = request.form.get('phone')
        entry = Deed_post(Name=name, Text = desc,Email = email,Date= datetime.now(), fname=n,pname=n1)
        db.session.add(entry)
        db.session.commit()
        # data = Deed_post.query.order_by(-Deed_post.S_NO).first()
        data = Deed_post.query.all()
        # abc = dict(data)



        # mail.send_message('You are doing Great ' + name + " !",
        #                   sender=email,
        #                   recipients=[email],
        #                   body= "Hi " + name + "!" +  "\n May your kindness and generosity return to you a hundredfold. \n You are such a wonderful blessing to many people. \n Thank you so much, and may you continue your good work every single day. There are not enough words that can express just how much we appreciate your kindness and generosity\n\n\n With Care \n Team  Gooddeeds" )
    return render_template("index_1.html",data = data)
    # except:
    #     return render_template('404.html')

@app.route('/enterDeed', methods = ['POST'])
def enterDeed():

    req = request.get_json()

    print(req)

    res = make_response(jsonify({'message':'JSON Received'}),200)

    return res



app.run(debug=True)
