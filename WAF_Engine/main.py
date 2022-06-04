# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Project :  Simple-WAF
@File    :  main
@Author  :  刘子琦
@Data    :  2022/4/23
@Description:
    主函数
    接受请求
"""

import socket
import re
import sys
import threading
from WAF_Engine.utils import log
import WAF_Engine.config as C
from WAF_Engine.response import do_response
from WAF_Engine.filter import do_filter
from WAF_Engine.logs import add_error_logs
from WAF_Engine.set_config import get_proxy_port, get_waf_status

'''
接受客户端请求
参数传客户端socket
接收到请求后先过滤
然后判断是否回送给真实内容服务器
'''


def handle_response(client_socket):
    BUF_SIZE = 1024  # 缓冲区大小
    client_socket.settimeout(C.CLIENT_SOCKET_TIMEOUT)  # 设置超时时间
    client_req = b''  # 接收的请求
    try:
        # 一直读取
        while True:
            data = client_socket.recv(BUF_SIZE)
            client_req += data
            if len(data) < BUF_SIZE:  # 如果接收的数据小于缓冲区大小,说明要么数据传输完毕，要么可能有post请求数据没接收
                temp_req = client_req.decode()  # 对已接收的所有数据进行解码
                temp_data = re.search(C.RE_COTENT_LENGTH, temp_req)  # 搜索是否有content-length
                if temp_data:
                    # 如果有content-length，那么就再接收相应大小数据
                    length_str = temp_data.group()
                    length = int(length_str)
                    # 设置超时时间，用来及时退出那些已经把所有数据都接受完，但得等待的socket，例如登录或者其他post请求内容很短的请求
                    client_socket.settimeout(0.5)
                    data = client_socket.recv(length)
                    client_req += data
                break
    except Exception as e:
        log("超时了。。。", 2)
        print(e)
    if not client_req:
        log("出现空请求", 1)
        return
    client_re = client_req.decode('utf-8', 'ignore')
    # 防火墙开
    if get_waf_status() == 'True':
        action, message = do_filter(client_socket, client_re)  # 返回行为，PASS|BLOCK|PROHIBIT
        do_response(client_socket, client_req, message, action)
    else:
        do_response(client_socket, client_req, '', C.ACTION_PASS)  # 防火墙关,所有请求直接放行

def main():
    # 代理服务器的socket
    proxy_server_socket = socket.socket()
    proxy_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # socket关闭后立即释放端口
    try:
        proxy_server_socket.bind(("0.0.0.0", int(get_proxy_port())))
    except Exception as e:
        error = '套接字绑定失败'
        add_error_logs(error, str(e))
        return
    proxy_server_socket.listen(1024)
    while True:
        client_socket, addr = proxy_server_socket.accept()

        log("建立连接", 1)

        log(str(client_socket.getpeername()) + "--->" + str(client_socket.getsockname()), 1)
        thread = threading.Thread(target=handle_response, args=(client_socket,))
        thread.setDaemon(True)  # 设置守护进程
        thread.start()
        thread_num=len(threading.enumerate())
        print(thread_num)
        print(str(threading.enumerate()))
    pass


if __name__ == '__main__':
    main()
