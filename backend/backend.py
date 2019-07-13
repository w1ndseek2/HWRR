# coding:utf-8
import json
from flask import Flask, session, request, redirect, send_file, render_template
import ans
import json
from utils import (
    getLoggger,
    merge_data,
    verify,
    execute_sql
)

app = Flask(__name__)
app.secret_key = 'seasdf'
log = getLoggger()


@app.route('/show_session')
def ses():
    return json.dumps(dict(session))


# 注册
@app.route('/api/register', methods=['POST'])
def pre_register():
    username = request.form['username']
    password = request.form['password']
    username = username.replace('\"', '')
    password = password.replace('\"', '')
    ret = execute_sql(
        'SELECT username FROM user WHERE username=%(username)s',
        username=username
    )
    if ret is not None and len(ret) > 0:
        return 'this username has been registered'
    session['username'] = username
    session['password'] = password
    session['action'] = 'register'
    return redirect('/static/sigpad.html')


def register(_data):
    if session['username'] not in register_data.keys():
        log.info('设置register_data[session[\'username\']]为空')
        register_data[session['username']] = []
    if verify(_data):
        register_data[session['username']].append(_data)
        log.info('获取到了一组合法签名数据')
        log.debug(_data)
    if len(register_data[session['username']]) == 3:
        log.info('获取到了三组信息，成功注册')
        log.debug('所有数据:')
        log.debug(register_data[session['username']])
        execute_sql(
            "INSERT INTO user (id,username,password,sign) values (\
                NULL, %(username)s, %(password)s, %(sign_data)s\
            )",
            username=session['username'],
            password=session['password'],
            sign_data=json.dumps(register_data[session["username"]])
        )
        register_data.pop(session['username'])
        session.pop('username')
        session.pop('password')
        return 'ret'
    return 'continue'


# 登陆
@app.route('/api/login', methods=['POST'])
def pre_login():
    username = request.form['username']
    session['username'] = username.replace('\"', '')
    session['action'] = 'login'
    return redirect('/static/sigpad.html')


def login(_data):
    true_data = execute_sql(
        "SELECT sign FROM user WHERE username=%(username)s",
        username=session['username']
    )
    result = ans.match(json.loads(true_data[0]), _data)
    if result:
        session['logged_in'] = True
    return str(result)


register_data = {}


# 前后端连接
@app.route('/api/submit', methods=['POST'])
def submit():
    if 'username' not in session.keys():
        return 'illegal request'
    data = json.loads(request.get_data())
    _data = []
    for i in data:
        _data += i['points']
    _data = merge_data(_data)

    if session['action'] == 'login':
        return login(_data)
    elif session['action'] == 'register':
        return register(_data)
    else:
        return 'unexpected action'


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


@app.route('/api/update')
def detail():
    username = request.form['username']
    password = request.form['password']
    username = username.replace('\"', '')
    ret = execute_sql(
        f'SELECT password FROM user WHERE username=\"{username}\"'
    )
    if ret[0] != password:
        return render_template('wrong_pass.html')
    return send_file("./frontpage.html")


# 初始化数据库
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
