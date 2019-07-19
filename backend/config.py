import os
import redis

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PORT = int(REDIS_PORT) if REDIS_PORT else 6379
REDIS_DB = 0
REDIS_PASS = os.getenv('REDIS_PASS')

conn = redis.Redis(
    REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASS
)

def get_secret_key():
    if conn.exists('secret_key'):
        return conn.get('secret_key')
    secret_key = os.urandom(64)
    conn.set('secret_key', secret_key)
    return secret_key
