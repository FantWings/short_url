from flask import Blueprint, make_response, session, request

from config import Config
from sql.model import db
from sql.tables.t_user import t_user
from lib.interface import response
from lib.smtp import sendmail

auth = Blueprint('auth', __name__)
config = Config()


def md5(password):
    from hashlib import md5
    salted = '%sandgoodstuff' % (password)
    return md5(salted.encode('utf-8')).hexdigest()


@auth.before_app_first_request
def setSession():
    """
    设置用户Session有效期
    """
    session.permanent = True


@auth.route('/signup', methods=['POST'])
def signup():
    submit = request.get_json()
    email = submit.get('email')
    db.session.add(
        t_user(
            password=md5(submit.get('passwd')),
            email=email
        )
    )
    db.session.commit()
    return make_response(response(msg="注册成功"), 200)


@auth.route('/sendVerifyEmail', methods=['GET'])
def sendVerifyMail():
    email = request.args.get('email')
    results = t_user.query.filter_by(email=email).first()
    if results is None:
        return response(msg='账户不存在！', status=1)
    if results.active:
        return response(msg='账户已经激活过了！', status=1)
    else:
        http_mode = config.config_get('http', 'httpmode')
        host_name = config.config_get('http', 'hostname')
        http_port = config.config_get('http', 'httpport')
        sender_name = config.config_get('site', 'name')
        results = sendmail(
            '''
            您正在尝试注册账号，请点击链接来完成注册：
            %s://%s:%s/auth/verifyEmail?email=%s&token=%s
            ''' % (http_mode, host_name, http_port,
                   email, results.token), email, '账户注册', sender_name)
        return response(msg=results)


@auth.route('/verifyEmail', methods=['GET'])
def verifyEmail():
    email = request.args.get('email')
    token = request.args.get('token')
    results = t_user.query.filter_by(email=email).first()
    if token == results.token:
        results.active = True
        results.token = None
        db.session.commit()
        return make_response(response(msg="账户已激活"), 200)
    else:
        return make_response(response(msg="验证失败，请重试", status=1), 200)


@auth.route('/signIn', methods=['POST'])
def signIn():
    submit = request.get_json()
    email = submit.get('email')
    results = t_user.query.filter_by(email=email).first()
    if md5(submit.get('passwd')) == results.password:
        session['uid'] = results.id
        return make_response(response(msg="登录成功"), 200)
    else:
        return make_response(response(msg="账号或密码错误", status=1), 200)


@auth.route('/userInfo', methods=['GET'])
def userInfo():
    if session.get('uid', default=False):
        results = t_user.query.get(session['uid'])
        data = {
            'uuid': results.uuid,
            'email': results.email,
            'phone': results.phone,
            'qq': results.qq,
            'vip_vaild': results.vip_vaild_time,
            'active': results.active
        }
        return make_response(response(data=data), 200)

    else:
        return make_response(response(msg="需要登录", status=1), 200)


@auth.route('/signOut', methods=['DELETE'])
def signout():
    session.pop('uid', None)
    return make_response(response(msg='登出成功'), 200)
