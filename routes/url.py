from flask import Blueprint, make_response, request, session
import random

from lib.interface import response

from sql.model import db
from sql.tables.t_url import t_url

url = Blueprint('url', __name__)


@url.route('/get', methods=['GET'])
def get_urls():
    userid = session.get('uid')
    results = t_url.query.filter_by(owner_id=userid).all()
    make_response(response(data=results), 200)


@url.route('/add', methods=['POST'])
def add_url():
    userid = session.get('uid')
    client_data = request.get_json()
    if userid is None:
        make_response(response(msg="该操作需要登录", code=401), 200)

    if userid:
        new_url = t_url(
            short_url=random(),
            original_url=client_data.get('url'),
            owner_id=userid,
        )

    db.session.add(new_url)
    db.seesion.commit()


@url.route('/delete', methods=['DELETE'])
def del_url():
    userid = session.get('uid')
    if userid is None:
        make_response(response(msg="该操作需要登录", code=401), 200)
    else:
        results = t_url.query.get(request.args.get('urlId'))
        results.status = -1
        db.session.commit()
        return make_response(response(msg="操作成功"), 200)
