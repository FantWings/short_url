from flask import Blueprint, make_response, redirect, request
from time import time, mktime

from sql.model import db
from sql.tables.t_url import t_url
from sql.tables.t_log import t_log
from sql.tables.t_user import t_user

from lib.log import access

index = Blueprint('index', __name__)


@index.route('/<params>', methods=['GET'])
def url_router(params):
    results = t_url.query.filter_by(short_url=params).first()
    if results is None:
        return make_response("链接不存在！", 404)
    if results.status == -1:
        return make_response("链接已失效！", 404)
    if results.vaild_time is not None:
        if int(mktime(results.vaild_time.timetuple())) < time():
            return make_response("链接已过期！", 404)
        else:
            pass
    else:
        user = t_user.query.get(results.owner_id)
        vip = int(mktime(user.vip_vaild_time.timetuple())) > time()

        if not vip:
            if user.creadit <= 0:
                return make_response("用户点数已用完！", 200)
            else:
                user.creadit = user.creadit - 1

        db.session.add(
            t_log(
                url_id=params,
                ip_addr=request.headers.get(
                    'X-Forwarded-For') or request.remote_addr,
                ua=request.headers.get('User-Agent'),
                referer=request.headers.get('Referer'),
            )
        )
        access(request.remote_addr, params, results.original_url, vip)
        db.session.commit()
        return make_response(redirect(results.original_url), 302)
