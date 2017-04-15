
# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, request, redirect, flash, g
import pymysql
import json
import hashlib

app = Flask(__name__, static_url_path='')
app.secret_key = 'really_strong_psw'
db = pymysql.connect(host='127.0.0.1', port=3306, password="", user='root', database='pj')

# def sql_wrapper(table_name, attributes, sql_override=None):
#     def func(id):
#         if (id == None): return None
#
#         cursor = dbConnection.cursor()
#         cursor.execute(sql_override if sql_override is not None else 'select ' + ','.join(
#             attributes) + ' from ' + table_name + ' where id=%s',
#                        [id])
#         result = cursor.fetchall()
#         if len(result) == 0:
#             return None
#         else:
#             ret = {}
#             for i in range(0, len(attributes)):
#                 ret[attributes[i]] = result[0][i]
#
#             return ret
#     return func

def get_authed_user():
    return get_user(session.get('user_id'), None)

@app.before_request
def before_request():
    g.authed_user = get_authed_user()
    g.url_path = request.path

@app.route('/auth/logout')
def page_logout():
    flash('登出成功', 'success')
    del session['user_id']
    return redirect('/')

@app.route('/auth/login')
def page_login():
    return render_template('login.html')

@app.route('/auth/login', methods = ['POST'])
def page_login_post():
    sno = request.form['username']
    psw = request.form['password']
    cursor = db.cursor()
    # cursor.execute('select id,password from `user` where name=%s', [username])
    cursor.execute('select sno, psw from from student where sno=%s', [sno])
    result = cursor.fetchall()

    if len(result)==0 or hash(psw+sno) != result[0][1]:
        flash('用户名或密码错误', 'error')
        return redirect('auth/login')

    session['user_id'] = result[0][0]

    # flash("欢迎：" + username + u"。登入成功！", 'success')
    return redirect('/')


def hash(psw):
    m = hashlib.sha256()
    m.update(psw.encode('utf-8'))
    return m.hexdigest

if __name__ == '__main__':
    app.run(debug=True)
