from flask import Blueprint, make_response, session, request
from hashlib import md5


from sql.model import db
from sql.tables.t_user import t_user
from lib.interface import response
from lib.smtp import sendmail

auth = Blueprint('auth', __name__)


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
    password = md5().update(submit.get('passwd').
                            encode(encoding='utf-8'))
    db.session.add(
        t_user(
            password=password,
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
        response(msg='账户不存在！', status=1)
    else:
        results = sendmail(
            '''
            您正在尝试注册账号，请点击链接来完成注册：
            https://localhost:5000/auth/verfiyEmail?email=%s&token=%s
            ''' % (email, results.token), email, '账户注册', '福瑞文化')
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
    password = md5().update(submit.get('passwd').
                            encode(encoding='utf-8'))

    results = t_user.query.filter_by(email=email).first()
    if password == results.password:
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
