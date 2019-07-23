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


@page.route('/request/<action>')
def _request(action):
    if os.path.exists(f'templates/request/{action}.html'):
        return render_template(f'request/{action}.html')
    else:
        response = make_response(render_template('404.html'))
        response.status_code = 404
        return response


@page.route('/request/show/<int:id>')
def show_request(id):
    return render_template('request/show.html', id=id)


@page.route('/<page>')
def get_page_route(page):
    if 'id' not in session.keys():
        session['id'] = os.urandom(32)
    info = getInfo(session['username']) if 'username' in session.keys() else {
        'logged_in': False,
        'role': 'unknown'
    }

    if page in ['index', 'home', 'main']:
        page = 'index'
        return render_template('index.html', **{"role": info['role'], 'logged_in': info['logged_in']})
    elif info['logged_in'] and page in ['login', 'register']:
        return redirect('/page/index')
    elif page in ['login', 'register', 'optimize', 'logout']:
        return redirect(f'/{page}.html')
    elif os.path.exists(f'templates/{page}.html'):
        return render_template(page + '.html')
    else:
        response = make_response(render_template('404.html'))
        response.status_code = 404
        return response
