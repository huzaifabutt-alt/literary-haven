from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db, bcrypt
from app.models import User, Blogpost
from app.forms import LoginForm, RegistrationForm
from flask import session
from flask import jsonify
from datetime import datetime
main = Blueprint('main', __name__)
# define routes here
ADMIN_PASSWORD = 'sajjad'
@main.route('/contact')
def contact():
    return render_template('contact.html')
@main.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    return render_template('post.html', post=post)

@main.route('/admin/add')
def add():
    return render_template('add.html')
@main.route('/logoutadmin')
def logoutadmin():
    session.pop('authenticated', None)
    return redirect(url_for('admin'))
@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Get the password from the form
        password = request.form.get('password')

        # Check if the password is correct
        if password == ADMIN_PASSWORD:
            # If correct, render the admin1.html template
            return render_template('admin1.html', authenticated=True)
        else:
            # If incorrect, reload admin.html with an error message
            return render_template('admin.html', authenticated=False, error="Invalid password")

    # For GET requests, simply render the login form in admin.html
    return render_template('admin.html', authenticated=False)
@main.route('/search_posts', methods=['GET'])
def search_posts():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    
    query = request.args.get('query', '').lower()
    if query:
        results = [post for post in posts if query in post.title.lower() or query in post.subtitle.lower()]
    else:
        results = []
    return jsonify({'results': [{'id': post.id, 'title': post.title, 'subtitle': post.subtitle} for post in results]})


@main.route('/admin/delete')
def delete():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('delete.html', posts=posts)
@main.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # Save or process
    return redirect(url_for('main.contact'))

@main.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/deletepost', methods=['DELETE','POST'])
def deletepost():
    post_id = request.form.get("post_id")

    post = Blogpost.query.filter_by(id=post_id).first()

    db.session.delete(post)
    db.session.commit()
    
    return redirect(url_for('main.index'))
