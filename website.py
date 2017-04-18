
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
    if g.id is None and g.url_path not in {'/', '/login'}:
        return redirect('/')

@app.route('/')
def page_home():
    return render_template('welcome.html')

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
    # cursor.execute('select id,password from `user` where name=%s', [username])
    is_stu = False;
    if (len(id)==11):
        cursor.execute('select sno, psw, sname from student where sno=%s', [id])
        is_stu = True
    else:
        cursor.execute('select tno, psw, tname, from teacher where tno=%s', [id])
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

if __name__ == '__main__':
    app.run(debug=True)
