# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Project :  Simple-WAF
@File    :  filter
@Author  :  刘子琦
@Data    :  2022/4/23
@Description:
    过滤模块
"""
from WAF_Engine.load_rules import load_rules
from WAF_Engine.utils import change_to_dict, ip_info, url_decode  # 将json转换成字典
from WAF_Engine.logs import add_pass_logs, add_block_logs, ip_is_database
from WAF_Engine.waf_db import DataBase
from WAF_Engine.set_config import get_cc_minutes, get_cc_times
import WAF_Engine.config as C
import re
import datetime
import pytz  # 时区
import os

'''
主要的外部调用函数
'''


def do_filter(client_socket, client_req):
    message = get_message(client_socket, client_req)
    # 首先判断本次访问ip是否被封
    if is_prohibit(message['ip'], message):
        return [C.ACTION_PROHIBIT, message]
    # 判定是否多次请求
    if is_illegal_ask(message, int(get_cc_minutes()), int(get_cc_times())):
        return [C.ACTION_BLOCK, message]
    # 先判断url中是否有敏感目录、敏感文件,有则拦截
    if not do_url(message, message['url']):
        return [C.ACTION_BLOCK, message]
    # 判断GET请求是否有攻击语句,有则拦截
    if not do_get(message, message['url']):
        return [C.ACTION_BLOCK, message]
    if not do_post(message, message['body']):
        return [C.ACTION_BLOCK, message]
    add_pass_logs(message)  # 添加放行日志
    return [C.ACTION_PASS, message]  # 所有匹配完毕，放行
    pass


'''
得到信息
获取信息字典返回
'''


def get_message(client_socket, client_req):
    message = dict()  # 生成字典
    # print(client_req)
    headers, body = client_req.split("\r\n\r\n", 1)  # 分隔http的请求头和请求内容
    ip, port = client_socket.getpeername()  # 得到请求的ip和端口

    timestr = datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S")  # 时间

    method = re.search(C.RE_METHOD, headers).group()  # 匹配METHOD
    url = re.search(C.RE_URL, headers).group()  # 匹配URL
    user_agent = re.search(C.RE_AGENT, headers).group()  # 匹配出User-Agent
    cookie = re.search(C.RE_COOKIE, headers)  # 匹配出cookie
    if cookie:
        cookie = cookie.group()
    message['date'] = timestr
    message['ip'] = ip
    message['port'] = port
    message['method'] = method
    message['url'] = url
    message['body'] = body
    message['user_agent'] = user_agent
    message['cookie'] = cookie
    # 先判断该ip是否在之前出现过，若出现过，直接利用以往信息，没出现过，再去请求
    site = ip_is_database(ip)
    if not site:
        site = ip_info(ip)
    message['country'] = site['country']
    message['city'] = site['city']
    message['proxy'] = site['proxy']
    return message


'''
判断ip是否被封禁
'''


def is_prohibit(ip, message):
    path = os.path.join(os.path.dirname(__file__), C.FILE_RULES_PATH, C.FILENAME_IP_PROHIBIT)
    with open(path, 'r+', encoding='utf-8') as f:
        line = f.readline()
        while line:
            a = change_to_dict(line)
            # on表示启动封禁，off表示暂时取消封禁
            if a['status'] == 'on':
                regular_ip = a['ip']
                if regular_ip == ip:
                    description = '该用户IP被封'
                    types = '非法访问'
                    add_block_logs(message, description, types)  # 添加拦截日志
                    return True  # 表示被封
            line = f.readline()
    return False  # 表示没被封


'''
获取url正则表达式
并判断是否放行
主要是url判断，
'''


def do_url(message, url):
    file_site = ''
    # 如果请求中含有GET请求，将GET请求分割出去,只留下前面请求的目录文件
    if '?' in url:
        file_site = re.search(C.RE_FILES_URL, url).group()
    else:
        file_site = url
    path = os.path.join(os.path.dirname(__file__), C.FILE_RULES_PATH, C.FILENAME_RULES_URL)
    # 从url黑名单中读取正则表达式
    with open(path, 'r+', encoding='utf-8') as f:
        line = f.readline()  # 先读一行
        # 直到所有数据读完
        while line:
            a = change_to_dict(line)  # 将读取到的JSON转换成字典
            if a['status'] == 'on':  # 判断该正则表达式是否打开
                regular = a['regular']  # 获取正则表达式
                # 如果出现违规请求，返回False
                if not is_pass(regular, file_site):
                    message['type'] = a['type']
                    add_block_logs(message, a['description'], a['type'])  # 记录拦截的日志
                    return False
            line = f.readline()
    # 所有匹配都没有，返回True
    return True


'''
处理get请求
如果get请求的内容是url编码或者其他编码，需要先解码才能再去匹配
'''


def do_get(message, url):
    file_site = ''
    # 如果请求中含有GET请求，只留下后面的GET请求
    if '?' in url:
        file_site = re.search(C.RE_GET_URL, url).group()
        info = file_site.split('&')  # 将get请求根据&分隔开来
        lists = []  # 记录分隔出来的get数据,要过滤的数据在这
        for item in info:
            data = re.search(C.RE_GET_SPLIT, item)
            # 有数据，加入列表中
            if data:
                lists.append(data.group())
        lists = url_decode(lists)  # 先进行url解码
        # print(lists)
        path = os.path.join(os.path.dirname(__file__), C.FILE_RULES_PATH, C.FILENAME_RULES_GET)  # 本地规则文件地址
        with open(path, 'r+', encoding='utf-8') as f:
            line = f.readline()  # 一行一行读数据
            while line:
                a = change_to_dict(line)
                if a['status'] == 'on':
                    regular = a['regular']
                    # 如果出现非法请求，返回False
                    # 匹配列表中所有数据
                    for item in lists:
                        if not is_pass(regular, item):
                            message['type'] = a['type']
                            add_block_logs(message, a['description'], a['type'])  # 添加拦截日志
                            return False
                line = f.readline()  # 读下一行
    return True  # 所有数据都正常，放行


'''
判断POST请求
第一个参数表示全部信息，第二个参数表示要处理的post提交信息
'''


def do_post(message, body):
    path = os.path.join(os.path.dirname(__file__), C.FILE_RULES_PATH, C.FILENAME_RULES_POST)  # 本地规则文件地址
    # 先判断是否有文件类型,有说明是文件上传
    if 'Content-Type' in body:
        if not do_post_suffix(message, body, path):  # 先判断文件后缀
            return False
        return do_post_type(message, body, path)

    info = body.split('&')  # 按照&分割数据
    lists = []  # 记录post请求=后面的数据
    lists_front = []  # 记录post请求=之前的数据
    for item in info:
        data = re.search(C.RE_GET_SPLIT, item)
        data_front = re.search(C.RE_POST_SPLIT, item)
        if data:
            data = data.group().replace('+', '')  # 获取数据,并将+替换掉，因为在post请求中+代表空格
            lists.append(data)  # 数据加入列表中
        if data_front:
            lists_front.append(data_front.group())
    lists = url_decode(lists)  # url解码

    ####首先判断是不是登录
    if 'username' in lists_front:
        return do_post_login(message, lists, path)  # 是登录post，进行sql post检查
    ###判断是不是命令执行
    if 'ip' in lists_front:
        return do_post_exe(message, lists, path)
    return do_post_xss(message, lists, path)


'''
文件上传
文件类型判定
'''


def do_post_type(message, body, path):
    data = re.search(C.RE_POST_UPDATE_TYPE, body).group().strip('\r')  # 获取上传文件的类型
    with open(path, 'r+', encoding='utf-8') as f:
        line = f.readline()
        while line:
            a = change_to_dict(line)
            if a['status'] == 'on':
                if a['type'] == '文件上传':
                    if a['description'] == '文件类型':
                        regular = a['regular']
                        if not is_pass(regular, data):
                            return True
            line = f.readline()  # 继续匹配下一条
        # 全部匹配完没有存在在白名单中，则拦截
        message['type'] = a['type']
        add_block_logs(message, a['description'], a['type'])  # 添加拦截日志
        return False


'''
文件上传
文件后缀判断
'''


def do_post_suffix(message, body, path):
    file_name = re.search(C.RE_POST_UPDATE_SUFFIX, body).group().strip('"')  # 获取上传文件的类型
    data = file_name.split('.')[1]  # 按照.分割开，获取文件后缀
    with open(path, 'r+', encoding='utf-8') as f:
        line = f.readline()
        while line:
            a = change_to_dict(line)
            if a['status'] == 'on':
                if a['type'] == '文件上传':
                    if a['description'] == '文件后缀':
                        regular = a['regular']
                        # 黑名单判定
                        if not is_pass(regular, data):
                            message['type'] = a['type']
                            add_block_logs(message, a['description'], a['type'])  # 添加拦截日志
                            return False
            line = f.readline()  # 继续匹配下一条
        # 全部匹配完，不存在黑名单中，则放行
        return True


'''
SQL注入
post登录过滤
data指数据
'''


def do_post_login(message, data, path):
    with open(path, 'r+', encoding='utf-8') as f:
        line = f.readline()
        while line:
            a = change_to_dict(line)  # 加载规则成字典
            # 规则是否开启
            if a['status'] == 'on':
                # 只要sql注入的规则
                if a['type'] == 'sql注入':
                    regular = a['regular']  # 获得正则表达式
                    for item in data:
                        if not is_pass(regular, item):
                            message['type'] = a['type']
                            add_block_logs(message, a['description'], a['type'])  # 添加拦截日志
                            return False
            line = f.readline()  # 读下一行
        return True  # 放行

    pass


'''
XSS
XSS post数据过滤
主要针对存储下xss
'''


def do_post_xss(message, data, path):
    with open(path, 'r+', encoding='utf-8') as f:
        line = f.readline()  # 先读一行
        while line:
            a = change_to_dict(line)  # 转换为dic 数据
            if a['status'] == 'on':
                if a['type'] == 'xss':
                    regular = a['regular']
                    for item in data:
                        if not is_pass(regular, item):
                            message['type'] = a['type']
                            add_block_logs(message, a['description'], a['type'])  # 添加拦截日志
                            return False
            line = f.readline()  # 读取下一行
        return True


'''
命令执行
过滤命令执行post语句中的特殊字符
'''


def do_post_exe(message, data, path):
    with open(path, 'r+', encoding='utf-8') as f:
        line = f.readline()  # 先读一行
        while line:
            a = change_to_dict(line)  # 转换为dic 数据
            if a['status'] == 'on':
                if a['type'] == '命令执行':
                    regular = a['regular']
                    for item in data:
                        if not is_pass(regular, item):
                            message['type'] = a['type']
                            add_block_logs(message, a['description'], a['type'])  # 添加拦截日志
                            return False
            line = f.readline()  # 读取下一行
        return True


'''
非法多次请求过滤
minutes表示多少时间内以分钟为单位
times表示次数，定义几minutes内几次请求为多次非法请求
如果判断是非法多次请求，那么将给予拦截，并封禁IP
'''


def is_illegal_ask(message, minutes, times):
    db = DataBase()
    url = re.search(C.RE_FILES_URL, message['url'])  # 去掉GET请求的请求数据,即获取纯URL
    if url:
        url = url.group()
    else:
        url = message['url']
    ip = message['ip']
    now_date = message['date']
    # 几分钟前的时间
    rencent_date = (datetime.datetime.now() - datetime.timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S")
    # 数据库放行日志中搜索一段时间内某个ip对某个url的请求次数，返回一个列表，列表最多有两个参数，一个POST，一个GET，或者只有POST，只有GET
    nums = db.select_ip_times(ip, now_date, rencent_date, url)
    lists = []
    for item in nums:
        lists.append(item['num'])
    # lists列表空代表以前没有访问过，直接放行
    if not lists:
        return False
    max_num = max(lists)  # minutes内最大访问量
    # 如果大于最大访问量
    if max_num > times:
        message['type'] = 'CC'
        add_block_logs(message, '非法多次请求', message['type'])  # 添加拦截日志
        # 封IP
        # 先判断是否在黑名单中,若在将状态打开，因为状态已经打开的话肯定就直接拦截了
        ip_backlists = db.get_prohibit_ip()
        for item in ip_backlists:
            if item['ip'] == ip:
                db.change_prohibit_status(item['id'], 'on')
                load_rules(C.LOAD_PROHIBIT)  # 更新本地IP黑名单缓存
                return True  # 这样就不用再添加黑名单了，直接返回拦截
        db.add_prohibit_ip(ip, now_date, 'on')
        load_rules(C.LOAD_PROHIBIT)  # 更新本地IP黑名单缓存
        return True  # 表示是非法访问
    return False


'''
url正则判定
是否放行
传进正则表达式和需要过滤的字符串
'''


def is_pass(regular, message):
    a = re.search(regular, message, re.IGNORECASE)  # 第三个参数表示不区分大小写
    if a:  # 如果能匹配出来东西，说明有黑名单中内容
        return False
    return True


if __name__ == '__main__':
    pass
