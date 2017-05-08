
# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, request, redirect, flash, g
import pymysql
import json
import hashlib
from flask_bootstrap import Bootstrap
app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.secret_key = 'really_strong_psw'
db = pymysql.connect(host='127.0.0.1', port=3306, password="", user='root', database='edu_manage', charset='utf8')

# page_stu = {'/dashboard-courseinfo', '/dashboard-coursespossessed', '/dashboard-teacherinfo', '/dashboard-coursesavailable', '/dashboard-courses-done'}
page_teacher = {'/tdashboard-courseinfo', '/tdashboard-teacherinfo', '/tdashboard-coursespossessed'}
@app.before_request
def before_request():
    g.username = session.get('name', None)
    g.id = session.get('id', None)
    g.url_path = request.path
    g.is_stu = session.get('is_stu', None)
    print("URL is: " + g.url_path)
    if g.id is None and g.url_path not in {'/', '/login', '/please_login', '/adminlogin'}:
        return redirect('/login')
    # if g.url_path!='/' and g.is_stu and g.url_path not in page_stu or not g.is_stu and g.url_path not in page_teacher:
    #     return redirect('/')

@app.route('/')
def page_home():
    if g.is_stu: return redirect('dashboard-coursespossessed')
    elif g.id not in ADMIN_ACCOUNT: return redirect('tdashboard-coursespossessed')
    elif g.id is not None: return redirect('/admin_manage')
    else: return render_template('welcome.html')

@app.route('/please_login')
def page_please_login():
    return render_template('please-login.html')

@app.route('/logout')
def page_logout():
    flash('登出成功', 'success')
    try:
        del session['id']
        del session['name']
        del session['is_stu']
    except:
        pass
    return redirect('/')

@app.route('/login')
def page_login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def page_login_post():
    id = request.form['username']
    psw = request.form['password']
    # return str(request.form)
    cursor = db.cursor()
    is_stu = False
    if len(id)==11:  # Student
        cursor.execute('select sno, psw, sname from student where sno=%s', [id])
        is_stu = True
    else: # Teacher
        cursor.execute('select tno, psw, tname from teacher where tno=%s', [id])
    result = cursor.fetchall()
    if len(result)==0 or hash(id+psw)!=result[0][1]: # TODO: change to hash
        flash('用户名或密码错误', 'error')
        return redirect('/login')
    name = result[0][2]
    session['id'] = result[0][0]
    session['name'] = name
    session['is_stu'] = is_stu
    flash("欢迎：" + name + "。登入成功！", 'success')
    return redirect('/')

@app.route('/adminlogin')
def page_adminlogin():
    return render_template('adminlogin.html')

ADMIN_ACCOUNT = {"admin":"123456"}

@app.route('/adminlogin', methods=['POST'])
def page_adminlogin_post():
    id = request.form['username']
    psw = request.form['password']

    if id not in ADMIN_ACCOUNT or ADMIN_ACCOUNT[id]!=psw: # TODO: change to hash
        flash('用户名或密码错误', 'error')
        return redirect('/adminlogin')
    session['id'] = id
    session['name'] = 'admin'
    flash("欢迎：admin" + "。登入成功！", 'success')
    return redirect('/admin_manage')

SEMESTER = 2016

@app.route('/admin_manage')
def page_admin_manage():
    return render_template('/admin_manage.html', semester=SEMESTER)


from roll import roll
@app.route('/admin_manage', methods=['POST'])
def page_admin_manage_post():
    global SEMESTER
    SEMESTER = SEMESTER+1
    if roll(db, SEMESTER) < 0:
        flash("归档数据时出现错误","error")
    else:
        flash("归档以及导入新学期成功，已经进入下一个学期",'success')
    return render_template('/admin_manage.html', semester=SEMESTER)

def hash(psw):
    m = hashlib.sha256()
    m.update(psw.encode('utf-8'))
    return m.hexdigest()

def run_sql(sqlcmd, argtuple=None, columnname=None):
    ans = list()
    with db.cursor() as cursor:
        cursor.execute(sqlcmd, argtuple)
        for c in cursor:
            yield dict(zip(columnname, c))

def get_courses(sqlcmd, argtuple=None, columnname=None, hascells=True): # TODO: return a iterator
    courses = list()
    for cou in run_sql(sqlcmd, argtuple, columnname):
        with db.cursor() as c2:
            if hascells:
                c2.execute("""
                    select wnum, cnum from course_time
                    where cno=%s""", cou["cno"])
                cou["cells"] = ['{}-{}'.format(*i) for i in c2]
            cou["teacher"] = [j for j in run_sql("select tno, tname from teacher natural join teach_rel where cno=%s", cou["cno"], ["tno", "tname"])]
            cou["cid"] = cou["cno"].replace('.','_')
        # print(str(cou["cells"]))
        courses.append(cou)
    return courses

def get_stu_table():
    cursor = db.cursor();
    cursor.execute("""
        select wnum, cnum, cname from course_time natural join performance natural join course
        where sno=%s""", [g.id]) # TODO: grade is NULL
    cnameincell = [['' for _ in range(15)] for _ in range(8)]
    for (w,c,name) in cursor:
        cnameincell[w][c] = name
    return cnameincell

PAGE_NUM = 10
AVAIL_STR = """
select cno, cname, credit, capacity from course as AA
where cno not in (
    select cno from performance where sno=@sid
) and not exists (
    select * from course_time A, course_time B, performance C
    where (A.wnum,A.cnum)=(B.wnum,B.cnum) and B.cno=C.cno and A.cno=AA.cno and C.sno=%s
) """

@app.route('/dashboard-coursesavailable-<pagenumber>')
def dashboard_coursesavailable(pagenumber):
    courses = get_courses(AVAIL_STR + "limit %s, %s", [g.id, (int(pagenumber)-1)*PAGE_NUM, PAGE_NUM], ["cno", "cname", "credit", "cap"])
    return render_template('dashboard-coursesavailable.html', pageamount=10, pagenumber=int(pagenumber), course=courses, cnameincell=get_stu_table(), sidebar_name='coursesavailable')

@app.route('/dashboard-coursesavailable-<pagenumber>', methods=['POST'])
def dashboard_coursesavailable_post(pagenumber):
    cursor = db.cursor()
    if 'select' in request.form:
        try:
            cursor.execute('insert into performance values(%s, %s, NULL)', [g.id, request.form['select']])
            db.commit()
        except:
            db.rollback()
        return redirect(g.url_path)
    elif 'search' in request.form:
        where_clause = ''
        for attr in ('cno', 'cname'):
            a = request.form[attr]
            if (a):
                where_clause += (' and ' if where_clause else '') + "{} like '%%{}%%'".format(attr,a)
        qcmd = 'select * from ('+AVAIL_STR+') as BB ' + (' where ' if where_clause else '') + where_clause + 'limit %d, %d' % ((int(pagenumber)-1)*PAGE_NUM, PAGE_NUM)
        courses = get_courses(qcmd, [g.id], ["cno", "cname", "credit", "cap"])
        # return str(courses)
        return render_template('dashboard-coursesavailable.html', pageamount=10, pagenumber=int(pagenumber), course=courses, cnameincell=get_stu_table(), sidebar='coursesavailable')
    else:
        return redirect('test.login')

@app.route('/dashboard-coursespossessed')
def page_course_possessed():
    courses = get_courses("""
        select distinct cno, cname, credit, capacity from course natural join performance as A
        where sno=%s""", [g.id], ["cno", "cname", "credit", "cap"])
    return render_template('dashboard-coursespossessed.html', course=courses, cnameincell=get_stu_table(), sidebar_name = 'coursespossessed')
    # return str(get_stu_table())

@app.route('/dashboard-coursespossessed', methods=['POST'])
def dashboard_coursespossessed_post():
    # return str(request.form)
    if 'drop' in request.form: # 请求退课
        print("begin drop")
        cno = request.form['drop'] # 得到课程编号
        cursor = db.cursor()
        try:
            cursor.execute('delete from performance where sno=%s and cno=%s', [g.id, cno])
            db.commit()
        except:
            return "fucked"
            db.rollback()
        return redirect(g.url_path)
    else:
        return redirect('/')

@app.route('/dashboard-courseinfo-<cid>')
def page_courseinfo(cid):
    c2 = db.cursor()
    c2.execute("select description from course where cno=%s", cid)
    # return str(c2.fetchall())
    return render_template(
        'dashboard-courseinfo.html',
        sidebar_name='courseinfo', # 激活侧边栏高亮
        student = None,
        description = c2.fetchall()[0][0] # 课程描述
    )
    return render_template(
        'dashboard-courseinfo.html',
        student=cursor.fetchall(),
        description=c2.fetchall()[0][0]
    )

@app.route('/dashboard-coursesdone-<year>')
def page_coursedone_y(year):
    if year == SEMESTER:
        with db.cursor() as cursor:
            cursor.execute("""
                select SUM(grade*credit)/SUM(credit), SUM(credit) from performance natural join course
                where sno=%s and grade is not NULL
                group by sno""", [g.id])
            # return str(cursor.fetchall())
            try:
                (gpa, sum_credit) = cursor.fetchall()[0]
            except:
                (gpa, sum_credit) = (None, None)
        courses = get_courses("""select distinct cno, cname ,credit, grade from performance natural join course as A
        where sno=%s and grade is not NULL""", [g.id], ["cno", "cname", "credit", "grade"], hascells=False)
    else:
        with db.cursor() as cursor:
            cursor.execute("""
                select SUM(grade*credit)/SUM(credit), SUM(credit) from past_performance natural join past_course
                where sno=%s and grade is not NULL and stime=%s
                group by sno""", [g.id, year])
            # return str(cursor.fetchall())
            try:
                (gpa, sum_credit) = cursor.fetchall()[0]
            except:
                (gpa, sum_credit) = (None, None)
        courses = get_courses("""select distinct cno, cname ,credit, grade from past_performance natural join past_course as A
        where sno=%s and grade is not NULL and stime=%s""", [g.id, year], ["cno", "cname", "credit", "grade"], hascells=False)

    return render_template(
        'dashboard-coursesdone.html',
        course = courses,
        gpa = gpa,
        credit = sum_credit,
        sidebar_name = 'coursesdone',
        years = list(range(2016, SEMESTER+1))
    )

@app.route('/dashboard-coursesdone')
def page_coursedone():
    return page_coursedone_y(SEMESTER)

@app.route('/dashboard-coursesdone', methods=['POST'])
def dashboard_coursesdone_post():
    if 'relearn' in request.form: # 请求重修
        cno = request.form['relearn']
        cursor = db.cursor()
        try:
            cursor.execute('delete from performance where sno=%s and cno=%s', [g.id, cno])
            cursor.execute('insert into performance values(%s, %s, NULL)', [g.id, cno])
            db.commit()
        except:
            flash("该课程与当前选课冲突", 'error')
            db.rollback()
        return redirect(g.url_path)
    return 'fucked!'

@app.route('/dashboard-teacherinfo-<tno>')
def page_teacher_info(tno):
    it = run_sql("select tname, prof from teacher where tno=%s", [tno], ["tname", "prof"])
    return render_template(
        'dashboard-teacherinfo.html',
        teacher = next(it),
        sidebar_name = 'teacherinfo',
        ifedit = dict()
    )

def get_sturnk():
    it = run_sql("""select sno, sname, SUM(credit*grade)/SUM(credit) as gpa, SUM(credit) as sumc
    from student natural join performance natural join course
    where grade is not NULL
    group by sno, sname
    having gpa is not NULL
    order by gpa DESC
    """, None, ["sno", "sname", "gpa", "sumc"])
    # return str([stu for stu in it])
    stunum = 0
    rnk = 0
    students = list()
    prev_gpa = -1
    pos = 0
    for stu in it:
        if prev_gpa != float(stu["gpa"]):
            prev_gpa = float(stu["gpa"])
            rnk = rnk+1
        stu["rank"] = rnk
        if stu["sno"]!=g.id:
            stu["sno"]="**********"
            stu["sname"]="***"
        else: pos = stunum
        students.append(stu)
        stunum = stunum+1
    return (pos, stunum, students)


@app.route('/dashboard-sturank-<pagenumber>')
def page_sturank(pagenumber):
    (pos, stunum, students) = get_sturnk()
    pagenumber = int(pagenumber)
    return render_template("dashboard-sturank.html",
           sidebar_name='sturank',
           pageamount=int(stunum/PAGE_NUM),
           pagenumber=pagenumber,
           students = students[(pagenumber-1)*PAGE_NUM:pagenumber*PAGE_NUM])

@app.route('/dashboard-sturank')
def page_sturank_default():
    pos = get_sturnk()[0]
    # return str(get_sturnk()[1])
    return page_sturank(pos / PAGE_NUM + 1)

#--------------------------------------------tdashboard-------------------------------------------------------------------
#这里是给老师们用的dashboard，是给老师们用的是给老师们用的是给老师们用的是给老师们用的是给老师们用的是给老师们用的是给老师们用的
#-------------------------------------------------------------------------------------------------------------------------
def get_teacher_table():
    with db.cursor() as cursor:
        cursor.execute("""
            select wnum, cnum, cname from course_time natural join teach_rel natural join course
            where tno=%s""", [g.id])
        cnameincell = [['' for _ in range(15)] for _ in range(8)]
        for (w,c,name) in cursor:
            cnameincell[w][c] = name
    return cnameincell
@app.route('/tdashboard-coursespossessed')
def tdashboard_coursespossessed():
    courses = get_courses("""
        select cno, cname, credit, capacity from course natural join teach_rel as A
        where tno=%s""", [g.id], ["cno", "cname", "credit", "cap"])
    cnameincell = get_teacher_table()
    return render_template (
        'tdashboard-coursespossessed.html',
        course = courses,
        cnameincell = cnameincell,
        sidebar_name = 'coursespossessed'
    )

@app.route('/tdashboard-courseinfo-<cno>')
def tdashboard_coursesinfo(cno):
    # x = { 'sno' : '123', 'sname' : 'Wang', 'sex' : 'M' }
    # y = { 'sno' : '456', 'sname' : 'Peng', 'sex' : 'F' }
    # student = [ x, y ] # 学生花名册

    with db.cursor() as c:
        c.execute("select description from course where cno=%s", [cno])
        description = c.fetchall()[0][0]
    return render_template(
        'tdashboard-courseinfo.html',
        sidebar_name='courseinfo', # 激活侧边栏高亮
        student = run_sql("select sno, sname, sex, grade from student natural join performance where cno=%s", [cno], ["sno", "sname", "sex", "grade"]),
        description = description# 课程描述
    )

@app.route('/tdashboard-courseinfo-<cno>', methods=['POST'])
def tdashboard_coursesinfo_post(cno):
    print(str(request.form))
    with db.cursor() as c:
        if 'drop' in request.form:
            try:
                c.execute("delete from performance where sno=%s and cno=%s", [request.form['drop'], cno])
                db.commit()
            except:
                db.rollback()
            # return (u'听说你想踢掉我(%s)？那你还是太naive了'%request.form['drop'])
        elif 'update' in request.form:
            try:
                for sno in request.form:
                    if len(sno)==11:
                        c.execute("update performance set grade=%s where sno=%s and cno=%s", [request.form[sno], sno, cno])
                db.commit()
            except:
                db.rollback()
                flash("输入的分数有误", 'error')
    return redirect(g.url_path)

@app.route('/tdashboard-teacherinfo')
def tdashboard_teacherinfo():
    it = run_sql("select tname, prof, email, tel from teacher where tno=%s", [g.id], ["tname", "prof", "email", "phno"])
    ifedit = { 'email', 'phno' } # 一个集合，表示可以修改的栏目。
    return render_template(
        'tdashboard-teacherinfo.html',
        teacher = next(it),
        sidebar_name = 'teacherinfo',
        ifedit = ifedit
    )

@app.route('/tdashboard-teacherinfo', methods = ['POST'])
def tdashboard_teacherinfo_post():
    print(str(request.form))
    with db.cursor() as c:
        try:
            if 'editemail' in request.form:
                c.execute("update teacher set email=%s where tno=%s",[request.form["email"], g.id])
            if 'editphno' in request.form:
                c.execute("update teacher set tel=%s where tno=%s",[request.form["phno"], g.id])
            db.commit()
        except:
            db.rollback()
            flash("输入的信息有误",'error')
    return redirect(g.url_path)

from config import *
import sys
if __name__ == '__main__':
    if '--first' in sys.argv: reset()
    app.run(debug=True)
