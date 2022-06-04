# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Project :  Simple-WAF
@File    :  waf_db
@Author  :  刘子琦
@Data    :  2022/4/24
@Description:
    数据库的一些操作
"""
import datetime

import pytz

import WAF_Engine.config as C
import pymysql
from WAF_Engine.utils import change_to_json, change_to_dict, log  # 将字典转换为json，将json转换成字典
from WAF_Engine.set_config import get_database_ip, get_database_login_info, get_database_name


class DataBase:
    __db = ''  # 数据库对象

    def __init__(self):
        self.__db = self.__get_db()  # 获得数据库对象
        pass

    def __del__(self):
        self.__db.close()  # 关闭数据库

    # 连接数据库
    def __get_db(self):
        # 获取数据库信息
        host = get_database_ip()
        user = get_database_login_info()[0]
        password = get_database_login_info()[1]
        db = get_database_name()

        try:
            db = pymysql.connect(host=host, user=user, password=password, db=db)
            return db
        except Exception as e:
            log('数据库连接失败', 2)
            print(e)

    # 执行sql语句
    def __execute(self, sql):
        cursor = self.__db.cursor()
        cursor.execute(sql)
        return cursor

    # 返回数据库句柄
    def get_db(self):
        return self.__db

    # 搜索rules的函数
    def __select_rules(self, table):
        sql = 'SELECT * FROM `{}`;'.format(table)
        list = []
        try:
            cursor = self.__execute(sql)
            self.__db.commit()
            if table == C.TABLENAME_IP_PROHIBIT:
                for temp in cursor.fetchall():
                    dict = {'id': temp[0], 'ip': temp[1], 'date': temp[2], 'status': temp[3]}
                    list.append(dict)
            else:
                for temp in cursor.fetchall():
                    dict = {'id': temp[0], 'regular': temp[1], 'type': temp[2], 'description': temp[3],
                            'status': temp[4]}
                    list.append(dict)
            return list
        except Exception as e:
            log('sql执行错误----规则查询错误', 2)
            print(e)

    # 搜索日志信息
    def __select_logs(self, table):
        sql = 'SELECT * FROM `{}`;'.format(table)
        list = []
        try:
            cursor = self.__execute(sql)
            self.__db.commit()
            for temp in cursor.fetchall():
                dict = {'id': temp[0]}
                info = change_to_dict(temp[1])
                dict['info'] = info
                list.append(dict)
            return list
        except Exception as e:
            log('sql执行错误----日志搜索错误', 2)
            print(e)

    # 根据IP查询日志信息
    def __select_logs_ip(self, table, ip):
        sql = 'SELECT * FROM `{}` WHERE info->"$.ip"="{}";'.format(table, ip)
        lists = []
        try:
            cursor = self.__execute(sql)
            self.__db.commit()
            for temp in cursor.fetchall():
                dict = {'id': temp[0]}
                info = change_to_dict(temp[1])
                dict['info'] = info
                lists.append(dict)
            return lists
        except Exception as e:
            log('sql执行错误----日志搜索错误', 2)
            print(e)

    # 添加rules的函数,info字典形式,返回是否插入成功
    def __add_rules(self, table, info):
        # 插入的sql语句
        sql = '''
            INSERT INTO `{table}`(`regular`,`type`,`description`,`status`)VALUES('{regular}','{type}','{description}','{status}');
        '''.format(table=table, regular=info['regular'], type=info['type'], description=info['description'],
                   status=info['status'])
        try:
            cursor = self.__execute(sql)
            self.__db.commit()
            return True
        except Exception as e:
            self.__db.rollback()  # 出错回滚
            log('sql执行错误----规则插入失败', 2)
            print(e)
            return False

    # 添加日志信息,注意:info是json数据
    def __add_logs(self, table, info):
        info = change_to_json(info)
        sql = '''
            INSERT INTO `{table}`(`info`)VALUES('{info}');
        '''.format(table=table, info=info)
        # print(sql)
        try:
            cursor = self.__execute(sql)
            self.__db.commit()
            return True
        except Exception as e:
            self.__db.rollback()  # 出错回滚
            log('sql执行错误----日志插入失败', 2)
            print(e)
            return False

    # 删除rules、logs的函数,根据id删除
    def __delete_info(self, table, id):
        # 删除的sql语句
        sql = '''
            DELETE FROM `{table}` WHERE `ID`={id};
        '''.format(table=table, id=id)
        try:
            cursor = self.__execute(sql)
            self.__db.commit()
            return True
        except Exception as e:
            self.__db.rollback()
            log('sql执行错误----日志或规则删除失败', 2)
            print(e)
            return False

    # 清空日志
    def __delete_logs(self, table):
        # 删除的sql语句
        sql = '''
                    DELETE FROM `{table}`;
                '''.format(table=table)
        try:
            cursor = self.__execute(sql)
            self.__db.commit()
            return True
        except Exception as e:
            self.__db.rollback()
            log('sql执行错误----日志清空失败', 2)
            print(e)
            return False

    # 修改规则状态
    def __change_rules_status(self, table, id, status):
        sql = '''
                    UPDATE `{table}` SET `status`='{status}' WHERE `id`={id};
                '''.format(table=table, status=status, id=id)
        try:
            cursor = self.__execute(sql)
            self.__db.commit()
            return True
        except Exception as e:
            self.__db.rollback()
            log('sql执行错误---修改规则状态', 2)
            print(e)
            return False

    # 得到rules_url表中的信息，以列表形式返回
    def get_rules_url(self):
        table = C.TABLENAME_RULES_URL  # 表名
        return self.__select_rules(table)

    # 得到rules_sql表中的信息，以列表形式返回
    def get_rules_get(self):
        table = C.TABLENAME_RULES_GET  # 表名
        return self.__select_rules(table)

    # 得到rules_xss表中的信息，以列表形式返回
    def get_rules_post(self):
        table = C.TABLENAME_RULES_POST  # 表名
        return self.__select_rules(table)

    # 插入rules_url表中的信息,返回是否插入成功，传入字典参数
    def add_rules_url(self, info):
        table = C.TABLENAME_RULES_URL  # 表名
        return self.__add_rules(table, info)

    # 插入rules_sql表中的信息,返回是否插入成功，传入字典参数
    def add_rules_get(self, info):
        table = C.TABLENAME_RULES_GET  # 表名
        return self.__add_rules(table, info)

    # 插入rules_xss表中的信息,返回是否插入成功，传入字典参数
    def add_rules_post(self, info):
        table = C.TABLENAME_RULES_POST  # 表名
        return self.__add_rules(table, info)

    # 删除rules_url表中的信息,返回是否插入成功，传入要删除的id
    def delete_rules_url(self, id):
        table = C.TABLENAME_RULES_URL
        return self.__delete_info(table, id)

    # 删除rules_sql表中的信息,返回是否插入成功，传入要删除的id
    def delete_rules_get(self, id):
        table = C.TABLENAME_RULES_GET
        return self.__delete_info(table, id)

    # 删除rules_url表中的信息,返回是否插入成功，传入要删除的id
    def delete_rules_post(self, id):
        table = C.TABLENAME_RULES_POST
        return self.__delete_info(table, id)

    # 查询WAF  PASS日志信息,查询数据类型为JSON
    def get_logs_waf_pass(self):
        table = C.TABLENAME_LOGS_WAF_PASS
        return self.__select_logs(table)

    # 查询WAF PASS日志信息，根据ip查询
    def get_logs_waf_pass_ip(self, ip):
        table = C.TABLENAME_LOGS_WAF_PASS
        return self.__select_logs_ip(table, ip)

    # 添加PASS日志信息,
    def add_logs_waf_pass(self, info):
        table = C.TABLENAME_LOGS_WAF_PASS
        return self.__add_logs(table, info)

    # 清空PASS日志信息
    def delete_logs_waf_pass(self):
        table = C.TABLENAME_LOGS_WAF_PASS
        return self.__delete_logs(table)

    # 查询WAF  拦截日志信息,查询数据类型为JSON
    def get_logs_waf_block(self):
        table = C.TABLENAME_LOGS_WAF_BLOCK
        return self.__select_logs(table)

    # 查询WAF PASS日志信息，根据ip查询
    def get_logs_waf_block_ip(self, ip):
        table = C.TABLENAME_LOGS_WAF_BLOCK
        return self.__select_logs_ip(table, ip)

    # 添加拦截日志信息,
    def add_logs_waf_block(self, info):
        table = C.TABLENAME_LOGS_WAF_BLOCK
        return self.__add_logs(table, info)

    # 清空拦截日志信息
    def delete_logs_waf_block(self):
        table = C.TABLENAME_LOGS_WAF_BLOCK
        return self.__delete_logs(table)

    # 查询WAF  error日志信息,查询数据类型为JSON
    def get_logs_waf_error(self):
        table = C.TBALENAME_LOGS_WAF_ERROR
        return self.__select_logs(table)

    # 添加error日志信息,
    def add_logs_waf_error(self, info):
        table = C.TBALENAME_LOGS_WAF_ERROR
        return self.__add_logs(table, info)

    # 清空error日志信息
    def delete_logs_waf_error(self):
        table = C.TBALENAME_LOGS_WAF_ERROR
        return self.__delete_logs(table)

    # 得到用户操作日志信息
    def get_logs_user_operate(self):
        table = C.TABLENAME_LOGS_USER_OPERATE
        return self.__select_logs(table)

    # 添加用户操作日志
    def add_logs_user_operate(self, info):
        table = C.TABLENAME_LOGS_USER_OPERATE
        return self.__add_logs(table, info)

    # 清空用户操作日志
    def delete_logs_user_operate(self):
        table = C.TABLENAME_LOGS_USER_OPERATE
        return self.__delete_logs(table)

    # 修改url规则状态
    def change_url_status(self, id, status):
        table = C.TABLENAME_RULES_URL
        return self.__change_rules_status(table, id, status)

    # 修改GET规则状态
    def change_get_status(self, id, status):
        table = C.TABLENAME_RULES_GET
        return self.__change_rules_status(table, id, status)

    # 修改POST规则状态
    def change_post_status(self, id, status):
        table = C.TABLENAME_RULES_POST
        return self.__change_rules_status(table, id, status)

    # 得到被封禁的ip信息
    def get_prohibit_ip(self):
        table = C.TABLENAME_IP_PROHIBIT
        return self.__select_rules(table)

    # 删除被封禁的ip信息
    def delete_prohibit_ip(self, id):
        table = C.TABLENAME_IP_PROHIBIT
        return self.__delete_info(table, id)

    # 添加被封禁的ip，相当于封禁
    def add_prohibit_ip(self, ip, date, status):
        table = C.TABLENAME_IP_PROHIBIT
        sql = '''
            INSERT INTO `{table}`(`ip`,`date`,`status`)VALUES('{ip}','{date}','{status}');
        '''.format(table=table, ip=ip, date=date, status=status)
        try:
            cursor = self.__execute(sql)
            self.__db.commit()
            return True
        except Exception as e:
            self.__db.rollback()  # 出错回滚
            log('sql执行错误----封禁ip插入失败', 2)
            print(e)
            return False

    # 修改IP封禁状态
    def change_prohibit_status(self, id, status):
        table = C.TABLENAME_IP_PROHIBIT
        return self.__change_rules_status(table, id, status)

    # 查询一段时间范围内的IP对某url的访问量
    def select_ip_times(self, ip, nowtime, recenttime, url):
        sql = '''SELECT count(info->"$.method") FROM `logs_waf_pass` WHERE info->"$.ip"="{ip}" AND info->"$.url"="{url}" AND info->"$.date" 
        >="{recenttime}" AND info->"$.date" <="{nowtime}" GROUP BY info->"$.method"'''.format(ip=ip, url=url, recenttime=recenttime, nowtime=nowtime)
        print(sql)
        try:
            cursor = self.__execute(sql)
            self.__db.commit()
            lists = []
            for temp in cursor.fetchall():
                dict = {'num': temp[0]}
                lists.append(dict)
            return lists
        except Exception as e:
            log('sql执行错误----一段时间内的ip访问量查询失败', 2)
            print(e)

if __name__ == '__main__':
    db = DataBase()
    timestr = datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S")  # 时间
    recent=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    a=db.select_ip_times('127.0.0.1',timestr,recent,'/login.php')
    lists=[]
    for item in a:
        print(item['num'])
        lists.append(item['num'])
    print(lists)
    print(max(lists))
