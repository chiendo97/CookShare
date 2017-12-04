# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import User

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle request to the /register route
    Add an User to the database through the registration form
    :return:
    """
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! You may now login')

        # Redirect to the login page
        return redirect(url_for('auth.login'))

    # load the registration template
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """

    :return:
    """

    form = LoginForm()
    if form.validate_on_submit():
        # check whether user exists in the database and whether
        # the password entered matches the password in the databse

        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # log user in
            login_user(user)

            # redirect to the dashboard page after login
            return redirect(url_for('home.admin_dashboard'))

            # if user.is_admin:
            #     return redirect(url_for('home.admin_dashboard'))
            # else:
            #     return redirect(url_for('home.dashboard'))

        else:
            flash('Invalid email or password')

    # load the login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """

    :return:
    """
    logout_user()
    flash('You have successfully been logged out')

    # redirect to the login page
    return redirect(url_for('auth.login'))