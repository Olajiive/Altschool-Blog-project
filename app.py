from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os



app = Flask(__name__, template_folder="templates")

picsfolder = os.path.join('static', 'image')

app.config['UPLOAD_FOLDER']=picsfolder
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///user.db"
app.config["SQLALCHEMY_BINDS"]={
    "post": "sqlite:///post.db"
    }
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]='0acdf54aa627351b42f02679'

db= SQLAlchemy(app)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.Text())
    post = db.relationship('Post', backref='user', lazy='dynamic' )

    def __repr__(self):
        return f"user: {self.firstname}"

class Post(db.Model, UserMixin):
    __bind_Key__ = "post"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    Author= db.Column(db.String(), nullable=False)
    Registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    post_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<post '{self.title}'>"



login_manager = LoginManager(app)

@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))

@app.route('/')
def home():
    posts=Post.query.all()
    context = {
        "posts": posts
    }
    return render_template('home.html', **context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user_email = User.query.filter_by(email=email).first()
        if user_email and check_password_hash(user_email.password_hash, password):
            login_user(user_email)
            return redirect (url_for('home'))


        else:
            flash('Invalid email or password')
        
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        password = request.form.get("password")

        user_email= User.query.filter_by(email=email).first()
        if user_email:
            flash("Email has been taken by someone else")
            return redirect(url_for('signup'))

        password_hash = generate_password_hash(password)

        new_user = User(email=email, firstname=firstname, lastname=lastname, password_hash=password_hash)
        
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/post', methods=['GET', 'POST'])
@login_required
def account():
    if request.method=='POST':
        title=request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        post=Post(title=title, Author=author, content=content, user=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post'))
    return render_template('create_post.html')


@app.route('/user/post/')
def post():
    posts = Post.query.filter_by(post_id=current_user.id).all()
    return render_template('post.html', posts = posts, user = current_user )

@app.route('/account', methods=['GET', 'POST'])
def account_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        Author = request.form.get('author')

        new_post = Post(title=title, content=content , Author=Author)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/user/post')

    return render_template('post.html')

@app.route('/post/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)

    if request.method == "POST":
        post.title = request.form.get("title")
        post.Author = request.form.get("author")
        post.content = request.form.get("content")
        
        
        db.session.commit()

        return redirect(url_for("post"))
    return render_template('update.html' , post=post)


@app.route('/post/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    
    return redirect(url_for('post'))


@app.route('/about')
def about():
    pic1= os.path.join(app.config['UPLOAD_FOLDER'], 'photo.jpg' )
    return render_template('about.html', user_image=pic1)

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)