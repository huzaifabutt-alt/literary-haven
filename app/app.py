from flask import Flask, render_template,flash, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_login import login_user, current_user, logout_user, login_required

from forms import RegistrationForm, LoginForm
from datetime import datetime
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from  flask_login import login_required
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 