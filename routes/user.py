from flask import Blueprint, make_response, request

# from sql.model import db
from sql.tables.t_user import t_user
from lib.interface import response
from lib.redis import Redis

user = Blueprint('user', __name__)


@user.before_request
def getUserId():
    global token
    global userid

    token = request.headers.get('token', default=False)
    if not token:
        return make_response(response(msg="需要登录", code=10), 200)

    userid = Redis.read('session_{}'.format(token))
    if not userid:
        return make_response(response(msg="登录态过期，请刷新页面", code=10), 200)


@user.route('/userInfo', methods=['GET'])
def userInfo():
    results = t_user.query.get(userid)
    data = {
        'uuid': results.uuid,
        'avatar': results.avatar,
        'email': results.email,
        'phone': results.phone,
        'qq': results.qq,
        'vip_vaild': results.vip_vaild_time,
        'active': results.active
    }
    return make_response(response(data=data), 200)
