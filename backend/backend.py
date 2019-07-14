import json
from flask import Flask, session, request, redirect, send_file, render_template
import DynamicProcess
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


register_data = {}


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
        real = DynamicProcess.prepare_list(
            json.dumps(register_data[session["username"]])
        )
        real_v = DynamicProcess.prepare_value(real)
        execute_sql(
            "INSERT INTO user (username, password, sign_prepared, sign_val) values (\
                %(username)s, %(password)s, %(sign_prepared)s, %(sign_val)s\
            )",
            username=session['username'],
            password=session['password'],
            sign_prepared=real,
            sign_val=real_v
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
        "SELECT sign_prepared, sign_val FROM user WHERE username=%(username)s",
        username=session['username']
    )
    result, new_prepared = DynamicProcess.match(
        true_data[0], true_data[1],
        _data, limit=0.6
    )
    if result:
        execute_sql(
            'UPDATE user SET sign_val=%(sign_v)s WHERE username=%(username)s',
            sign_v=new_prepared,
            username=session['username']
        )
        session['logged_in'] = True
    return str(result)


@app.route('/api/update')
def pre_update():
    username = request.form['username']
    password = request.form['password']
    username = username.replace('\"', '')
    ret = execute_sql(
        'SELECT password FROM user WHERE username=%(username)s',
        username=username
    )
    if ret[0] != password:
        return render_template('wrong_pass.html')
    session['action'] = 'update'
    return redirect


def update(_data):
    return 'not implemented'


@app.route('/api/submit', methods=['POST'])
def submit():
    if 'username' not in session.keys():
        return 'illegal request'
    data = json.loads(request.get_data())
    _data = []
    for i in data:
        _data += i['points']
    _data = merge_data(_data)
    action = session['action']
    session.pop('action')
    if action == 'login':
        return login(_data)
    elif action == 'register':
        return register(_data)
    elif action == 'update':
        return update(_data)
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


# 初始化数据库
@app.route('/api/db_init', methods=['GET'])
def db_init():
    init_sqls = [
        "DROP TABLE IF EXISTS user",
        "CREATE TABLE user (\
            id int primary key auto_increment,\
            username varchar(50) NOT NULL,\
            password varchar(50) NOT NULL,\
            sign_prepared text,\
            sign_val text\
        );",
        "INSERT INTO user (username,password) VALUES ('admin','admin');"
    ]
    for i in init_sqls:
        execute_sql(i)
    return 'init success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
