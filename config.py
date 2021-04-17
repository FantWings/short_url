from os import path, getenv, urandom
from lib.log import msg
from datetime import timedelta

base_dir = path.abspath(path.dirname(__file__))


class Config(object):
    """
    FLASK配置发布函数
    """
    if getenv('SQL_MODE') == 'mysql':
        # 拼接SQL URI
        database_uri = "mysql://%s:%s@%s:%s/%s" % (
            getenv('SQL_USER'),
            getenv('SQL_PASS'),
            getenv('SQL_HOST'),
            getenv('SQL_PORT'),
            getenv('SQL_BASE')
        )
        msg('服务端已配置MySQL，将使用MySQL作为存储介质。')
    else:
        database_uri = False
        msg('服务端未配置MySQL，服务端将使用默认的SQLite作为存储介质。')

    # SQLALCHEMY配置
    SQLALCHEMY_DATABASE_URI = database_uri or 'sqlite:///' + path.join(
        base_dir, 'sqlite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # 禁用ASCII编码
    JSON_AS_ASCII = False

    # 设置SESSION安全密钥
    SECRET_KEY = urandom(24)

    # 设置SESSION有效期
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
