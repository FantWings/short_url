import uuid
from random import Random


def genToken(length):
    token = ''
    chars = '0123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ-_'
    temp = len(chars) - 1
    for i in range(length):
        token += chars[Random().randint(0, temp)]
    return token


def genUuid():
    return uuid.uuid1().hex
