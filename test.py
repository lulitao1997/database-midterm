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
app.secret_key = 'really_strong_psw'

# 废弃
@app.route('/dashboard-curriculum')
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

# 请求登出
@app.route('/logout')
def test_logout():
	return (u'你已经登出啦！你是坠棒的！')
	
# dashboard-coursesavailable 可选课程
@app.route('/dashboard-coursesavailable-<pagenumber>') # pagenumber: 当前的的页码，作为传入参数，默认(初始)为1
def test_dashboard_coursesavailable(pagenumber):
	computer = dict()
	computer['cid']=123435
	computer['cells'] = ['1-1','2-2','3-3']
	computer['info'] = ('1234.35', 'computer', 'wang', '1', '100')
	computer['done'] = True
	
	cs = { 
		'cid': 123, 
		'cells': ['1-3','4-5'], 
		'info': ('123', 'cs', 'wang', '1', '100'), 
		'done': False # 是否已经修过
	}
	course = [computer, cs]
	cnameincell = [['hellooooooo' for col in range(15)] for row in range(8)]
	return render_template(
		'dashboard-coursesavailable.html', 
		pageamount = 10, # 所有的页码的数量
		pagenumber = int(pagenumber), # 当前页码
		course = course, # 传入的course，在list中使用
		cnameincell = cnameincell, # 需要染色的格子
		sidebar_name = 'coursesavailable' # sidebar_name　用来激活侧边栏对应高亮
	)

@app.route('/dashboard-coursesavailable-<pagenumber>', methods=['POST'])
def test_dashboard_coursesavailable_post(pagenumber):
	if 'select' in request.form: # 请求选课
		cno = request.form['select']
		return cno
	elif 'search' in request.form: # 请求检索
		cno = request.form['cno']
		cname = request.form['cname']
		tname = request.form['tname']
		return cname
	else: # 逻辑上应该不会出现这种情况
		return redirect('/welcome')
		
# dashboard-coursespossessed 已选课程
@app.route('/dashboard-coursespossessed')
def test_dashboard_coursespossessed():
	computer = dict()
	computer['cid'] = 12345
	computer['cells'] = ['1-1','2-2','3-3']
	computer['info'] = ('123435', 'computer', 'wang', '1', '100')
	computer['done'] = True
	cs = { 
		'cid': 123, 
		'cells': ['1-3','4-5'], 
		'info': ('123', 'cs', 'wang', '1', '100'), 
		'done': False # 是否已经修过
	}
	course = [computer, cs]
	cnameincell = [['hellooooooo' for col in range(15)] for row in range(8)]
	return render_template(
		'dashboard-coursespossessed.html', 
		course = course, 
		cnameincell = cnameincell,
		sidebar_name = 'coursespossessed'
	)

@app.route('/dashboard-coursespossessed', methods=['POST'])
def test_dashboard_coursespossessed_post():
	if 'drop' in request.form: # 请求退课
		cno = request.form['drop'] # 得到课程编号
		return cno
	else:
		return redirect('login.html')

# dashboard-courseinfo 课程信息
@app.route('/dashboard-courseinfo-<cno>')
def test_dashboard_courseinfo(cno):
	x = ('123', 'Wang', 'CS')
	y = ('456', 'Peng', 'ME')
	student = [ x, y ] # 学生花名册
	return render_template(
		'dashboard-courseinfo.html', 
		sidebar_name='courseinfo', # 激活侧边栏高亮
		student = student, 
		description = u'你好吗我很好' # 课程描述
	)
	
# dashboard-courses-done 已修课程
@app.route('/dashboard-coursesdone')
def test_dashboard_coursesdone():
	computer = dict()
	computer['cid'] = 12345
	computer['cells'] = ['1-1','2-2','3-3']
	computer['info'] = ('123435', 'computer', 'wang', '1', 'A')
	computer['done'] = True
	cs = { 
		'cid': 12301, # cid: cno without dot
		'info': (
			'123.01', # cno
			'cs',  # cname
			'wang',# tname
			'1', # credit
			'F' # grade
		), 
	}
	course = [computer, cs]
	return render_template(
		'dashboard-coursesdone.html', 
		course = course, 
		sidebar_name = 'coursesdone'
	)

@app.route('/dashboard-coursesdone', methods = ['POST'])
def test_dashboard_coursesdone_post():
	if 'relearn' in request.form: # 请求重修
		cno = request.form['relearn']
	return (u'这句话没什么卵用')
	
@app.route('/welcome')
def test_welcome():
	return render_template('welcome.html')

@app.route('/welcome', methods=['POST'])
def gologin():
	return redirect('/login')

@app.route('/login')
def login():
	flash(u'我来试一下flash','error')
	return render_template('login.html')

app.run(debug = True)
