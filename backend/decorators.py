import functools
import json
from users import isLoggedIn
from flask import render_template, session
from utils import execute_sql


def api_response(func):
    @functools.wraps(func)
    def _api_response(*args):
        result = {}
        result['status'], result['message'], result['content'] = func()
        return json.dumps(result), 200, {'Content-Type': 'application/json;'}
    return _api_response


def requireLogin(func):
    @functools.wraps(func)
    def checkLogin(*args):
        if 'username' not in session.keys() or not isLoggedIn(session['username']):
            return render_template('error.html', messages=['请先登陆', 'Please login'])
        return func(*args)
    return checkLogin


def requireRole(role):
    def factory(func):
        @functools.wraps(func)
        def checkRole(*args):
            this_role = execute_sql(
                "SELECT role FROM user WHERE username=%(username)s",
                username=session['username']
            )[0]
            if this_role != role:
                return render_template('error.html', messages=[
                    f'只有身份为{role}的用户可以进行此操作',
                    f'You must be {role} to perform such operations'
                ])
            else:
                return func(*args)
        return checkRole
    return factory
