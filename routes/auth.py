from flask import Blueprint, make_response, request, current_app

from sql.model import db
from sql.tables.t_user import t_user
from lib.interface import response
from lib.smtp import sendmail
from lib.redis import Redis
from lib.gen import genToken

auth = Blueprint('auth', __name__)


def md5(secret):
    from hashlib import md5
    salted = 'super{}password'.format(secret)
    return md5(salted.encode('utf-8')).hexdigest()


@auth.route('/signup', methods=['POST'])
def signup():
    submit = request.get_json()
    email = submit.get('email')
    db.session.add(t_user(password=md5(submit.get('passwd')), email=email))
    db.session.commit()
    return make_response(response(msg="注册成功"), 200)


@auth.route('/sendVerifyEmail', methods=['GET'])
def sendVerifyMail():
    account = request.args.get('email')
    results = t_user.query.filter_by(email=account).first()
    if results is None:
        return response(msg='账户不存在！', code=1)
    if results.active:
        return response(msg='账户已经激活过了！', code=1)
    else:
        try:
            token = genToken(32)
            Redis.write('verify_{}'.format(account), token, expire=300)
        except Exception:
            return response(msg="临时数据写入失败，请重试", code=1)
        n_list = [
            current_app.config.get('HTTP_MODE'),
            current_app.config.get('HOST_NAME'),
            current_app.config.get('HTTP_PORT'), account, token
        ]
        results = sendmail(
            '''
            您正在尝试注册账号，请点击链接来完成注册：
            {0}://{1}:{2}/auth/verifyEmail?email={3}&token={4}
            '''.format(*n_list), account, '账户注册',
            current_app.config.get('SITE_NAME'))
        return response(msg=results)


@auth.route('/verifyEmail', methods=['GET'])
def verifyEmail():
    account = request.args.get('email')
    token = request.args.get('token')
    results = t_user.query.filter_by(email=account).first()
    if results is None:
        return response(msg='账户不存在！请检查！', code=1)
    if results.active:
        return response(msg='账户已经激活过了！', code=1)
    if token == Redis.read('verify_{}'.format(account)):
        results.active = True
        db.session.commit()
        Redis.delete('verify_{}'.format(account))
        return make_response(response(msg="账户已激活"), 200)
    else:
        return make_response(response(msg="验证失败，请重试", code=1), 200)


@auth.route('/signIn', methods=['POST'])
def signIn():
    submit = request.get_json()
    email = submit.get('email')
    results = t_user.query.filter_by(email=email).first()
    if results is None:
        return make_response(response(msg="用户不存在", code=1), 200)
    if md5(submit.get('password')) == results.password:
        sessionToken = genToken(24)
        Redis.write('session_{}'.format(sessionToken), results.id)
        if submit.get('remember'):
            Redis.expire(sessionToken, 604800)
        return make_response(
            response(data={'token': sessionToken}, msg="登录成功"), 200)
    else:
        return make_response(response(msg="账号或密码错误", code=1), 200)


@auth.route('/signOut', methods=['DELETE'])
def signout():
    sessionId = request.headers.get('token', default=False)
    Redis.delete(sessionId)
    return make_response(response(msg='登出成功', code=10), 200)
