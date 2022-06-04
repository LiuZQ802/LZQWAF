# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Project :  Simple-WAF
@File    :  front_db
@Author  :  刘子琦
@Data    :  2022/4/29
@Description:
    前端数据库操作模块
"""

from WAF_Engine.waf_db import DataBase


# 继承waf_db
class front_db(DataBase):
    __db = ''

    def __init__(self):
        super().__init__()
        self.__db = super().get_db()

    #########获取信息##############
    # 获得正常通行日志
    def get_logs_waf_pass(self):
        return super().get_logs_waf_pass()

    # 获得拦截日志
    def get_logs_waf_block(self):
        return super().get_logs_waf_block()

    # 获得系统运行日志
    def get_logs_waf_error(self):
        return super().get_logs_waf_error()

    # 获得URL规则
    def get_rules_url(self):
        return super().get_rules_url()

    # 获得GET规则
    def get_rules_get(self):
        return super().get_rules_get()

    # 获得IP黑名单
    def get_prohibit_ip(self):
        return super().get_prohibit_ip()

    ############规则操作####################
    # 修改url规则状态
    def change_url_status(self, id, status):
        return super().change_url_status(id, status)

    # 修改get规则状态
    def change_get_status(self, id, status):
        return super().change_get_status(id, status)

    # 修改post规则状态
    def change_post_status(self, id, status):
        return super().change_post_status(id, status)

    # 修改IP黑名单状态
    def change_prohibit_status(self, id, status):
        return super().change_prohibit_status(id, status)

    # 删除url规则
    def delete_rules_url(self, id):
        return super().delete_rules_url(id)

    # 删除get规则
    def delete_rules_get(self, id):
        return super().delete_rules_get(id)

    # 删除post规则
    def delete_rules_post(self, id):
        return super().delete_rules_post(id)

    # 删除ip黑名单
    def delete_prohibit_ip(self, id):
        return super().delete_prohibit_ip(id)

    # 添加url规则
    def add_rules_url(self, info):
        return super().add_rules_url(info)

    # 添加get规则
    def add_rules_get(self, info):
        return super().add_rules_get(info)

    # 添加post规则
    def add_rules_post(self, info):
        return super().add_rules_post(info)

    # 添加IP黑名单
    def add_prohibit_ip(self, ip, date, status):
        return super().add_prohibit_ip(ip, date, status)

    #################统计分析######################
    # 按某个关键字统计
    def __static_key(self, key):
        sql = '''SELECT info->'$.{key}',count(info->'$.{key}')as num FROM `logs_waf_block`group 
                by(info->'$.{key}') order by num DESC'''.format(key=key)
        cursor = self.__db.cursor()
        cursor.execute(sql)
        self.__db.commit()
        lists = []
        for item in cursor.fetchall():
            dict = {key: item[0], 'count': item[1]}
            lists.append(dict)
        return lists

    # 统计攻击源排行
    def static_rank_ip(self):
        lists = self.__static_key('ip')
        for item in lists:
            a = item['ip'].replace('\"', '')
            item['ip'] = a
            info = super().get_logs_waf_block_ip(a)[0]['info']
            item['country'] = info['country']
            item['city'] = info['city']
        return lists

    # 统计攻击方式排行
    def static_rank_type(self):
        lists = self.__static_key('type')
        return lists

    # 统计URL
    def static_rank_url(self):
        sql = '''SELECT info->'$.url',info->'$.method',count(info->'$.url') as num FROM `logs_waf_block` GROUP BY 
        info->'$.url',info->'$.method' ORDER BY num DESC'''
        cursor = self.__db.cursor()
        cursor.execute(sql)
        self.__db.commit()
        lists1 = []
        for item in cursor.fetchall():
            dict = {'url': item[0], 'method': item[1], 'count': item[2]}
            lists1.append(dict)

        sql = '''SELECT info->'$.url',info->'$.method',count(info->'$.url') as num FROM `logs_waf_pass` GROUP BY 
                info->'$.url',info->'$.method' ORDER BY num DESC'''
        cursor = self.__db.cursor()
        cursor.execute(sql)
        self.__db.commit()
        lists2 = []
        for item in cursor.fetchall():
            dict = {'url': item[0], 'method': item[1], 'count': item[2]}
            lists2.append(dict)
        lists = []
        for item1 in lists1:
            flag = True
            for item2 in lists2:
                if item1['url'] == item2['url'] and item1['method'] == item2['method']:
                    item1['count'] += item2['count']
                    lists.append(item1)
                    lists2.remove(item2)
                    flag = False
                    break
            if flag:
                lists.append(item1)
        for item in lists2:
            lists.append(item)
        lists = sorted(lists, key=lambda k: k['count'], reverse=True)
        return lists

    # 统计URL总ip个数
    def static_rank_url_ip(self, url, method):
        sql = '''SELECT info->'$.ip' FROM `logs_waf_block` WHERE 
        info->'$.url'="{url}" and info->'$.method'="{method}"; '''.format(url=url, method=method)
        cursor = self.__db.cursor()
        cursor.execute(sql)
        self.__db.commit()
        lists1 = []
        for item in cursor.fetchall():
            lists1.append(item[0])

        sql = '''SELECT info->'$.ip' FROM `logs_waf_pass` WHERE 
                info->'$.url'="{url}" and info->'$.method'="{method}"; '''.format(url=url, method=method)
        cursor = self.__db.cursor()
        cursor.execute(sql)
        self.__db.commit()
        lists2 = []
        for item in cursor.fetchall():
            lists2.append(item[0])
        lists1 += lists2
        ip_set = set(lists1)
        return len(ip_set)

    ###############日志操作######################
    # 清空PASS日志
    def delete_logs_waf_pass(self):
        return super().delete_logs_waf_pass()

    # 清空block日志
    def delete_logs_waf_block(self):
        return super().delete_logs_waf_block()

    # 清空程序错误日志
    def delete_logs_waf_error(self):
        return super().delete_logs_waf_error()

    # 清空用户操作日志
    def delete_logs_user_operate(self):
        return super().delete_logs_user_operate()

    # 添加用户操作日志
    def add_logs_user_operate(self, info):
        return super().add_logs_user_operate(info)


if __name__ == '__main__':
    a = front_db()
    b = a.static_rank_url()
    a.static_rank_url_ip('/login.php', 'GET')
    print(b)
