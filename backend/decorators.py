import functools
import json
import time
import users
import utils
from flask import render_template, session


def api_response(func):
    @functools.wraps(func)
    def _api_response(*args, **kwargs):
        result = {}
        result['status'], result['message'], result['content'] = func(*args, **kwargs)
        return json.dumps(result), 200, {'Content-Type': 'application/json;'}
    return _api_response


def requireLogin(func):
    @functools.wraps(func)
    def checkLogin(*args, **kwargs):
        if 'username' not in session.keys() or not users.isLoggedIn(session['username']):
            return render_template('error.html', messages=['请先登陆', 'Please login'])
        return func(*args, **kwargs)
    return checkLogin


def requireRole(role):
    def factory(func):
        @functools.wraps(func)
        def checkRole(*args, **kwargs):
            this_role = utils.execute_sql(
                "SELECT role FROM user WHERE username=%(username)s",
                username=session['username']
            )[0]
            if this_role != role:
                return render_template('error.html', messages=[
                    f'只有身份为{role}的用户可以进行此操作',
                    f'You must be {role} to perform such operations'
                ])
            else:
                return func(*args, **kwargs)
        return checkRole
    return factory


locks = {}


def sync(id):
    def factory(func):
        @functools.wraps(func)
        def _sync(*args, **kwargs):
            global locks
            while id in locks.keys() and locks[id]:
                time.sleep(0.2)
            locks[id] = True
            ret = func(*args, **kwargs)
            locks[id] = False
            return ret
        return _sync
    return factory
