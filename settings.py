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
    smtp_username = ini.get('smtp', 'user')
    smtp_password = ini.get('smtp', 'pass')
    smtp_host = ini.get('smtp', 'host')
    smtp_port = ini.get('smtp', 'port')

    """站点设置"""
    http_mode = ini.get('http', 'httpmode')
    host_name = ini.get('http', 'hostname')
    http_port = ini.get('http', 'httpport')
    site_name = ini.get('site', 'name')

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

    """SQLALCHEMY配置"""
    SQLALCHEMY_DATABASE_URI = database_uri or 'sqlite:///' + path.join(
        base_dir, 'sqlite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    JSON_AS_ASCII = False
