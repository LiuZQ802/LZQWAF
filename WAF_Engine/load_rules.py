# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Project :  Simple-WAF
@File    :  load_rules
@Author  :  刘子琦
@Data    :  2022/4/25
@Description:
    动态加载规则库，从数据库中加载
"""
from WAF_Engine.waf_db import DataBase
from WAF_Engine.utils import log, change_to_json
import WAF_Engine.config as C
import os

'''
写文件操作
name文件路径
data数据
'''


def write_files(name, data):
    with open(name, 'w+', encoding='utf-8') as f:
        for item in data:
            data_json = change_to_json(item)  # 将字典转换为json
            f.write(data_json + '\n')
    return True


'''
加载url规则
'''


def load_rules_url(db, path):
    name = path + '\\' + C.FILENAME_RULES_URL  # 文件路径
    data = db.get_rules_url()  # 得到的数据是字典形式，所以要转换为json
    flag = write_files(name, data)
    if flag:
        log('url规则加载完毕', 1)


'''
加载GET规则
'''


def load_rules_get(db, path):
    name = path + '\\' + C.FILENAME_RULES_GET  # 文件路径
    data = db.get_rules_get()  # 得到的数据是字典形式，所以要转换为json
    flag = write_files(name, data)
    if flag:
        log('get规则加载完毕', 1)


'''
加载POST规则
'''


def load_rules_post(db, path):
    name = path + '\\' + C.FILENAME_RULES_POST  # 文件路径
    data = db.get_rules_post()  # 得到的数据是字典形式，所以要转换为json
    flag = write_files(name, data)
    if flag:
        log('xss规则加载完毕', 1)


'''
加载封禁的IP信息
'''


def load_ip_prohibit(db, path):
    name = path + '\\' + C.FILENAME_IP_PROHIBIT  # 文件路径
    data = db.get_prohibit_ip()  # 得到被封禁的ip信息，要转化为JSON形式
    flag = write_files(name, data)
    if flag:
        log('封禁ip信息库加载完毕', 1)


'''
    加载规则库，对外调用函数
'''


def load_rules(status):
    path = os.path.join(os.path.dirname(__file__), C.FILE_RULES_PATH)  # 规则库目录
    # 如果文件夹不存在，则创建文件夹
    if not os.path.exists(path):
        os.mkdir(path)
    db = DataBase()  # 连接数据库
    if status == C.LOAD_URL:
        load_rules_url(db, path)  # 加载url规则
    elif status == C.LOAD_GET:
        load_rules_get(db, path)  # 加载get规则
    elif status == C.LOAD_POST:
        load_rules_post(db, path)  # 加载post规则
    elif status == C.LOAD_PROHIBIT:
        load_ip_prohibit(db, path)  # 加载封禁ip规则库
    pass
