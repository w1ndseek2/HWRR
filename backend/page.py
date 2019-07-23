import os
from flask import (
    Blueprint, session,
    render_template,
    make_response,
    request, redirect
)
from users import getInfo
from utils import cache

page = Blueprint('page', __name__)


@page.route('/<page>')
def getPageRoute(page):
    if 'id' not in session.keys():
        session['id'] = os.urandom(32)
    info = getInfo(session['username']) if 'username' in session.keys() else {
        'logged_in': False,
        'role': 'unknown'
    }
    return getPage(page, info)


def getPage(page, info):
    if page in ['index', 'home', 'main']:
        page = 'index'
        return render_template('index.html', **{"role": info['role'], 'logged_in': info['logged_in']})
    elif info['logged_in'] and page in ['login', 'register']:
        return redirect('/page/index')
    elif page in ['login', 'register', 'optimize', 'request', 'logout', 'review']:
        return redirect(f'/{page}.html')
    elif os.path.exists(f'templates/{page}.html'):
        return render_template(page + '.html')
    else:
        response = make_response(render_template('404.html'))
        response.status_code = 404
        return response
