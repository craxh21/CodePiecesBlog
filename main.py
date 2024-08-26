from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message  
import os
from dotenv import load_dotenv  #to load the environment variables from the .env file into flask app

import json


local_server = True

with open('config.json', 'r') as c:  #open the json file in read mode
    params = json.load(c)["params2"]   #and load it to a variable params



app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
"""app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/code pieces blog' """

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,  # Use port 587 for TLS
    MAIL_USE_TLS=True,  # Enable TLS
    # MAIL_USERNAME= params['gmail_user'],  
    # MAIL_PASSWORD= params['gmail_password']   # here taking values by config.json file is giving error
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),   #these variables 'MAIL_USERNAME' and 'MAIL_PASSWORD' must be initialized in a .evn file in the root directory of project
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD') 
)
mail = Mail(app)    #creating object of class Mail by passing app parameter to it


if(local_server): #when local server is found running then configure thr DB to local uri
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']  
else:  #else to the production uri
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_uri']

db = SQLAlchemy(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(13),nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),  nullable=False)
    tagline = db.Column(db.String(50),  nullable=False)
    slug = db.Column(db.String(21), nullable=False)  #slug is the remaining part of url seen besides the main name of the url. 
    content = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(12), nullable=True)
    date = db.Column(db.String(12), nullable=True)



@app.route("/")
def home():
    posts = Posts.query.filter_by().all()[0: params['no_of_posts_on_home_page']]
    return render_template('index.html', params= params, posts = posts ) #lhs is the posts object used in the index.html file and the rhs is the posts object declared in this function

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if(request.method=='POST'):
        #redirect to admin panel
        pass

    else:
        return render_template('login.html', params= params)

@app.route("/about")
def about():
    return render_template('about.html', params= params)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':  #i.e when the user clicks on send button
        # Fetching entry from the form
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        # Making entry in the database 
        # #lhs are var names in the db and the rhs are the var names used in this file to store the fetched values from the user entry
        entry = Contacts(name=name, phone_num=phone, msg=message, email=email, date=datetime.now())
        db.session.add(entry)
        db.session.commit()

        # Prepare and send the email
        mailSubject = f'New message from {name}'
        recipient = os.getenv('MAIL_USERNAME')  # value of the MAIL_USERNAME is stored in .env file
        body = f'Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}'

        if not (mailSubject and recipient and body):
            return 'Invalid request. Please provide subject, recipient, and body parameters.'

        try:
            msg = Message(subject=mailSubject, sender=email, recipients=[recipient])
            msg.body = body
            mail.send(msg)
            return 'Email sent successfully!'
        except Exception as e:
            return f'An error occurred: {e}'

    return render_template('contact.html', params=params)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post_func(post_slug):
    #creating object post2 of class Posts
    post2 = Posts.query.filter_by( slug = post_slug ).first()  #filter by slug named post_slug . and select the first tuple in the table

    return render_template('post.html', params=params, post = post2) # pass the post with post2 object created before




app.run(debug= True)