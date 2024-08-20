from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

local_server = True

with open('config.json', 'r') as c:
    params = json.load(c)["params"]



app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
"""app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/code pieces blog' """

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_uri']

db = SQLAlchemy(app)


class Contacts(db.Model):
   
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(13),nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)

@app.route("/")
def home():
    return render_template('index.html', params= params)

@app.route("/about")
def about():
    return render_template('about.html', params= params)


@app.route("/contact", methods = ['GET', 'POST'])   #get req ... used to fetch the index.html
def contact():
    if(request.method=='POST'):
        # this if fetching entry from the db
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        # making entry
        entry = Contacts(name=name, phone_num = phone, msg= message, email = email, date= datetime.now())

        # adding the entry
        db.session.add(entry)
        db.session.commit()
        
    return render_template('contact.html', params= params)




@app.route("/post")
def post():
    return render_template('post.html', params=params)

app.run(debug= True)