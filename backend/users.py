from utils import execute_sql, cache
from flask import session
import json


def isLoggedIn(username):
    if not cache.exists(username+".logged_in"):
        return False
    return cache.get(username+'.logged_in').decode() == 'true'


def setLoginStatus(username, status: bool):
    cache.set(username+'.logged_in', json.dumps(status), ex=3600)


def getInfo(username):
    res = execute_sql(
        'SELECT username, role FROM user WHERE username=%(username)s',
        username=username
    )
    if res:
        return {
            'logged_in': isLoggedIn(username),
            'username': res[0],
            'role': res[1]
        }
    else:
        return {'logged_in': False, 'role': 'unknown'}
