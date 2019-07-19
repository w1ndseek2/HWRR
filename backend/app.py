import os
from flask import Flask, redirect
import redis
import page
import api
from utils import get_secret_key


app = Flask(__name__)
app.secret_key = get_secret_key()

app.register_blueprint(page.page, url_prefix='/page')
app.register_blueprint(api.api, url_prefix='/api')

@app.route('/')
def index():
    return redirect('/page/index')

if __name__ == '__main__':
    app.run('0.0.0.0', 8081, debug=True)
