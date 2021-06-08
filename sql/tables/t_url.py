from sql.model import db
from sqlalchemy.sql import func


class t_url(db.Model):
    __tablename__ = "t_url"
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment='索引')
    short_url = db.Column(db.String(32), nullable=False, comment='缩短后的网址')
    original_url = db.Column(db.String(32), nullable=False, comment='原始网址')
    create_time = db.Column(db.DateTime,
                            nullable=False,
                            default=func.now(),
                            comment='创建时间')
    status = db.Column(db.SmallInteger,
                       nullable=False,
                       default=0,
                       comment='短链状态')
    owner_id = db.Column(db.Integer, comment='所有者', nullable=False)
    vaild_time_start = db.Column(db.DateTime,
                                 comment='有效期开始时间',
                                 default='2000-01-01',
                                 nullable=False)
    vaild_time_end = db.Column(db.DateTime,
                               comment='有效期截止时间',
                               default='9999-01-01',
                               nullable=False)
