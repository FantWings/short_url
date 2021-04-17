from flask import Blueprint, make_response, request, session
from datetime import datetime, timedelta
import random

from api.response import response

from sql.model import db
from sql.tables.t_url import t_url
from sql.tables.t_log import t_log
from sql.tables.t_user import t_user

api = Blueprint('api', __name__)


@api.route('/url/add', methods=['POST'])
def add_url():
    userid = session.get('token')
    client_data = request.get_json()
    if userid is None:
        new_url = t_url(
            short_url=random(),
            original_url=client_data.get('url'),
            vaild_time=datetime.now + timedelta(days=1),
        )

    if userid:
        new_url = t_url(
            short_url=random(),
            original_url=client_data.get('url'),
            owner_id=userid,
        )

    db.session.add(new_url)
    db.seesion.commit()


@api.route('/url/delete', methods=['DELETE'])
def del_url():
    userid = session.get('token')
    if userid is None:
        make_response(response(False, msg="该操作需要登录", code=401), 200)
    else:
        todo
