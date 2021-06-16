import time
from flask import Blueprint, make_response, request
from sqlalchemy import func

from lib.interface import response
from sql.model import db
from sql.tables.t_url import t_url
from lib.gen import genToken
from lib.redis import Redis

url = Blueprint('url', __name__)


@url.before_request
def getUserId():
    global token
    global userid

    token = request.headers.get('token', default=False)
    if not token:
        return make_response(response(msg="需要登录", code=10), 200)

    userid = Redis.read('session_{}'.format(token))
    if not userid:
        return make_response(response(msg="登录态过期，请刷新页面", code=10), 200)


@url.route('/getLists', methods=['GET'])
def get_urls():
    results = t_url.query.filter(t_url.owner_id == userid,
                                 t_url.status >= 0).all()
    data = []
    for result in results:
        isPerment = True if int(time.mktime(result.vaild_time_end.timetuple())
                                ) * 1000 == 253370750400000 else False
        data.append({
            'url_id':
            result.id,
            'short_url':
            result.short_url,
            'original_url':
            result.original_url,
            'starttime':
            int(time.mktime(result.vaild_time_start.timetuple())) * 1000,
            'endtime':
            int(time.mktime(result.vaild_time_end.timetuple())) * 1000,
            'permemt':
            isPerment,
            'status':
            result.status
        })
    return make_response(response(data=data), 200)


@url.route('/add', methods=['POST'])
def add_url():
    client_data = request.get_json()
    url = client_data.get('url')
    if t_url.query.filter_by(original_url=url, status=0).first() is None:
        new_url = t_url(
            short_url=genToken(8),
            original_url=url,
            owner_id=userid,
        )
        db.session.add(new_url)
        db.session.commit()
        return make_response(response(msg="地址添加成功"), 200)
    else:
        return make_response(response(msg="地址已经存在", code=1), 200)


@url.route('/delete', methods=['DELETE'])
def del_url():
    results = t_url.query.get(request.args.get('urlId'))
    results.status = -1
    db.session.commit()
    return make_response(response(msg="操作成功"), 200)


@url.route('/update', methods=['POST'])
def update_url():
    results = t_url.query.get(request.args.get('urlId'))
    if request.args.get('enable'):
        enable = request.args.get('enable')
        if enable == 'true':
            results.status = 0
        if enable == 'false':
            results.status = 1

    if request.args.get('method'):
        method = request.args.get('method')
        if method == 'date':
            client_data = request.get_json()
            if client_data["permemt"]:
                results.vaild_time_start = '2000-01-01'
                results.vaild_time_end = '9999-01-01'
            else:
                results.vaild_time_start = time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.localtime(client_data.get('starttime')))
                results.vaild_time_end = time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.localtime(client_data.get('endtime')))

    db.session.commit()
    return make_response(response(msg="操作成功"), 200)
