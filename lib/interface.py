def response(data="", msg="", code=0):
    """
    返回数据处理函数
    data:           回调数据（Json）
    msg:            附加消息（字符串）
    status:         返回码（数值）
    """
    response = {
        'msg': msg,
        'data': data,
        'code': code
    }
    return response
