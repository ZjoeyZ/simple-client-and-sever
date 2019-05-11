# 功能：绑定主机3000端口，接收访问请求，解析得到request对象，根据请求路径不同返回不同响应
import time
import socket
import urllib.parse


# from routes import route_static
# from routes import route_dict


def log(*args, **kwargs):
    """
    新的print函数，自动打印时间
    """
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


class Request(object):
    """
    定义一个 class 用于保存请求的数据
    """

    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''

    def form(self):
        """
        form 函数用于把 body 解析为一个字典并返回
        body 的格式如下 a=b&c=d&e=1
        """
        # username=1 2&a?&password=         真实输入
        # username=1+2%26a%3F&password=     转码过后
        args = self.body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            # 特殊符号转码
            v = urllib.parse.unquote(v)
            f[k] = v
        return f


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def parsed_path(path):
    """
    parsed_path 用于把 path 和 query 分离
    query 转 字典
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query)

    r = {
        # '/static': route_static,
        # '/': route_index,
        # '/login': route_login,
        # '/messages': route_message,
    }
    # r.update(route_dict)
    response = r.get(path, error)
    return response(request)


def run(host='', port=3000):
    """
    启动服务器
    """
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            buffer_size = 1024
            r = b''
            while True:
                request_b = connection.recv(buffer_size)
                r += request_b
                if len(request_b) < buffer_size:
                    break
            r = r.decode('utf-8')
            log('原始请求\r\n', r)
            # chrome 会发送空请求，判断一下防止程序崩溃
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            # 设置 request 的 method
            request.method = r.split()[0]
            # 把 body 放入 request 中
            request.body = r.split('\r\n\r\n', 1)[1]
            # 用 response_for_path 函数来得到 path 对应的响应内容
            response = response_for_path(path)
            connection.sendall(response)
            connection.close()


request = Request()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
