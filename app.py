import os
from flask_gravatar import Gravatar
import flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

login_manager = LoginManager()
from flask import Flask, request
from flask import render_template, url_for
import requests
import smtplib
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.utils import redirect

from forms import MyForm, EditPostForm, login_form, register_form, CommentForm

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-dev-key')
Bootstrap5(app)
login_manager.init_app(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

ckeditor = CKEditor(app)

gravatar = Gravatar(app,
                    size=50,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    posts = db.relationship("BlogPost", back_populates="author")
    comments = db.relationship("Comments", back_populates="author")
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(500), nullable=False)


class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author = db.relationship("User", back_populates="posts")
    comments = db.relationship("Comments", back_populates="post")
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

class Comments(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("blog_post.id"))
    author = db.relationship("User", back_populates="comments")
    post = db.relationship("BlogPost", back_populates="comments")
    text: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)

with app.app_context():
    db.create_all()

@app.context_processor
def inject_user():
    return dict(user=current_user, gravatar=gravatar)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route("/all_posts")
@login_required
def home():
    data_ = BlogPost.query.all()
    return render_template("index.html", data=data_,
                           bg_image=url_for('static', filename='assets/img/home-bg.jpg'),
                           H1="Hello, I'm Ahmad",
                           H2="Welcome to my blog — ideas, code & more.")


@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    sub_head = "I will be happy to connect and share ideas."
    main_heading = "Contact me?"

    if request.method == "POST":
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        message_text = request.form.get('message')

        if name and email and message_text:
            mail_body = f"""
    Name: {name}
    Phone Number: {phone}
    Email: {email}
    Message: {message_text}
    """
            # Properly format the email with Subject header
            formatted_message = "Subject: Connection request\n\n" + mail_body
            sender_mail = os.getenv("email")
            sender_pass = os.getenv("password")
            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender_mail, sender_pass)
                    response = server.sendmail(sender_mail, "computergeek125aka@gmail.com", formatted_message)
                    if not response:
                        main_heading = "Your message was sent successfully"
                        sub_head = "Looking forward to connect"
                    else:
                        sub_head = "Your message couldn't reach me."
                        main_heading = "Try Again"
            except Exception:
                sub_head = "Something went wrong. Please try again later."
                main_heading = "Try Again"

    return render_template("contact.html",
                           bg_image=url_for('static', filename='assets/img/contact-bg.jpg'),
                           H1=main_heading, H2=sub_head)


@app.route("/<int:postid_>", methods=['POST', 'GET'])
@login_required
def sample_post(postid_):
    form = CommentForm()
    post = db.get_or_404(BlogPost, postid_)
    if form.validate_on_submit():
        comment = Comments(post_id=postid_, text=form.body.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        form.body.data = ""
    comments = Comments.query.filter_by(post_id=postid_)
    return render_template(
        "post.html",
        id=postid_,
        bg_image=post.img_url,
        post=post, H1=post.title, H2=post.subtitle, form=form, comments=comments
    )


@app.route("/about")
@login_required
def about():
    return render_template("about.html",
                           bg_image=url_for('static', filename='assets/img/about-bg.jpg'),
                           H1="About Me!", H2="I am Ahmad — an AI engineer.")


@app.route("/post_form", methods=['POST', "GET"])
@login_required
def create_post():
    form_ = MyForm()
    if form_.validate_on_submit():
        post = BlogPost(author=current_user, title=form_.title.data, subtitle=form_.subtitle.data,
                        date=form_.date.data, body=form_.body.data, img_url=form_.image_uri.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("home"))  # BUG FIX: was missing return
    return render_template("make-post.html",
                           bg_image=url_for('static', filename='assets/img/about-bg.jpg'),
                           H1="New Post", H2="You're going to make a great blog post!",
                           form=form_)


@app.route("/delete/<int:id>")
@login_required
def delete_post(id):
    post = db.get_or_404(BlogPost, id)
    if current_user.id == post.author_id:
        db.session.delete(post)
        db.session.commit()
    else:
        flask.flash("You can't delete this post — only the author can.", "danger")
    return redirect(url_for('home'))


@app.route("/delete_comment/<int:id>")
@login_required
def delete_comment(id):
    comment = db.get_or_404(Comments, id)
    postid = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('sample_post', postid_=postid))


@app.route("/my-posts")
@login_required
def my_posts():
    user_posts = BlogPost.query.filter_by(author_id=current_user.id).all()
    return render_template("my_posts.html",
                           bg_image=url_for('static', filename='assets/img/home-bg.jpg'),
                           H1="My Posts",
                           H2="Manage everything you've written.",
                           posts=user_posts)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    form_ = EditPostForm()
    post = db.get_or_404(BlogPost, id)
    if post.author_id != current_user.id:
        # BUG FIX: was showing flash in wrong place
        flask.flash("You can't edit this post — only the author can.", "danger")
        return redirect(url_for("home"))
    if form_.validate_on_submit():
        if form_.title.data:
            post.title = form_.title.data
        if form_.subtitle.data:
            post.subtitle = form_.subtitle.data
        if form_.img_url.data:
            post.img_url = form_.img_url.data
        if form_.body.data:
            post.body = form_.body.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html",
                           bg_image=url_for('static', filename='assets/img/about-bg.jpg'),
                           H1="Edit Post", H2="Update the fields you'd like to change.",
                           form=form_, post=post)


@app.route("/", methods=['GET', 'POST'])
def login():
    main_heading = "Log In"
    sub_head = "Welcome Back!"
    form = login_form()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flask.flash('Logged in successfully.', 'success')
            next_page = flask.request.args.get('next')
            return flask.redirect(next_page or flask.url_for('home'))
        else:
            flask.flash('Invalid email or password. Please try again.', 'danger')
    return render_template("login.html",
                           bg_image=url_for('static', filename='assets/img/login-bg.jpg'),
                           H1=main_heading, H2=sub_head, form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    main_heading = "Register"
    sub_head = "Start contributing to the blog!"
    form = register_form()
    if form.validate_on_submit():
        existing_user = db.session.query(User).filter_by(email=form.email.data).first()
        if existing_user:
            flask.flash("Email already registered. Please log in instead.", "warning")
            return redirect(url_for("login"))
        hashed_password = generate_password_hash(form.password.data, method="scrypt:32768:8:2", salt_length=16)
        user = User(username=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flask.flash("Registered successfully! Please log in.", "success")
        return redirect(url_for("login"))  # BUG FIX: was missing return
    return render_template("register.html",
                           bg_image=url_for('static', filename='assets/img/register-bg.jpg'),
                           H1=main_heading, H2=sub_head, form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
