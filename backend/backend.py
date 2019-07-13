#coding:utf-8
import json
from flask import Flask, session, request, redirect, jsonify, send_file, render_template
import pymysql as MySQLdb
import ans
import json
import coloredlogs
import logging
import os

MySQLdb.install_as_MySQLdb()
app = Flask(__name__)
app.secret_key = 'seasdf'
conn = MySQLdb.connect(
    host=os.getenv('DB_URL') or 'localhost',
    user=os.getenv('DB_USER') or 'username',
    passwd=os.getenv('DB_PWD') or 'password',
    db=os.getenv('DB_NAME') or 'test2'
)
log = logging.getLogger(__name__)
coloredlogs.install(
    level='INFO',
    logger=log
)


def execute_sql(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return cursor.fetchone()


def merge_data(data):
    t = [i['time'] for i in data]
    x = [i['x'] for i in data]
    y = [i['y'] for i in data]
    return [t, x, y]


def verify(data):
    return len(data) == 3 and len(data[0]) >= 3


@app.route('/show_session')
def ses():
    return json.dumps(dict(session))


#前后端连接
@app.route('/api/submit', methods=['POST'])
def submit():
    if 'username' not in session.keys():
        return 'illeagal request'
    data = json.loads(request.get_data())
    _data = []
    for i in data:
        _data += i['points']
    _data = merge_data(_data)

    if 'password' not in session.keys():
        true_data = execute_sql(
            f"SELECT sign FROM user WHERE username=\"{session['username']}\";"
        )
        result = ans.match(json.loads(true_data[0]), _data)
        if result:
            session['logged_in'] = True
        return str(result)

    if 'data' not in session.keys():
        log.info('设置session["data"]为空')
        session['data'] = []
    if verify(_data):
        session['data'].append(_data)
        log.info('获取到了一组合法签名数据')
        log.debug(session['data'])
        session['data'] = session['data']
    if len(session['data']) == 3:
        log.info('获取到了三组信息，成功注册')
        log.debug(session['data'])
        execute_sql(
            f'UPDATE user SET sign=\"{json.dumps(session["data"])}\" ' +
            f'WHERE username=\"{session["username"]}\" and password=\"{session["password"]}\"'
        )
        session.pop('username')
        session.pop('password')
        session.pop('data')
        return 'ret'
    return 'continue'


@app.route('/api/logout')
def logout():
    if 'logged_in' in session.keys():
        session.pop('logged_in')
    return redirect('/api/index')


@app.route('/api/index')
def index():
    if 'logged_in' not in session.keys():
        return render_template('guest.html')
    return render_template('user.html', cookies=session)

#干什么的？
# @app.route('/api/redict')
# def detail():
#     return send_file("./frontpage.html")

#注册
@app.route('/api/register', methods=['POST'])
def reigster():
    username = request.form['username']
    password = request.form['password']
    username = username.replace('\"', '')
    password = password.replace('\"', '')
    ret = execute_sql(
        f'SELECT username FROM user WHERE username=\"{username}\"')
    if ret is not None and len(ret) > 0:
        return 'this username has been registered'
    session['username'] = username
    session['password'] = password
    execute_sql(
        f"insert into user (id,username,password,sign) values (NULL,\"{username}\",\"{password}\",'');"
    )
    return redirect('/static/sigpad.html')

#登陆
@app.route('/api/login', methods=['POST'])
def login():
    username = request.form['username']
    session['username'] = username.replace('\"', '')
    return redirect('/static/sigpad.html')

#初始化数据库
@app.route('/api/db_init', methods=['GET'])
def db_init():
    init_sqls = [
        "DROP TABLE IF EXISTS user",
        "CREATE TABLE user (\
            id int primary key auto_increment,\
            username varchar(50) NOT NULL,\
            password varchar(50) NOT NULL,\
            sign text NOT NULL\
        );",
        "INSERT INTO user (id,username,password,sign) VALUES (NULL,'admin','admin','');"
    ]
    for i in init_sqls:
        execute_sql(i)
    return 'init success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
