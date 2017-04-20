
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

@app.route('/login', methods=['POST'])
def page_login_post():
    id = request.form['username']
    psw = request.form['password']
    cursor = db.cursor()
    is_stu = False
    if len(id)==11:  # Student
        cursor.execute('select sno, psw, sname from student where sno=%s', [id])
        is_stu = True
    else: # Teacher
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

def get_stu_courses(sqlcmd, argtuple=None): # TODO: return a iterator
    cursor = db.cursor();
    cursor.execute(sqlcmd, argtuple)
    courses = list()
    for c in cursor:
        c2 = db.cursor()
        c2.execute("""
            select wnum, cnum from course_time
            where cno=%s""", c[0])
        cells = ['{}-{}'.format(*i) for i in c2]
        cid = c[0].replace('.','')
        # c is info
        courses.append({'cid':cid, 'cells':cells, 'info':c})
    return courses

def get_stu_table():
    cursor = db.cursor();
    cursor.execute("""
        select wnum, cnum, cname from course_time natural join performance natural join course
        where sno=%s""", [g.id])
    cnameincell = [['' for _ in range(15)] for _ in range(8)]
    for (w,c,name) in cursor:
        cnameincell[w][c] = name
    return cnameincell

# @app.route('/dashboard-coursesavailable')
# def dashboard_coursesavailable():
#     courses = get_stu_courses("""
#     select cno, cname, (select group_concat(tname separator ', ') from teacher natural join teach_rel where cno=AA.cno) as teachers, credit, capacity from course as AA
#     where cno not in (
#         select cno from performance where sno=@sid
#     ) and not exists (
#         select * from course_time A, course_time B, performance C
#         where (A.wnum,A.cnum)=(B.wnum,B.cnum) and B.cno=C.cno and A.cno=AA.cno and C.sno=%s
#     )""", g.id)
#     return render_template('dashboard-coursesavailable.html', pageamount=10, pagenumber=10, course=courses, cnameincell=get_stu_table())

PAGE_NUM = 5
AVAIL_STR = """
select cno, cname, (select group_concat(tname separator ', ') from teacher natural join teach_rel where cno=AA.cno) as teachers, credit, capacity from course as AA
where cno not in (
    select cno from performance where sno=@sid
) and not exists (
    select * from course_time A, course_time B, performance C
    where (A.wnum,A.cnum)=(B.wnum,B.cnum) and B.cno=C.cno and A.cno=AA.cno and C.sno=%s
) """


@app.route('/dashboard-coursesavailable-<pagenumber>')
def dashboard_coursesavailable(pagenumber):
    courses = get_stu_courses(AVAIL_STR + "limit %s, %s", [g.id, (int(pagenumber)-1)*PAGE_NUM, PAGE_NUM])
    return render_template('dashboard-coursesavailable.html', pageamount=10, pagenumber=int(pagenumber), course=courses, cnameincell=get_stu_table())

@app.route('/dashboard-coursesavailable-<pagenumber>', methods=['POST'])
def dashboard_coursesavailable_post(pagenumber):
    cursor = db.cursor()
    if 'select' in request.form:
        # s = request.form['select']
        # return s
        try:
            cursor.execute('insert into performance values(@sid, @cid, NULL)', [g.id, request.form['select']])
            db.commit()
        except:
            db.rollback()
    elif 'search' in request.form:
        where_clause = ''
        for attr in ('cno', 'cname'):
            a = request.form[attr]
            if (a):
                where_clause += (' and ' if where_clause else '') + "{} like '%%{}%%'".format(attr,a)
        qcmd = 'select * from ('+AVAIL_STR+') as BB ' + (' where ' if where_clause else '') + where_clause + 'limit %d, %d' % ((int(pagenumber)-1)*PAGE_NUM, PAGE_NUM)
        # return qcmd
        # courses = get_stu_courses(qcmd, [g.id])
        # qcmd = """
        # select * from ( select cno, cname, (select group_concat(tname separator ', ') from teacher natural join teach_rel where cno=AA.cno) as teachers, credit, capacity from course as AA where cno not in ( select cno from performance where sno=@sid ) and not exists ( select * from course_time A, course_time B, performance C where (A.wnum,A.cnum)=(B.wnum,B.cnum) and B.cno=C.cno and A.cno=AA.cno and C.sno=%s ) ) where cno like %%LAWS130432.01%% limit 0, 5
        # """
        courses = get_stu_courses(qcmd, [g.id])
        # return str(courses)
        return render_template('dashboard-coursesavailable.html', pageamount=10, pagenumber=int(pagenumber), course=courses, cnameincell=get_stu_table())
        # return request.form['cname']
    else:
        return redirect('test.login')

@app.route('/dashboard-coursespossessed')
def page_course_possessed():
    courses = get_stu_courses("""
        select distinct cno, cname, (select group_concat(tname separator ', ')
        from teacher natural join teach_rel where cno=A.cno) as teachers, credit, capacity from course natural join performance as A
        where sno=%s""", [g.id])
    return render_template('dashboard-coursesavailable.html', pageamount=10, pagenumber=1, course=courses, cnameincell=get_stu_table())
    # return str(get_stu_table())

@app.route('/dashboard-courseinfo-<cid>')
def page_courseinfo(cid):
    cursor = db.cursor()
    cid = cid[:-2] + '.' + cid[-2:]
    cursor.execute("select * from performance where cno=%s", [cid])

    c2 = db.cursor()
    c2.execute('select description from course where cno=%s', [cid])
    
    return render_template(
        'dashboard-courseinfo.html',
        student=cursor.fetchall(),
        description=c2.fetchall()[0][0]
    )

if __name__ == '__main__':
    app.run(debug=True)
