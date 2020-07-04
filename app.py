#!/home/amit/anaconda3/envs/sci/bin/python3
# import pymysql
from flask import Flask,render_template,request, redirect
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
app.config['UPLOAD_FOLDER'] = '//home//amit//Gooddeeds//GD//static'
dbconn = pymysql.connect("localhost","root","","deeds")
db = SQLAlchemy(app)
cursor = dbconn.cursor()
# name = request.files['img'].filename

class Deed_post(db.Model):

    Name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(12),primary_key=True,nullable=False)
    Text = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(12), nullable=True)
    fname= db.Column(db.String(60), nullable=True)
    # Contact = db.Column(db.String(12), nullable=True)

@app.route("/")
def home():
    return render_template("index.html")






@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    try:
        if(request.method=='POST'):
            '''Add entry to the database'''
            name = request.form.get('name')
            email = request.form.get('email')
            desc= request.form.get('desc')
            f = request.files['img']
            n = f.filename
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            # phone = request.form.get('phone')
            entry = Deed_post(Name=name, Text = desc,Email = email,Date= datetime.now(), fname=n)
            db.session.add(entry)
            db.session.commit()
            data = Deed_post.query.all()
            # abc = dict(data)

            # cursor.execute("select * from deed_post")
            # res = cursor.fetchall()
            # abc=json.dumps(res, indent=4, default=str)
            # print(json.dumps(res, indent=4, default=str))

            mail.send_message('You are doing Great ' + name + " !",
                              sender=email,
                              recipients=[email],
                              body= "Email send successful"
                              )
        return render_template("index.html",data = data)
    except:
        return render_template('404.html')





app.run(debug=True)
