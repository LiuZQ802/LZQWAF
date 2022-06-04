# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Project :  Simple-WAF
@File    :  response
@Author  :  刘子琦
@Data    :  2022/4/23
@Description:
    代理服务器将客户发送过来的请求处理替换相关信息后发送给真实服务器
    真实服务器发出response，被代理服务器接受
    然后代理服务器接受到回应之后再返还给客户-------------pass
    拦截函数是指直接把客户请求拦截
    log记录日志
"""

import socket
import urllib.request
import WAF_Engine.config as C
from WAF_Engine.utils import log
from WAF_Engine.logs import add_error_logs
from WAF_Engine.set_config import get_real_host, get_real_port

'''
根据动作选择处理方法
client_socket指客户端的socket
proxy_req指代理服务器接受客户请求后再经过过滤的请求信息
action表示动作模块

BLOCK  拦截
PASS  通过
LOG  记录日志
'''


def do_response(client_socket, proxy_req, message, action):
    if action == C.ACTION_PROHIBIT:
        response_prohibit(client_socket, message)
    elif action == C.ACTION_PASS:
        response_pass(client_socket, proxy_req)
    elif action == C.ACTION_BLOCK:
        response_block(client_socket, message)


"""
PASS
正常放行
"""


def response_pass(client_socket, client_req):
    real_host = get_real_host()  # 真实内容服务器ip地址，并实现负载均衡
    real_port = int(get_real_port())  # 真实服务器端口
    proxy_req = client_req.replace('keep-alive'.encode(), 'close'.encode())
    proxy_client_socket = socket.socket()
    try:
        proxy_client_socket.connect((real_host, real_port))  # 连接真实服务器
        proxy_client_socket.sendall(proxy_req)  # 请求发送给真实服务器
        '''
             接受真实服务器的response
           '''
        real_resp = b''
        BUF_SIZE = 1024
        try:
            while True:
                data = proxy_client_socket.recv(BUF_SIZE)
                real_resp += data
                if not data:
                    break
            # 说明数据接完
        except Exception as e:
            print(e)
        log("服务器回应\n", 1)
        # 将真实服务器回应给代理服务器的信息，处理发给客户
        proxy_resp = real_resp.replace('Connection: close'.encode(), 'Connection: keep-alive'.encode())
        client_socket.sendall(proxy_resp)
        client_socket.close()
    except Exception as e:
        error = '服务器连接失败'
        add_error_logs(error, str(e))  # 添加运行错误日志

    pass


'''
BLOCK
拦截
'''


def response_block(client_socket, message):
    # 请求本地拦截页面
    url = 'http://127.0.0.1:677/intercept_page'
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read()

    # 替换关键信息
    real_response = response.replace('ip地址demo'.encode(), message['ip'].encode())
    real_response = real_response.replace('时间demo'.encode(), message['date'].encode())
    real_response = real_response.replace('类型demo'.encode(), message['type'].encode())
    client_socket.sendall(real_response)
    client_socket.close()
    pass


'''
封禁
'''


def response_prohibit(client_socket, message):
    url = 'http://127.0.0.1:677/prohibit_page'
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read()
    # 替换关键信息
    real_response = response.replace('ip地址demo'.encode(), message['ip'].encode())
    real_response = real_response.replace('时间demo'.encode(), message['date'].encode())
    # real_response = real_response.replace('类型demo'.encode(), message['type'].encode())
    client_socket.sendall(real_response)
    client_socket.close()
