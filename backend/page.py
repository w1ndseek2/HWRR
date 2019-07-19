import os
from flask import (
    Blueprint, session,
    render_template,
    make_response,
    request, redirect
)
from users import getInfo

try:
    from backend.utils import cache
except ImportError:
    from utils import cache

page = Blueprint('page', __name__)


@page.route('/<page>')
def getPageRoute(page):
    if 'id' not in session.keys():
        session['id'] = os.urandom(32)
    role = getInfo(session['username'])['role']\
        if 'username' in session.keys() else 'unknown'
    return getPage(page, role)


FIELDS = [{
    'name': 'username',
    'type': 'text',
    'placeholder': 'username/ student ID/ teacher ID'
}, {
    'name': 'password',
    'type': 'password',
    'placeholder': 'input password'
}, {
    'name': 'role',
    'type': 'text',
    'placeholder': 'input "student" or "teacher"'
}]


def getPage(page, role):
    if page in ['index', 'home', 'main']:
        page = 'index'
        return render_template('index.html', **{"role": role})
    elif page in ['login', 'register', 'optimize']:
        title = page.capitalize()
        action = f'/api/{page}'
        return render_template('form.html', **{
            'title': title,
            'action': action,
            'fields': FIELDS[:1] if page == 'login' else FIELDS if page == 'register' else FIELDS[:2]
        })
    elif os.path.exists(f'templates/{page}.html'):
        return render_template(page + '.html')
    else:
        response = make_response(render_template('404.html'))
        response.status_code = 404
        return response
