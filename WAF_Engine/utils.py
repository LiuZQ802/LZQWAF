# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Project :  Simple-WAF
@File    :  utils
@Author  :  刘子琦
@Data    :  2022/4/23
@Description:
    常用小工具插件
    @日志输出工具
    @根据ip地址定位信息的小工具
"""
import random

import WAF_Engine.config as C
import urllib.request
import json
from urllib.parse import unquote  # 实现url解码

'''
一个日志输出工具
参数:messgae 表示日志信息
    level 表示级别:0:正常输出白色;1:debug级别绿色;2:waring级别红色
'''


def log(message, level=0):
    color_common = ''  # 正常颜色
    color_green = '\033[1;32m[+]'  # 绿色[+]
    color_red = '\033[1;31m[!]'  # 红色[!]

    output = ''

    if level == 0:
        output = color_common + message
    elif level == 1:
        output = color_green + message
    elif level == 2:
        output = color_red + message
    else:
        raise ValueError("level cannot be " + str(level) + '!!!')

    if C.DEBUG_LEVEL <= level and C.DEBUG_LEVEL != -1:
        print(output)

    # 还原颜色
    print('\033[1;0m', end='')

    pass


'''
定位ip信息的攻击
通过传参ip，获取信息
获取 状态 国家 省 市 是否使用代理  ip
调用的API接口为：http://ip-api.com/json/{ip}?lang=zh-CN&fields=155673
'''


def ip_info(ip):
    message = {'country': None, 'city': None, 'proxy': None}
    url = 'http://ip-api.com/json/%s?lang=zh-CN&fields=155673' % ip  # API接口
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        data = response.read().decode('utf-8')
        dict = change_to_dict(data)  # 加载JSON
        if dict['status'] == 'success':  # 请求成功
            message = {'country': dict['country'], 'city': dict['regionName'] + dict['city'], 'proxy': dict['proxy']}
    except:
        pass
    # print(dict)
    # print(message)
    return message


'''
将字典转换为json
'''


# 将数据转换为json
def change_to_json(data):
    data = json.dumps(data,ensure_ascii=False)
    return data


'''
将json转换成字典
'''


def change_to_dict(data):
    data = json.loads(data)
    return data


'''
url解码
'''


def url_decode(lists):
    new_lists = []
    i=0
    for item in lists:
        # 如果有%存在，说明是还需再解码,while循环不断解码
        while '%' in item:
            # print(item)
            item = unquote(item, 'utf-8')
            #最多经过五次解码
            i+=1
            if i==5:
                break
        new_lists.append(item)
    return new_lists


if __name__ == '__main__':
    # ip_info('49.78.212.59')
    dict={'i':'sql注入'}
    json=change_to_json(dict)

    print(json)
