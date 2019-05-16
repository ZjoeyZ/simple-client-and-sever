#只有修改了的代码，其他和前面的sever4一样

import socket
import urllib.parse

from utils import log

from routes import route_static
from routes import route_dict



# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self):
        self.headers = {}
        self.cookies = {}

    def add_cookies(self):
        """
        把headers里的cookies字段取出来
        生成一个字典，｛string：string｝
        加入request对象，
        """
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        log('cookie', kvs)
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v

    def add_headers(self, header):
        """
        传入的header参数如下所示
        [
            'Accept-Language: xxxxxx'
            'Cookie: x=xx; xx=xxx'
        ]
        解析得到字典
        """
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        # 清除 上次的cookies
        self.cookies = {}
        #加入新cookie
        self.add_cookies()



