import logging
import coloredlogs
import pymysql
import os
pymysql.install_as_MySQLdb()
conn = pymysql.connect(
    host=os.getenv('DB_URL') or 'localhost',
    user=os.getenv('DB_USER') or 'username',
    passwd=os.getenv('DB_PWD') or 'password',
    db=os.getenv('DB_NAME') or 'test2'
)


def execute_sql(sql, **kwargs):
    cursor = conn.cursor()
    cursor.execute(sql, kwargs)
    conn.commit()
    return cursor.fetchall()[0]


def merge_data(data):
    t = [i['time'] for i in data]
    x = [i['x'] for i in data]
    y = [i['y'] for i in data]
    return [t, x, y]


def verify(data):
    return len(data) == 3 and len(data[0]) >= 3


def getLoggger(__name__=__name__):
    log = logging.getLogger(__name__)
    coloredlogs.install(
        level='INFO',
        logger=log
    )
    return log
