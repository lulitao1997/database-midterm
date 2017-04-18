
# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, request, redirect, flash, g
import pymysql
import json
import hashlib
from flask_bootstrap import Bootstrap
app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.secret_key = 'really_strong_psw'
db = pymysql.connect(host='127.0.0.1', port=3306, password="", user='root', database='edu_manage')

# def get_authed_user():
#     return get_user(session.get('username', None))

@app.before_request
def before_request():
    g.name = session.get('name', None)
    g.id = session.get('id', None)
    g.url_path = request.path
    if g.id is None and g.url_path not in {'/', '/login', '/please_login'}:
        return redirect('/please_login')

@app.route('/')
def page_home():
    if g.id: return redirect('dashboard-coursespossessed')
    return render_template('welcome.html')

@app.route('/please_login')
def page_please_login():
    return render_template('please-login.html')

@app.route('/logout')
def page_logout():
    flash('登出成功', 'success')
    del session['id']
    del session['name']
    return redirect('/')

@app.route('/login')
def page_login():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def page_login_post():
    id = request.form['username']
    psw = request.form['password']
    cursor = db.cursor()
    is_stu = False;
    if len(id)==11:
        cursor.execute('select sno, psw, sname from student where sno=%s', [id])
        is_stu = True
    else:
        cursor.execute('select tno, psw, tname from teacher where tno=%s', [id])
    result = cursor.fetchall()
    if len(result)==0 or psw!=result[0][1]: # TODO: change to hash
        flash('用户名或密码错误', 'error')
        return redirect('/login')
    name = result[0][2]
    session['id'] = result[0][0]
    session['name'] = name
    flash("欢迎：" + name + u"。登入成功！", 'success')
    return redirect('/')

def hash(psw):
    m = hashlib.sha256()
    m.update(psw.encode('utf-8'))
    return m.hexdigest

@app.route('/dashboard-coursesavailable')
def dashboard_coursesavailable():
    pass
	# computer = dict()
	# computer['cid']=12345
	# computer['cells'] = ['1-1','2-2','3-3']
	# computer['info'] = ('123435', 'computer', 'wang', '1', '100')
	# computer['done'] = True
	# cs = { 'cid': 123, 'cells': ['1-3','4-5'], 'info': ('123', 'cs', 'wang', '1', '100'), 'done': False }
	# course = [computer, cs]
	# cnameincell = [['hellooooooo' for col in range(15)] for row in range(8)]
	# return render_template('dashboard-coursesavailable.html', pageamount=10, pagenumber=10, course = course, cnameincell = cnameincell)
    # return str(len(courses))


@app.route('/dashboard-coursesavailable', methods=['POST'])
def dashboard_coursesavailable_post():
	if 'select' in request.form:
		s = request.form['select']
		return s
	elif 'search' in request.form:
		return request.form['cname']
	else:
		return redirect('test.login')

@app.route('/dashboard-coursespossessed')
def page_course_possessed():
    cursor = db.cursor();
    cursor.execute("""
        select distinct cno, cname, grade, credit, capacity from course natural join performance
        where sno=%s""", g.id)
    cno_l = cursor.fetchall()
    courses = list()
    cnameincell = [['' for _ in range(15)] for _ in range(8)]
    for c in cno_l:
        cursor.execute("""
            select wnum, cnum from course_time
            where cno=%s""", c[0])
        days = cursor.fetchall()
        cells = ['{}-{}'.format(*i) for i in days]
        cid = c[0].replace('.','')
        # c is info
        courses.append({'cid':cid, 'cells':cells, 'info':c})
        for d in days: cnameincell[d[0]][d[1]] = c[1]

    return render_template('dashboard-coursesavailable.html', pageamount=10, pagenumber=10, course=courses, cnameincell=cnameincell)

if __name__ == '__main__':
    app.run(debug=True)
