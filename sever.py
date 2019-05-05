# 功能： 绑定主机2000端口，接收访问请求，返回简单响应并打印
import socket

s = socket.socket()

host = ''
port = 2000
s.bind((host, port))  # 服务器绑定端口

while True:

    s.listen(5)

    connection, address = s.accept()  # recive socket 对象 和地址

    buffer_size = 500
    request_byte = b''

    # recieve all the byte
    while True:
        request = connection.recv(buffer_size)
        request_byte += request
        if len(request) < buffer_size:
            break

    print('requester\'s ip port and request, {}\n{}'.format(address, request_byte.decode('utf-8')))

    response = b'HTTP/1.1 200 OK\r\n\r\n<h1>Hello World!</h1>'

    connection.sendall(response)

    connection.close()
