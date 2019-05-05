# 功能：接收用户输入的url，解析，访问用户想要访问的网址，接收响应并打印
import socket
import ssl


# 1，parsed url 得到 protocol, host, port, path
# 2，根据protocol，生产socket对象
# 3，根据host和port，利用socket连接
# 4，生成二进制请求，利用socket发送
# 5，利用socek接收请求，并解码
# 6，解析请求，判断是否重定位，返回status_code, headers, body
# 7，打印 整数status_code,字典headers, 响应body

def parsed_url(url):
    """
    解析 url 返回 (protocol host port path)
    """
    # 检查协议
    protocol = 'http'
    if url[:7] == 'http://':  # 检查前7个字符
        u = url.split('://')[1]
        # split()通过指定分隔符对字符串进行切片，得字符串数组，不包含分隔符
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        # '://' 定位 然后取第一个 / 的位置来切片
        u = url

    # 检查默认 path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # 默认端口
    port_dict = {
        'http': 80,
        'https': 443,
    }
    port = port_dict[protocol]

    # 检查端口
    # if host.find(':') != -1:
    if ':' in host:
        h = host.split(':')
        host = h[0]
        port = int(h[1])

    # 返回一个tuple
    return protocol, host, port, path


def socket_by_protocol(protocol):
    """
    根据协议返回一个 socket 实例
    """
    if protocol == 'http':
        s = socket.socket()
    else:
        # HTTPS 协议需要使用 ssl.wrap_socket 包装一下原始的 socket
        # 连接443端口，http连接80端口
        s = ssl.wrap_socket(socket.socket())
    return s


def response_by_socket(s):
    """
    参数是一个 socket 实例
    返回这个 socket 读取的所有数据
    """
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


def parsed_response(r):
    """
    把 response 解析出 状态码 headers body 返回
    状态码是 int
    headers 是 dict
    body 是 str
    """
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    # HTTP/1.1 200 ok
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v
    return status_code, headers, body


# 其中复杂的逻辑全部封装成上面的函数
def get(url):
    """
    用 GET 请求 url 并返回响应
    """
    protocol, host, port, path = parsed_url(url)

    s = socket_by_protocol(protocol)

    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    # connection:close 告诉服务器发完数据就可以断开了，这样才可以recieve
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = response_by_socket(s)
    r = response.decode(encoding)

    status_code, headers, body = parsed_response(r)
    if status_code in [301, 302]:
        url = headers['Location']
        return get(url)

    return status_code, headers, body


def main():
    url = 'http://movie.douban.com/top250'
    status_code, headers, body = get(url)
    print('status code:', status_code)
    print('headers:{}'.format(headers))
    print('body:', body)


if __name__ == '__main__':
    main()
