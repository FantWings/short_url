from os import path, urandom
from datetime import timedelta
import configparser

base_dir = path.abspath(path.dirname(__file__))


class Config():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini', encoding='utf-8')

    def config_get(self, section, item):
        '''
        从INI获取配置字段
        --------------------
        section = INI stction名称
        item = 配置字段key
        '''
        return self.config.get(section, item)

    def config_items(self, section):
        '''
        从INI获取所有键值对
        --------------------
        section = INI stction名称
        '''
        return self.config.items(section)


class Sql(object):
    """
    FLASK配置发布函数
    """
    config = Config()
    if config.config_get('db', 'mode') == 'mysql':
        # 拼接SQL URI
        database_uri = "mysql://%s:%s@%s:%s/%s" % (
            config.config_get('db', 'user'),
            config.config_get('db', 'pass'),
            config.config_get('db', 'host'),
            config.config_get('db', 'port'),
            config.config_get('db', 'base'),
        )
    else:
        database_uri = False

    # SQLALCHEMY配置
    SQLALCHEMY_DATABASE_URI = database_uri or 'sqlite:///' + path.join(
        base_dir, 'sqlite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # 禁用ASCII编码
    JSON_AS_ASCII = False

    # 设置SESSION安全密钥
    SECRET_KEY = urandom(24)

    # 设置SESSION有效期
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
