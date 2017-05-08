# -*- coding: utf-8 -*-
from flask import Flask, render_template, flash, redirect, url_for, session, request, g
from flask_wtf import Form
from wtforms import IntegerField, SubmitField
from wtforms.validators import Required, NumberRange
from flask_bootstrap import Bootstrap
import pymysql
import jinja2
#import numpy as np

app = Flask(__name__)
app.secret_key = 'really_strong_psw'

@app.before_request
def before_request():
    g.username = 'Ashitaka97'
    
@app.route('/')
def page_home():
    return render_template('welcome.html')
    
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

	
#--------------------------------------------dashboard--------------------------------------------------------------------
#这里是给学生们用的dashboard，是给学生们用的是给学生们用的是给学生们用的是给学生们用的是给学生们用的是给学生们用的是给学生们用的
#-------------------------------------------------------------------------------------------------------------------------

# dashboard-coursesavailable 可选课程
@app.route('/dashboard-coursesavailable-<pagenumber>') # pagenumber: 当前的的页码，作为传入参数，默认(初始)为1
def test_dashboard_coursesavailable(pagenumber):
	cs = {
		'cid': 123,
		'cells': ['1-3','4-5'],
		'cno' : '12.3',
		'cname' : 'cs',
		'teacher' : [
			{ 'tno' : '123', 'tname' : u'王尔德' },
			{ 'tno' : '456', 'tname' : u'王缺德' }
		],
		'credit' : '2',
		'cap' : '100',
		'done': False # 是否已经修过
	}
	course = [ cs ]
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
	cs = {
		'cid': 123,
		'cells': ['1-3','4-5'],
		'cno' : '12.3',
		'cname' : 'cs',
		'teacher' : [
			{ 'tno' : '123', 'tname' : u'王尔德' },
			{ 'tno' : '456', 'tname' : u'王缺德' }
		],
		'credit' : '2',
		'cap' : '100',
		'done': False # 是否已经修过
	}
	course = [ cs ]
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
	student = [x, y] # 学生花名册，如果想隐藏，可赋值为None
	return render_template(
		'dashboard-courseinfo.html',
		sidebar_name='courseinfo', # 激活侧边栏高亮
		student = None,
		description = u'你好吗我很好' # 课程描述
	)
# dashboard-teacherinfo 教师信息
@app.route('/dashboard-teacherinfo-<tno>')
def test_dashboard_teacherinfo(tno):
	teacher = { 'tname': u'王尔德', 'prof': u'教授', 'email': '233@fudan.edu.cn', 'phno': '1234567' };
	ifedit = {} # 一个集合，表示可以修改的栏目，默认学生不能修改。
	return render_template(
		'dashboard-teacherinfo.html',
		teacher = teacher,
		sidebar_name = 'teacherinfo',
		ifedit = ifedit
	)
	
# dashboard-courses-done 已修课程
@app.route('/dashboard-coursesdone-<year>')
def test_dashboard_coursesdone(year):
	cs = {
		'cno' : '12.3',
		'cname' : 'cs',
		'teacher' : [
			{ 'tno' : '123', 'tname' : u'王尔德' },
			{ 'tno' : '456', 'tname' : u'王缺德' }
		],
		'credit' : '2',
		'grade' : 'F'		
	}
	course = [cs]
	years = [ 2015, 2016, 2017 ]
	return render_template(
		'dashboard-coursesdone.html',
		course = course,
		gpa = '4.1',
		credit = '150.5',
		sidebar_name = 'coursesdone',
		years = years
	)

@app.route('/dashboard-coursesdone', methods=['POST'])
def test_dashboard_coursesdone_post():
	if 'relearn' in request.form: # 请求重修
		#cno = request.form['relearn']	
		#cno = cno[:-2] + '.' + cno[-2:]
		#cursor = db.cursor()
		#try:
		#	cursor.execute('delete from performance where sno=%s and cno=%s', [g.id, cno])
		#	cursor.execute('insert into performance values(%s, %s, NULL)', [g.id, cno])
		return "hello"
	
#--------------------------------------------tdashboard-------------------------------------------------------------------
#这里是给老师们用的dashboard，是给老师们用的是给老师们用的是给老师们用的是给老师们用的是给老师们用的是给老师们用的是给老师们用的
#-------------------------------------------------------------------------------------------------------------------------

#我的信息
@app.route('/tdashboard-coursespossessed') 
def test_tdashboard_coursespossessed():
	cs = {
		'cid': 123,
		'cells': ['1-3','4-5'],
		'cno' : '12.3',
		'cname' : 'cs',
		'teacher' : [
			{ 'tno' : '123', 'tname' : u'王尔德' },
			{ 'tno' : '456', 'tname' : u'王缺德' }
		],
		'credit' : '2',
		'cap' : '100',
	}
	course = [ cs ]
	cnameincell = [['hellooooooo' for col in range(15)] for row in range(8)]
	return render_template (
		'tdashboard-coursespossessed.html', 
		course = course, 
		cnameincell = cnameincell,
		sidebar_name = 'coursespossessed'
	)


#课程信息
@app.route('/tdashboard-courseinfo-<cno>')
def test_tdashboard_coursesinfo(cno):
	x = { 'sno' : '123', 'sname' : 'Wang', 'sex' : 'M' }
	y = { 'sno' : '456', 'sname' : 'Peng', 'sex' : 'F' }
	student = [ x, y ] # 学生花名册
	return render_template(
		'tdashboard-courseinfo.html',
		sidebar_name='courseinfo', # 激活侧边栏高亮
		student = student,
		description = u'你好吗我很好' # 课程描述
	)
	
@app.route('/tdashboard-courseinfo-<cno>', methods=['POST'])
def test_tdashboard_coursesinfo_post(cno):
	if 'drop' in request.form:
		return (u'听说你想踢掉我(%s)？那你还是太naive了'%request.form['drop'])


#教师信息	
@app.route('/tdashboard-teacherinfo-<tno>')
def test_tdashboard_teacherinfo(tno):
	teacher = { 'tname': u'王尔德', 'prof': u'教授', 'email': '233@fudan.edu.cn', 'phno': '1234567' };
	ifedit = { 'email', 'phno' } # 一个集合，表示可以修改的栏目。
	return render_template(
		'tdashboard-teacherinfo.html',
		teacher = teacher,
		sidebar_name = 'teacherinfo',
		ifedit = ifedit
	)

@app.route('/tdashboard-teacherinfo-<tno>', methods = ['POST']) 
def test_tdashboard_teacherinfo_post(tno): 
	if 'editemail' in request.form:
		return u'想修改成%s？你想多啦！'%request.form['email']
	elif 'editphno' in request.form:
		return u'想修改成%s？你想多啦！'%request.form['phno']
		
#---------------------------------------------------------------------------------------------------

app.run(debug = True)
