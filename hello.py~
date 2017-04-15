from flask import Flask, render_template, flash, redirect, url_for, session
from flask_wtf import Form
from wtforms import IntegerField, SubmitField
from wtforms.validators import Required, NumberRange
from flask_bootstrap import Bootstrap
import jinja2

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

@app.route('/')
def index():
	return render_template('welcome.html')

@app.route('/', methods=['POST'])
def gologin():
	return render_template('login.html')
	
@app.route('/login')
def login():
	return render_template('login.html')
app.run(debug = False)


