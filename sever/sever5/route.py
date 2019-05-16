# 只有route_login和生成session有关
# 其他的route都只有增加了得到用户信息，和将入这个信息到template的代码，这里也一并忽略

from utils import log
from models import Message
from models import User

import random

session = {

}


def random_str():
    """
    生成一个随机的字符串
    """
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 1)
        s += seed[random_index]
    return s


def response_with_headers(headers):
    """
        headers字典转字符串
    """
    header = 'HTTP/1.1 210 VERY OK\r\n'
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '【游客】')
    return username


def route_login(request):
    """
    登录页面的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    log('login, cookies', request.cookies)
    # seesion对比得到用户信息
    username = current_user(request)

    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            # 设置一个随机字符串来当令牌使用
            session_id = random_str()
            session[session_id] = u.username
            log('new session', session)
            # 下面是把session存入 cookie 中
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            username = u.username
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''

    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    log('login 的响应', r)
    return r.encode(encoding='utf-8')
