import json
from flask import (
    Blueprint, session,
    request, redirect,
    send_file, render_template
)

import DynamicProcess

try:
    import backend.users
    from backend.utils import (
        getLoggger,
        merge_data,
        verify,
        execute_sql,
        cache
    )
except:
    import users
    from utils import (
        getLoggger,
        merge_data,
        verify,
        execute_sql,
        cache
    )

api = Blueprint('api', __name__)
api.secret_key = 'seasdf'
log = getLoggger()


@api.route('/show_info')
def ses():
    info = {'role': 'unknown'}
    if 'username' in session.keys():
        info = users.getInfo(username=session['username'])
    return json.dumps(info)


# 注册
@api.route('/register', methods=['POST'])
def pre_register():
    for i in ['username', 'password', 'role']:
        if i not in request.form.keys():
            return render_template('error.html', messages=['invalid request'])
    username = request.form['username']
    username = username.replace('\"', '')
    ret = execute_sql(
        'SELECT username FROM user WHERE username=%(username)s',
        username=username
    )
    if ret is not None and len(ret) > 0:
        return render_template('error.html', messages=[
            '用户名已存在',
            'this username has been registered'
        ])
    session['username'] = username
    session['password'] = request.form['password'].replace('\"', '')
    session['role'] = request.form['role'].replace('\"', '')
    session['action'] = 'register'
    return redirect('/page/sigpad')


def register(_data):
    if not cache.exists(session['username']):
        log.info('设置register_data[session[\'username\']]为空')
        cache.set(session['username'] + '.count', 0, ex=600)
        # expires in 10 minutes
    session['action'] = 'register'
    if verify(_data):
        cache.rpush(session['username'], json.dumps(_data))
        cache.incr(session['username'] + '.count')

        log.info('获取到了一组合法签名数据')
        log.debug(_data)
    if int(cache.get(session['username'] + '.count')) >= 3:
        log.info('获取到了三组信息，成功注册')

        log.debug('所有数据:')
        register_data = cache.lrange(session['username'], 0, -1)
        register_data = [json.loads(i) for i in register_data]
        log.debug(register_data)

        cache.delete(session['username'])
        cache.delete(session['username'] + '.count')

        real = DynamicProcess.prepare_list(register_data)
        real_v = DynamicProcess.prepare_value(real)
        execute_sql(
            "INSERT INTO user (username, password, sign_prepared, sign_val, role) values (\
                %(username)s, %(password)s, %(sign_prepared)s, %(sign_val)s, %(role)s \
            )",
            username=session['username'],
            password=session['password'],
            sign_prepared=json.dumps(real),
            sign_val=real_v,
            role=session['role']
        )
        session.pop('username')
        session.pop('password')
        session.pop('role')
        return 'ret'
    return 'continue'


# 登陆
@api.route('/login', methods=['POST'])
def pre_login():
    username = request.form['username']
    username = username.replace('"', '')
    ret = execute_sql(
        'SELECT username FROM user WHERE username=%(username)s',
        username=username
    )
    if ret is None or len(ret) == 0:
        return 'this username hasn\'t been registered yet'
    session['username'] = username
    session['action'] = 'login'
    return redirect('/page/sigpad')


def login(_data):
    true_data = execute_sql(
        "SELECT sign_prepared, sign_val FROM user WHERE username=%(username)s",
        username=session['username']
    )
    result, new_prepared = DynamicProcess.match(
        json.loads(true_data[0]), float(true_data[1]),
        _data, limit=0.6
    )
    role = execute_sql(
        "SELECT role FROM user WHERE username=%(username)s",
        username=session['username']
    )[0]
    if result:
        execute_sql(
            'UPDATE user SET sign_val=%(sign_v)s WHERE username=%(username)s',
            sign_v=new_prepared,
            username=session['username']
        )
        users.setLoginStatus(session['username'], True)
        # 一小时内免登录
    return str(result)


@api.route('/update', methods=['POST'])
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
    return redirect('/page/sigpad')


def update(_data):
    true_data = execute_sql(
        "SELECT sign_prepared, sign_val FROM user WHERE username=%(username)s",
        username=session['username']
    )
    result = False
    if true_data:
        result, new_prepared = DynamicProcess.match(
            json.loads(true_data[0]), float(true_data[1]),
            _data, limit=0.6
        )
    if result:
        execute_sql(
            'UPDATE user SET sign_val=%(sign_v)s WHERE username=%(username)s',
            sign_v=new_prepared,
            username=session['username']
        )
        return 'success'
    return 'failure'


@api.route('/submit', methods=['POST'])
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


@api.route('/logout')
def logout():
    if 'username' in session.keys():
        users.setLoginStatus(session['username'], False)
    return redirect('/')


# 初始化数据库
@api.route('/db_init', methods=['GET'])
def db_init():
    init_sqls = [
        "DROP TABLE IF EXISTS user",
        "CREATE TABLE user (\
            id int primary key auto_increment,\
            username varchar(50) NOT NULL,\
            password varchar(50) NOT NULL,\
            sign_prepared text,\
            sign_val float,\
            role text\
        );",
        "INSERT INTO user (username,password) VALUES ('admin','admin');"
    ]
    for i in init_sqls:
        execute_sql(i)
    return 'init success'
