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
	computer = dict()
	computer['cid']=12345
	computer['cells'] = ['1-1','2-2','3-3']
	computer['info'] = ('12345', 'computer', 'wang', '1', '100')
	computer['done'] = True
	cs = { 'cid': 123, 'cells': ['1-3','4-5'], 'info': ('123', 'cs', 'wang', '1', '100'), 'done': False }
	course = [computer, cs]
	cname = np.ones((20,20))	
	return render_template('dashboard-coursesavailable.html', course = course, cname = cname)


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
