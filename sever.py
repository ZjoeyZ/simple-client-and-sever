import socket

s = socket.socket()

host = ''
port = 2000
s.bind((host, port))  #服务器绑定端口

while True:

    s.listen(5)
    
    connection, address = s.accept()
    
    request = connection.recv(1024)

    print('ip and request, {}\n{}'.format(address, request.decode('utf-8')))

    response = b'HTTP/1.1 200 OK\r\n\r\n<h1>Hello World!</h1>'
    
    connection.sendall(response)

    connection.close()
