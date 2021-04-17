from time import localtime, strftime


def msg(message, level=0):
    """
    SQL状态日志输出函数

    level = 日志等级
    message = 消息内容
    """
    log_level = ['INFO', 'WARN', 'ERROR', 'DEBUG']
    print("[%s] %s | %s" % (log_level[level], strftime(
        "%m-%d %H:%M:%S", localtime()), message))


def access(ip_addr, short_url, original_url, is_vip):
    """
    访问状态日志输出函数

    ip_addr = 用户IP
    short_url = 短链接
    original_url = 原始链接
    is_vip = 是否为包月VIP
    """
    print(
        "[INFO] %s | %s | %s --> %s | vip: %s" % (
            strftime("%m-%d %H:%M:%S", localtime()),
            ip_addr,
            short_url,
            original_url,
            is_vip,
        ))
