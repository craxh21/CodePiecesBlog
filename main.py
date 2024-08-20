
from flask import Flask, render_template , request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/code pieces blog' 

db = SQLAlchemy(app)

class Contacts(db.Model):
   
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(13),nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)

@app.route("/" )
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact", methods = ['GET', 'POST'])
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
        
    return render_template('contact.html')



@app.route("/post")
def post():
    return render_template('post.html')

app.run(debug= True) 


