from sql.mysql import db
from datetime import datetime


class t_user(db.Model):
    __tablename__ = "t_user"
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment='索引')
    uuid = db.Column(
        db.String(32),
        nullable=False,
        comment='用户UUID')
    username = db.Column(
        db.String(32),
        nullable=False,
        comment='用户名')
    password = db.Column(
        db.String(32),
        nullable=False,
        comment='密码')
    email = db.Column(
        db.String(32),
        nullable=False,
        comment='邮箱')
    phone = db.Column(db.Integer, comment='手机号')
    qq = db.Column(db.Integer, comment='QQ号')
    create_time = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        comment='创建时间')
    update_time = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        comment='修改时间')
    creadit = db.Column(
        db.SmallInteger,
        nullable=False,
        default=1000,
        comment='修改时间')
    vip_exp = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        comment='会员过期时间')


class t_url(db.Model):
    __tablename__ = "t_url"
    short_url = db.Column(
        db.String(32),
        primary_key=True,
        nullable=False,
        comment='缩短后的网址')
    original_url = db.Column(
        db.String(32),
        nullable=False,
        comment='原始网址')
    create_time = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        comment='创建时间')
    status = db.Column(
        db.SmallInteger,
        nullable=False,
        default=0,
        comment='短链状态')
    owner_id = db.Column(
        db.Integer,
        nullable=False,
        comment='所有者')


class t_log(db.Model):
    __tablename__ = "t_log"
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment='索引')
    url_id = db.Column(
        db.String(32),
        nullable=False,
        comment='缩短后的网址')
    ip_addr = db.Column(
        db.String(32),
        nullable=False,
        comment='用户IP地址')
    ua = db.Column(
        db.String(256),
        nullable=False,
        comment='用户UA')
    referer = db.Column(
        db.String(32),
        comment='来源')
    time = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        comment='访问时间')
