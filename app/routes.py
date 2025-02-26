from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app import app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_required, login_user, logout_user
import sqlalchemy as sa
from app import db
from app.models import User


title = 'TRX Companion'


@app.route('/')
@app.route('/index')
@login_required
def index():
    exercises = [
        {
            'name': 'Rowing',
            'description': 'A good way to start your day',
            'image': 'img.jpg',
            'alt': 'Rowing'},
        {
            'name': 'Yoga',
            'description': 'A good way to start your day',
            'image': 'img.jpg',
            'alt': 'Yoga'},
        {
            'name': 'Cycling',
            'description': 'A good way to start your day',
            'image': 'img.jpg',
            'alt': 'Cycling'},
        {
            'name': 'Rowing',
            'description': 'A good way to start your day',
            'image': 'img.jpg',
            'alt': 'Rowing'},
        {
            'name': 'Yoga',
            'description': 'A good way to start your day',
            'image': 'img.jpg',
            'alt': 'Yoga'},
        {
            'name': 'Cycling',
            'description': 'A good way to start your day',
            'image': 'img.jpg',
            'alt': 'Cycling'}
    ]
    return render_template('index.html',
                           title=title,
                           name="Home",
                           exercises=exercises)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title=title, name="Login", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    workouts = [
        {
            'name': 'Morning Core',
            'exercises': [
                {
                    'name': 'Rowing',
                    'description': 'A good way to start your day',
                    'image': 'img.jpg',
                    'alt': 'Rowing'},
                {
                    'name': 'Yoga',
                    'description': 'A good way to start your day',
                    'image': 'img.jpg',
                    'alt': 'Yoga'},
                {
                    'name': 'Cycling',
                    'description': 'A good way to start your day',
                    'image': 'img.jpg',
                    'alt': 'Cycling'}
            ]
            }
        ]
    return render_template('user.html',
                           title=title,
                           name="User " + username,
                           user=user,
                           workouts=workouts)
