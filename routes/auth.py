from flask import Blueprint, make_response, session
from time import time

from sql.model import db
from sql.tables.t_user import t_user

auth = Blueprint('auth', __name__)


@auth.before_request
def before_request():
    """
    设置用户Session有效期
    """
    session.permanent = True


@auth.route('/signup', methods=['POST'])
def signup():
    return make_response('Login', 200)


@auth.route('/signin', methods=['POST'])
def login():
    return make_response('Login', 200)


@auth.route('/signout')
def signout():
    return make_response('Login', 200)
