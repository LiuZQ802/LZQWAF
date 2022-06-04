# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Project :  Simple-WAF
@File    :  set_config
@Author  :  刘子琦
@Data    :  2022/4/24
@Description:
    写一些配置文件
    或者修改获取配置文件信息
"""
import configparser
import os

'''
配置一些基本配置文件
'''


def write_conf():
    conf = configparser.ConfigParser()
    # WAF基本配置
    conf['WAF'] = {'WAF_CONFIG': True, 'REAL_HOST': '192.168.109.154', 'REAL_PORT': 80, 'PROXY_HOST': '127.0.0.1',
                   'PROXY_PORT': 80, 'SERVICE_NAME': 'HTTP'}
    # 数据库基本配置
    conf['DATABASE'] = {'DATABASE_HOST': '192.168.109.155', 'DATABASE_USER': 'root', 'DATABASE_PASSWD': '001003',
                        'DATABASE_NAME': 'waf'}
    # CC攻击拦截参数设置
    conf['CC'] = {'MINUTES': 1, 'TIMES': 100}
    path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
    with open(path, 'w') as f:
        conf.write(f)


####################对防火墙配置的操作#################################

# 获取防火墙状态
def get_waf_status():
    conf = configparser.ConfigParser()
    path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
    conf.read([path])
    waf_config = conf.get('WAF', 'WAF_CONFIG')
    return waf_config


# 修改防火墙状态
def set_waf_status(status):
    conf = configparser.ConfigParser()
    try:
        path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
        conf.read(path)
        conf.set('WAF', 'WAF_CONFIG', status)
        with open(path, 'w') as f:
            conf.write(f)
        return True
    except:
        return False


# 获取内容服务器真实IP
def get_real_host():
    conf = configparser.ConfigParser()
    path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
    conf.read([path])
    real_host = conf.get('WAF', 'REAL_HOST')
    return real_host


# 修改内容服务器真实IP
def set_real_host(host):
    conf = configparser.ConfigParser()
    try:
        path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
        conf.read(path)
        conf.set('WAF', 'REAL_HOST', host)
        with open(path, 'w') as f:
            conf.write(f)
        return True
    except:
        return False


# 获取内容服务器真实真实端口
def get_real_port():
    conf = configparser.ConfigParser()
    path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
    conf.read([path])
    real_port = conf.get('WAF', 'REAL_PORT')
    return real_port


# 修改内容服务器真实端口
def set_real_port(port):
    conf = configparser.ConfigParser()
    try:
        path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
        conf.read(path)
        conf.set('WAF', 'REAL_PORT', port)
        with open(path, 'w') as f:
            conf.write(f)
        return True
    except:
        return False


# 获得防火墙代理服务器的IP
def get_proxy_host():
    conf = configparser.ConfigParser()
    path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
    conf.read([path])
    proxy_host = conf.get('WAF', 'PROXY_HOST')
    return proxy_host


# 设置防火墙代理服务器IP
def set_proxy_host(host):
    conf = configparser.ConfigParser()
    try:
        path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
        conf.read(path)
        conf.set('WAF', 'PROXY_HOST', host)
        with open(path, 'w') as f:
            conf.write(f)
        return True
    except:
        return False


# 获得防火墙代理服务器端口
def get_proxy_port():
    conf = configparser.ConfigParser()
    path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
    conf.read([path])
    proxy_port = conf.get('WAF', 'PROXY_PORT')
    return proxy_port


# 修改防火墙代理服务器端口
def set_proxy_port(port):
    conf = configparser.ConfigParser()
    try:
        path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
        conf.read(path)
        conf.set('WAF', 'PROXY_PORT', port)
        with open(path, 'w') as f:
            conf.write(f)
        return True
    except:
        return False


# 获得服务器名称
def get_service_name():
    conf = configparser.ConfigParser()
    path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
    conf.read([path])
    service_name = conf.get('WAF', 'SERVICE_NAME')
    return service_name


# 修改服务器名称
def set_service_name(name):
    conf = configparser.ConfigParser()
    try:
        path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
        conf.read(path)
        conf.set('WAF', 'SERVICE_NAME', name)
        with open(path, 'w') as f:
            conf.write(f)
        return True
    except:
        return False

####################对防火墙数据库的基本操作##################################
# 获得数据库IP
def get_database_ip():
    conf = configparser.ConfigParser()
    path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
    conf.read([path])
    database_host = conf.get('DATABASE', 'DATABASE_HOST')
    return database_host


# 修改数据库IP
def set_database_ip(ip):
    conf = configparser.ConfigParser()
    try:
        path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
        conf.read(path)
        conf.set('DATABASE', 'DATABASE_HOST', ip)
        with open(path, 'w') as f:
            conf.write(f)
        return True
    except:
        return False


# 获得数据库用户名和密码
def get_database_login_info():
    conf = configparser.ConfigParser()
    path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
    conf.read([path])
    user = conf.get('DATABASE', 'DATABASE_USER')
    passwd = conf.get('DATABASE', 'DATABASE_PASSWD')
    return [user, passwd]


# 修改数据库用户名密码
def set_database_login_info(user, passwd):
    conf = configparser.ConfigParser()
    try:
        path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
        conf.read(path)
        conf.set('DATABASE', 'DATABASE_USER', user)
        conf.set('DATABASE', 'DATABASE_PASSWD', passwd)
        with open(path, 'w') as f:
            conf.write(f)
        return True
    except:
        return False


# 得到数据库库名
def get_database_name():
    conf = configparser.ConfigParser()
    path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
    conf.read([path])
    database_name = conf.get('DATABASE', 'DATABASE_NAME')
    return database_name


# 设置数据库库名
def set_database_name(name):
    conf = configparser.ConfigParser()
    try:
        path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
        conf.read(path)
        conf.set('DATABASE', 'DATABASE_NAME', name)
        with open(path, 'w') as f:
            conf.write(f)
        return True
    except:
        return False


#######################CC攻击防范参数设置############################
# 获得几分钟，表市判断几分钟内的
def get_cc_minutes():
    conf = configparser.ConfigParser()
    path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
    conf.read([path])
    cc_minutes = conf.get('CC', 'MINUTES')
    return cc_minutes


# 设置分钟
def set_cc_minutes(minutes):
    conf = configparser.ConfigParser()
    try:
        path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
        conf.read(path)
        conf.set('CC', 'MINUTES', minutes)
        with open(path, 'w') as f:
            conf.write(f)
        return True
    except:
        return False


# 获得最大访问次数
def get_cc_times():
    conf = configparser.ConfigParser()
    path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
    conf.read([path])
    cc_times = conf.get('CC', 'TIMES')
    return cc_times


# 设置最大访问数
def set_cc_times(times):
    conf = configparser.ConfigParser()
    try:
        path = os.path.join(os.path.dirname(__file__), 'WAF_CONF')
        conf.read(path)
        conf.set('CC', 'TIMES', times)
        with open(path, 'w') as f:
            conf.write(f)
        return True
    except Exception as e:
        print(e)
        return False
