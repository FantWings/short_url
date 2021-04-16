from sql.model import db
from datetime import datetime


class t_log(db.Model):
    __tablename__ = "t_log"
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment='索引')
    url_id = db.Column(
        db.String(32),
        nullable=False,
        comment='缩短后的网址'
    )
    ip_addr = db.Column(
        db.String(32),
        nullable=False,
        comment='用户IP地址'
    )
    ua = db.Column(
        db.String(256),
        nullable=False,
        comment='用户UA'
    )
    referer = db.Column(
        db.String(32),
        comment='来源'
    )
    time = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        comment='访问时间'
    )
