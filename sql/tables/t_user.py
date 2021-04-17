from sql.model import db
from sqlalchemy.sql import func


class t_user(db.Model):
    __tablename__ = "t_user"
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment='索引')
    uuid = db.Column(
        db.String(64),
        nullable=False,
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
        nullable=False,
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
