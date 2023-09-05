from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from utils.forms import LoginForm,RegistrationForm
from app import db
from models import User
router = Blueprint('auth', __name__)


@router.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        # return form.username.data+" "+form.password.data
        # Perform a query to find the user
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # Replace this with hashed password check
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


@router.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)  # Replace this with hashed password
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@router.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))

