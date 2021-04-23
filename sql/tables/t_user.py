from sql.model import db
from sqlalchemy.sql import func

import uuid
from random import Random


def genToken(length):
    token = ''
    chars = 'abcdefghijklnmopqrstuvwxyz1234567890'
    temp = len(chars) - 1
    for i in range(length):
        token += chars[Random().randint(0, temp)]
    return token


def genUuid():
    return uuid.uuid1().hex


class t_user(db.Model):
    __tablename__ = "t_user"
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment='索引')
    uuid = db.Column(
        db.String(64),
        nullable=False,
        default=genUuid(),
        comment='用户UUID'
    )
    avatar = db.Column(
        db.String(64),
        comment='头像'
    )
    password = db.Column(
        db.String(32),
        comment='密码'
    )
    email = db.Column(
        db.String(32),
        nullable=False,
        comment='邮箱',
        unique=True
    )
    phone = db.Column(
        db.String(11),
        # 手机号验证功能没做完，暂时注释必填字段
        # nullable=False,
        comment='手机号',
        unique=True
    )
    qq = db.Column(
        db.String(13),
        comment='QQ号'
    )
    create_time = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.now(),
        comment='创建时间'
    )
    update_time = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.now(),
        comment='修改时间',
        onupdate=func.now()
    )
    creadit = db.Column(
        db.SmallInteger,
        nullable=False,
        default=100,
        comment='可用点数'
    )
    vip_vaild_time = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.now(),
        comment='会员过期时间'
    )
    active = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        comment='账户状态'
    )
    token = db.Column(
        db.String(32),
        default=genToken(32),
        comment='临时token'
    )
