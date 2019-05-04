import socket

s = socket.socket()

host = ''
port = 2000
s.bind((host, port))  #服务器绑定端口

while True:

    s.listen(5)
    
    connection, address = s.accept()#recive socket 对象 和地址

    buffer_size = 500
    request_byte = b''

    #recieve all the byte
    while True:
        request = connection.recv(buffer_size)
        request_byte += request
        if len(request) < buffer_size:
            break

    print('requester\'s ip port and request, {}\n{}'.format(address, request_byte.decode('utf-8')))

    response = b'HTTP/1.1 200 OK\r\n\r\n<h1>Hello World!</h1>'
    
    connection.sendall(response)

    connection.close()

# 1,浏览器访问 http://localhost:2000/

# 2,服务器第一次返回
# requester's ip port and request, ('127.0.0.1', 1035)
# GET / HTTP/1.1
# Host: localhost:2000 #说明浏览器请求的是谁
# .......

# 2，服务器第二次返回
# GET /favicon.ico HTTP/1.1
# Host: localhost:2000

#User-Agent:
    # Mozilla/5.0 (Windows NT 10.0; Win64; x64)
    # AppleWebKit/537.36 (KHTML, like Gecko) 苹果内核
    # Chrome/73.0.3683.103 我是谷歌，我的版本是
    # Safari/537.36

# User-Agent:
    # Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0)
    # Gecko/20100101    火狐内核
    # Firefox/66.0  我是火狐，我的版本是


# q=0.8
# Accept: image/webp,*/*（任意对象任意类型）
    # WebP格式，谷歌（google）开发的一种旨在加快图片加载速度的图片格式。
    # 图片压缩体积大约只有JPEG的2/3，并能节省大量的服务器宽带资源和数据空间。
# Accept-Language: zh-CN,zh;q=0.8（权重，优先级）,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate算法（压缩格式）
# Accept-Language: zh-CN,zh（中文-大陆）;q=0.8,zh-TW（中文-台湾）;q=0.7,zh-HK（中文-香港）;q=0.5,en-US;q=0.3,en;q=0.2
# Connection: keep-alive #保持connection不中断，便于请求多次，比如图片等
# Cache-Control: max-age=0
