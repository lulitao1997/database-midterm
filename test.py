# -*- coding: utf-8 -*-
from flask import Flask, render_template, flash, redirect, url_for, session, request
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
	computer = dict()
	computer['cid']=12345
	computer['cells'] = ['1-1','2-2','3-3']
	computer['info'] = ('123435', 'computer', 'wang', '1', '100')
	computer['done'] = True
	cs = { 'cid': 123, 'cells': ['1-3','4-5'], 'info': ('123', 'cs', 'wang', '1', '100'), 'done': False }
	course = [computer, cs]
	cnameincell = [['hellooooo' for col in range(15)] for row in range(8)]
	return render_template(
		'dashboard-curriculum.html',
		course = course, 
		cnameincell = cnameincell,
		sidebar_name = 'curriculum'
	)

# dashboard-coursesavailable
@app.route('/test/dashboard-coursesavailable-<pagenumber>')
def test_dashboard_coursesavailable(pagenumber):
	computer = dict()
	computer['cid']=12345
	computer['cells'] = ['1-1','2-2','3-3']
	computer['info'] = ('123435', 'computer', 'wang', '1', '100')
	computer['done'] = True
	cs = { 'cid': 123, 'cells': ['1-3','4-5'], 'info': ('123', 'cs', 'wang', '1', '100'), 'done': False }
	course = [computer, cs]
	cnameincell = [['hellooooooo' for col in range(15)] for row in range(8)]
	return render_template(
		'dashboard-coursesavailable.html', 
		pageamount=10, 
		pagenumber=int(pagenumber), 
		course = course, 
		cnameincell = cnameincell,
		sidebar_name = 'coursesavailable'
	)

@app.route('/test/dashboard-coursesavailable-<pagenumber>', methods=['POST'])
def test_dashboard_coursesavailable_post(pagenumber):
	if 'select' in request.form:
		s = request.form['select']
		return s
	elif 'search' in request.form:
		return request.form['cname']
	else:
		return redirect('test.login')
		
# dashboard-coursespossessed
@app.route('/test/dashboard-coursespossessed')
def test_dashboard_coursespossessed():
	computer = dict()
	computer['cid']=12345
	computer['cells'] = ['1-1','2-2','3-3']
	computer['info'] = ('123435', 'computer', 'wang', '1', '100')
	computer['done'] = True
	cs = { 'cid': 123, 'cells': ['1-3','4-5'], 'info': ('123', 'cs', 'wang', '1', '100'), 'done': False }
	course = [computer, cs]
	cnameincell = [['hellooooooo' for col in range(15)] for row in range(8)]
	return render_template(
		'dashboard-coursespossessed.html', 
		course = course, 
		cnameincell = cnameincell,
		sidebar_name = 'coursespossessed'
	)

@app.route('/test/dashboard-coursespossessed', methods=['POST'])
def test_dashboard_coursespossessed_post():
	if 'drop' in request.form:
		s = request.form['drop']
		return s
		
# dashboard-courseinfo
@app.route('/test/dashboard-courseinfo-<id>')
def test_dashboard_courseinfo(id):
	x = ('123', 'Wang', 'CS')
	y = ('456', 'Peng', 'ME')
	student = [ x, y ]
	return render_template(
		'dashboard-courseinfo.html', 
		student = student, 
		description = '你好吗我很好'.decode('utf-8')
	)
	
@app.route('/test/welcome')
def test_welcome():
	return render_template('welcome.html')

@app.route('/test/welcome', methods=['POST'])
def gologin():
	return redirect('/test/login')

@app.route('/test/login')
def login():
	return render_template('login.html')

app.run(debug = True)
