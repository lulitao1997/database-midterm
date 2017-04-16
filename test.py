from flask import Flask, render_template, flash, redirect, url_for, session
from flask_wtf import Form
from wtforms import IntegerField, SubmitField
from wtforms.validators import Required, NumberRange
from flask_bootstrap import Bootstrap
import jinja2
import numpy as np

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

@app.route('/test/dashboard-curriculum')
def test_dashboard_curriculum():
	cname = np.ones((20,20))
	return render_template('dashboard-curriculum.html', cname = cname)

@app.route('/test/dashboard-coursesavailable')
def test_dashboard_coursesavailable():
	course = [('computer', 'z201'), ('love','z202')]
	return render_template('dashboard-coursesavailable.html', course = course)


@app.route('/test/dashboard-coursespossessed')
def test_dashboard_coursespossessed():
	course = [('computer', 'z201'), ('love','z202')]
	return render_template('dashboard-coursespossessed.html', course = course)

@app.route('/test/welcome')
def test_welcome():
	return render_template('welcome.html')

@app.route('/test/welcome', methods=['POST'])
def gologin():
	return redirect('/test/login')

@app.route('/test/login')
def login():
	return render_template('login.html')
app.run(debug = False)
