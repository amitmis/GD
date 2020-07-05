#!/home/amit/anaconda3/envs/sci/bin/python3
# import pymysql
from flask import Flask,render_template,request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,template_folder='template')

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'infogooddeed',
    MAIL_PASSWORD=  ''
)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/deeds'
db = SQLAlchemy(app)

class Deed_post(db.Model):

    Name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(12),primary_key=True,nullable=False)
    Text = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(12), nullable=True)
    Contact = db.Column(db.String(12), nullable=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        desc= request.form.get('desc')
        phone = request.form.get('phone')
        entry = Deed_post(Name=name, Text = desc,Email = email,Date= datetime.now(),Contact = phone )
        db.session.add(entry)
        db.session.commit()

        mail.send_message('You are doing Great ' + name + "!",
                          sender=email,
                          recipients=[email],
                          body= "Email send successful"
                          )
    return render_template("index.html")

@app.route('/enterDeed', methods = ['POST'])
def enterDeed():

    req = request.get_json()
    name = request.json['name']
    email = request.json['email']
    location = request.json['location']
    deed = request.json['userDeed']
    userImage = request.json['imageUser']
    deedImage = request.json['imageDeed']

    print(req)
    # print('name =',name,email)

    res = make_response(jsonify({'message':'JSON Received'}),200)

    return res



app.run(port=5012,debug=True)