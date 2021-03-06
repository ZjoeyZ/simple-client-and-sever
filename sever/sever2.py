# 功能：绑定主机3000端口，接收访问请求，解析得到path，根据path不同返回不同响应
import socket


def log(*args, **kwargs):
    """
    用这个 log 替代 print
    """
    print('log', *args, **kwargs)


def route_index():
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello World</h1><img src="sever2_doge.gif"/>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_image():
    """
    图片的处理函数, 浏览器img标签会发出这个请求，读取图片并生成响应返回
    """
    with open('sever2_doge.gif', 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


# route_path_not_exsit()
def error(code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # HTTP 协议中 code 都是数字似乎更方便所以打破了不要用数字来作为字典的 key原则
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def response_for_path(path):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {
        '/': route_index,
        '/sever2_doge.gif': route_image,
    }
    response = r.get(path, error)
    return response()


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    with socket.socket() as s:
        s.bind((host, port))
        # 无限循环来处理请求
        while True:
            # 监听 接受 读取请求数据 解码成字符串
            s.listen(5)
            connection, address = s.accept()
            request = connection.recv(1024)
            request = request.decode('utf-8')
            log('ip and request, {}\n{}'.format(address, request))
            try:
                # 因为 chrome 会发送空请求导致 split 得到空 list
                # 所以这里用 try 防止程序崩溃
                path = request.split()[1]
                # 用 response_for_path 函数来得到 path 对应的响应内容
                response = response_for_path(path)
                # 把响应发送给客户端
                connection.sendall(response)
            except Exception as e:
                log('error', e)
            # 处理完请求, 关闭连接
            connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    # 字典解包，传参 key = word
    run(**config)
