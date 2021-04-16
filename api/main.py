from flask import Blueprint, make_response, redirect, request
from time import time

from sql.mysql import db
from sql.model import t_url, t_log, t_user

# from api.response import response

main = Blueprint('main', __name__)


@main.route('/<params>', methods=['GET'])
def url_router(params):
    print(request.headers)
    time_now = time()
    results = t_url.query.get(params)
    if results is None:
        return make_response("链接不存在！", 200)
    else:
        user = t_user.query.get(results.owner_id)
        if user.vip_exp < time_now:
            if user.creadit <= 0:
                return make_response("用户点数已用完！", 200)
        else:
            log = t_log(
                url_id=params,
                ip_addr=request.remote_addr,
                ua=request.headers.get('User-Agent'),
                referer=request.referrer,
            )
            if user.vip_exp < time_now:
                user.creadit = user.creadit - 1
            db.session.add(log)
            db.session.commit()
            return make_response(redirect(results.original_url), 302)
