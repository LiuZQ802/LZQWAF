# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Project :  Simple-WAF
@File    :  logs
@Author  :  刘子琦
@Data    :  2022/4/26
@Description:
    记录日志
"""
import re
import WAF_Engine.config as C
from WAF_Engine.waf_db import DataBase
import datetime
import pytz

'''
添加PASS日志信息 
'''


def add_pass_logs(message):
    db = DataBase()
    # 放行日志
    info = {'date': message['date'], 'ip': message['ip'], 'port': message['port'], 'country': message['country'],
            'city': message['city'],
            'proxy': message['proxy'], 'method': message['method'], 'url': message['url']}
    url = re.search(C.RE_FILES_URL, info['url'])  # 去掉GET请求的请求数据
    if url:
        info['url'] = url.group()
    db.add_logs_waf_pass(info)


'''
添加BLOCK日志
message表示基本信息
action表示描述
type表示非法请求的行为 类别
'''


def add_block_logs(message, action, type):
    db = DataBase()
    # 拦截日志
    info = {'date': message['date'], 'ip': message['ip'], 'port': message['port'], 'country': message['country'],
            'city': message['city'],
            'proxy': message['proxy'], 'method': message['method'], 'url': message['url'], 'type': type,
            'action': action}
    url = re.search(C.RE_FILES_URL, info['url'])  # 去掉GET请求的请求数据
    if url:
        info['url'] = url.group()
    db.add_logs_waf_block(info)


'''
添加允许错误日志
'''


def add_error_logs(error, exception):
    db = DataBase()
    timestr = datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S")  # 时间
    info = {'date': timestr, 'error': error, 'exception': exception}
    db.add_logs_waf_error(info)


'''
查看ip是否在数据库中存在过
若存在，返回国家、城市、代理
防止一个ip多次请求，这将会多次调用API，影响请求速度
'''


def ip_is_database(ip):
    db = DataBase()
    lists = db.get_logs_waf_pass_ip(ip)  # 根据ip查询放行日志信息
    if lists:  # 如果有记录
        dict = lists[0]  # 取一条数据
        info = dict['info']
        message = {'country': info['country'], 'city': info['city'], 'proxy': info['proxy']}  # 获取日志信息
        return message
    lists = db.get_logs_waf_block_ip(ip)  # 如果放行日志里没有，就访问拦截日志
    if lists:  # 如果有记录
        dict = lists[0]  # 取一条数据
        info = dict['info']
        message = {'country': info['country'], 'city': info['city'], 'proxy': info['proxy']}  # 获取日志信息
        return message
    # 拦截日志和放行日志都没有，返回空
    return None


if __name__ == '__main__':
    data = ip_is_database('127.0.0.1')
    print(data)
