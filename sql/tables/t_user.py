from sql.model import db
from datetime import datetime


class t_user(db.Model):
    __tablename__ = "t_user"
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment='索引')
    uuid = db.Column(
        db.String(32),
        nullable=False,
        comment='用户UUID'
    )
    username = db.Column(
        db.String(32),
        comment='用户名',
        unique=True
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
        db.SmallInteger,
        nullable=False,
        comment='手机号',
        unique=True
    )
    qq = db.Column(
        db.SmallInteger,
        comment='QQ号'
    )
    create_time = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        comment='创建时间'
    )
    update_time = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        comment='修改时间'
    )
    creadit = db.Column(
        db.SmallInteger,
        nullable=False,
        default=100,
        comment='修改时间'
    )
    vip_vaild_time = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        comment='会员过期时间'
    )
