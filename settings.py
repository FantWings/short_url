from os import path, urandom
from datetime import timedelta
import configparser

base_dir = path.abspath(path.dirname(__file__))
ini = configparser.ConfigParser()
ini.read('config.ini', encoding='utf-8')


class FlaskConfig(object):
    """FLASK配置"""
    SECRET_KEY = urandom(24)
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    """ SMTP配置 """
    SMTP_USER = ini.get('smtp', 'user')
    SMTP_PASS = ini.get('smtp', 'pass')
    SMTP_HOST = ini.get('smtp', 'host')
    SMTP_PORT = ini.get('smtp', 'port')
    """站点设置"""
    HTTP_MODE = ini.get('http', 'httpmode')
    HOST_NAME = ini.get('http', 'hostname')
    HTTP_PORT = ini.get('http', 'httpport')
    SITE_NAME = ini.get('site', 'name')
    """数据库配置"""
    if ini.get('db', 'mode') == 'mysql':
        # 拼接SQL URI
        database_uri = "mysql://%s:%s@%s:%s/%s" % (
            ini.get('db', 'user'),
            ini.get('db', 'pass'),
            ini.get('db', 'host'),
            ini.get('db', 'port'),
            ini.get('db', 'base'),
        )
    else:
        database_uri = False
    SQLALCHEMY_DATABASE_URI = database_uri or 'sqlite:///' + path.join(
        base_dir, 'sqlite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    JSON_AS_ASCII = False
    """Redis配置"""
    REDIS_HOST = ini.get('redis', 'host')
    REDIS_PORT = ini.get('redis', 'port')
    REDIS_DB = ini.get('redis', 'db')
    REDIS_EXPIRE = ini.get('redis', 'expire')
