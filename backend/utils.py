import logging
import coloredlogs
import pymysql
from redis import Redis
import os
import time
import functools


def getLoggger(__name__=__name__, level='INFO'):
    log = logging.getLogger(__name__)
    coloredlogs.install(
        level=level,
        logger=log
    )
    return log


pymysql.install_as_MySQLdb()
db = pymysql.connect(
    host=os.getenv('DB_URL') or 'localhost',
    user=os.getenv('DB_USER') or 'username',
    passwd=os.getenv('DB_PWD') or 'password',
    db=os.getenv('DB_NAME') or 'test2'
)
cache = Redis(
    host=os.getenv('CACHE_URL') or 'localhost',
    port=int(os.getenv('CACHE_PORT')) if os.getenv('CACHE_PORT') else 6379,
    password=os.getenv('CACHE_PWD') or ''
)
log = getLoggger()


def get_secret_key():
    if cache.exists('secret_key'):
        return cache.get('secret_key')
    secret_key = os.urandom(64)
    cache.set('secret_key', secret_key)
    return secret_key


executing = False


def execute_sql(sql, **kwargs):
    global executing
    while executing:
        time.sleep(0.5)
    executing = True
    log.debug('executing:\n'+sql)
    log.debug('parameters:')
    log.debug(kwargs)
    cursor = db.cursor()
    cursor.execute(sql, kwargs)
    db.commit()
    x = cursor.fetchall()
    executing = False
    return x[0] if x else None


def merge_data(data):
    t = [i['time'] for i in data]
    x = [i['x'] for i in data]
    y = [i['y'] for i in data]
    return [t, x, y]


def verify(data):
    return len(data) == 3 and len(data[0]) >= 3
