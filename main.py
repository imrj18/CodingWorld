from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from flask_mail import Mail
import json
import os
import math
# from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = params['local_server']

app = Flask(__name__)


# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT='465',
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME=params['gmail-user'],
#     MAIL_PASSWORD=params['gmail-password']
# )
# mail = Mail(app)

SECRET_KEY = os.urandom(32)

app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config['SECRET_KEY'] = SECRET_KEY  # Change this to a secure secret key

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['glb_url']

db = SQLAlchemy(app)


class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Post(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(30), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Define the relationship with the User model
    author = db.relationship('User', backref=db.backref('posts', lazy=True))


@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if "user" in session:
        email = session['user']
        user = User.query.filter_by(email=email).first()
        if user:
            if request.method == 'POST':
                f = request.files['file1']
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                return "Uploaded successfully!"


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')


@app.route("/delete/<int:sno>", methods=['GET', 'POST'])
def delete(sno):
    if "user" in session:
        email = session['user']
        user = User.query.filter_by(email=email).first()
        if user:
            posts = Post.query.filter_by(sno=sno).first()
            db.session.delete(posts)
            db.session.commit()
    return redirect("/dashboard")


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if 'user' in session:
        user = User.query.filter_by(email=session['user']).first()
        if user:
            posts = Post.query.filter_by(user_id=user.id).all()
            return render_template("dashboard.html", params=params, posts=posts)

    return redirect('/login')


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect('/dashboard')

    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("uname")
        userpass = request.form.get("upass")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('signup.html', params=params, error='Email already exists')

        new_user = User(name=username, email=email, password=userpass)  # Store password in plain text
        db.session.add(new_user)
        db.session.commit()

        session['user'] = email  # Log the user in automatically after signup
        return redirect('/dashboard')

    return render_template('signup.html', params=params)


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect('/dashboard')

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('upass')

        user = User.query.filter_by(email=email).first()

        # Check if user exists and password matches
        if user and user.password == password:  # Comparing plain text passwords
            session['user'] = user.email
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid email or password', params=params)

    return render_template('login.html', params=params)


@app.route("/create", methods=['GET', 'POST'])
def create_post():
    if "user" in session:
        email = session['user']
        user = User.query.filter_by(email=email).first()
        if user:
            if request.method == "POST":
                box_title = request.form.get('title')
                tline = request.form.get('tline')
                slug = request.form.get('slug')
                content = request.form.get('content')
                img_file = request.form.get('img_file')
                date = datetime.now()
                new_post = Post(title=box_title, slug=slug, content=content, tagline=tline, img_file=img_file,
                                date=date, user_id=user.id)
                db.session.add(new_post)
                db.session.commit()
                return redirect('/dashboard')  # Redirect to dashboard or any other page
            return render_template('create.html', params=params)
    else:
        return redirect('/login')  # Redirect to login page if user is not authenticated


@app.route("/edit/<int:sno>", methods=['GET', 'POST'])
def edit(sno):
    if "user" in session:
        email = session['user']
        user = User.query.filter_by(email=email).first()
        if user:
            post = Post.query.get_or_404(sno)
            if request.method == "POST":
                post.title = request.form.get('title')
                post.tagline = request.form.get('tline')
                post.slug = request.form.get('slug')
                post.content = request.form.get('content')
                post.img_file = request.form.get('img_file')
                db.session.commit()
                return redirect('/dashboard')  # Redirect to dashboard or any other page
            print(True)
            return render_template('edit.html', params=params, post=post)
    else:
        print(False)
        return redirect('/login')  # Redirect to login page if user is not authenticated


@app.route("/")
def home():
    posts = Post.query.filter_by().all()
    last = math.ceil(len(posts) / int(params['no_of_posts']))
    page = request.args.get('page')
    if not str(page).isnumeric():
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts'])+int(params['no_of_posts'])]
    if page == 1:
        prev = "#"
        next = "/?page=" + str(page + 1)
    elif page == last:
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)

    usernames = {}
    for post in posts:
        user = User.query.get(post.user_id)
        usernames[post.user_id] = user.name if user else 'Unknown'

    return render_template('index.html', params=params, posts=posts, prev=prev, next=next, usernames=usernames)


@app.route("/about")
def about():
    return render_template('about.html', params=params)


@app.route("/post")
def allpost():
    global post
    posts = Post.query.filter_by().all()
    usernames = {}
    for post in posts:
        user = User.query.get(post.user_id)
        usernames[post.user_id] = user.name if user else 'Unknown'
    post_content = post.content.replace('\n', '<br>')
    return render_template('AllPost.html', params=params, posts=posts, usernames=usernames, post_content=post_content)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    if post:
        user = User.query.get(post.user_id)
        user_name = user.name if user else 'Unknown'
        post_content = post.content.replace('\n', '<br>')
        return render_template('post.html', params=params, post=post, user_name=user_name, post_content=post_content)
    else:
        # Handle the case where no post is found with the given slug
        return render_template('post_not_found.html')


@app.route('/success')
def success():
    return render_template('success.html', params=params)


@app.route('/failure')
def failure():
    return render_template('failure.html', params=params)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contact(name=name, email=email, phone_num=phone, msg=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        # mail.send_message('New message from ' + name,
        #                   sender=email,
        #                   recipients=[params['gmail-user']],
        #                   body=message + "\n" + phone
        #                   )
        success_message = "Your message has been successfully submitted!"
        return render_template("contact.html", success_message=success_message, params=params)
    return render_template('contact.html', params=params)


app.run(debug=True)
