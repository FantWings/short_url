from flask import Blueprint, make_response, request

from lib.interface import response
from sql.model import db
from sql.tables.t_url import t_url
from lib.gen import genToken
from lib.redis import Redis

url = Blueprint('url', __name__)


@url.before_app_request
def get_userid():
    global userid
    userid = Redis.read(
        'session_{}'.format(request.headers.get('token', default=0)))


@url.route('/getLists', methods=['GET'])
def get_urls():
    if userid:
        results = t_url.query.filter_by(owner_id=userid).all()
        data = []
        for result in results:
            data.append(
                {
                    'url_id': result.id,
                    'short_url': result.short_url,
                    'original_url': result.original_url,
                    'vaild_time': result.vaild_time
                }
            )
        return make_response(response(data=data), 200)
    else:
        return make_response(response(msg="该操作需要登录", status=1), 200)


@url.route('/add', methods=['POST'])
def add_url():
    if userid:
        client_data = request.get_json()
        url = client_data.get('url')
        if t_url.query.filter_by(original_url=url).first() is None:
            new_url = t_url(
                short_url=genToken(8),
                original_url=url,
                owner_id=userid,
            )
            db.session.add(new_url)
            db.session.commit()
            return make_response(response(msg="地址添加成功"), 200)
        else:
            return make_response(response(msg="地址已经存在", status=1), 200)
    else:
        return make_response(response(msg="该操作需要登录", status=1), 200)


@url.route('/delete', methods=['DELETE'])
def del_url():
    if userid:
        results = t_url.query.get(request.args.get('urlId'))
        results.status = -1
        db.session.commit()
        return make_response(response(msg="操作成功"), 200)
    else:
        return make_response(response(msg="该操作需要登录", code=1), 200)
