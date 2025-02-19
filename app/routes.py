from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
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
      'alt': 'Cycling'}
  ]
  return render_template('index.html',
                         title='TRX Exercises',
                         exercises=exercises)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)  