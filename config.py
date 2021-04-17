import json
import os
from lib.log import msg
from datetime import timedelta

base_dir = os.path.abspath(os.path.dirname(__file__))
# 从config.json读取数据库配置
config = json.load(open('config.json'))


class Config(object):
    """
    FLASK配置发布函数
    """
    if config.get('sql_enable'):
        # 拼接SQL URI
        database_uri = "mysql://%s:%s@%s:%s/%s" % (
            config['sql_username'],
            config['sql_password'],
            config['sql_hostname'],
            config.get('sql_port', '3306'),
            config['sql_database']
        )
        msg('服务端已配置MySQL，将使用MySQL作为存储介质。')
    else:
        # 回退使用MYSQLITE
        database_uri = False
        msg('服务端未配置MySQL，服务端将使用SQLite作为存储介质。')

    # SQLALCHEMY配置
    SQLALCHEMY_DATABASE_URI = database_uri or 'sqlite:///' + os.path.join(
        base_dir, 'sqlite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # 禁用ASCII编码
    JSON_AS_ASCII = False

    # 设置SESSION安全密钥
    SECRET_KEY = os.urandom(24)

    # 设置SESSION有效期
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)


smtp = {
    'host': config.get('smtp_host'),
    'port': config.get('smtp_port'),
    'user': config.get('smtp_user'),
    'pass': config.get('smtp_pass'),
}
