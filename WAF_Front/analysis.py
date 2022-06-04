# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Project :  Simple-WAF
@File    :  analysis
@Author  :  刘子琦
@Data    :  2022/5/2
@Description:
    统计分析
"""
from front_db import front_db
from datetime import datetime, date, timedelta

'''
获取最近一周 日期

'''


def getDate():
    today = date.today().strftime("%m-%d")
    date_lists = [today]
    for item in range(1, 7):
        day = (date.today() - timedelta(days=item)).strftime('%m-%d')
        date_lists.append(day)
    date_lists.reverse()
    return date_lists


'''
一周内ip统计
'''


def ip_analyse():
    date = getDate()
    db = front_db()
    lists_pass = []
    lists_block=[]
    pass_logs = db.get_logs_waf_pass()
    block_logs = db.get_logs_waf_block()
    dicts = {
        date[0]: 0,
        date[1]: 0,
        date[2]: 0,
        date[3]: 0,
        date[4]: 0,
        date[5]: 0,
        date[6]: 0
    }
    dicts2={
        date[0]: 0,
        date[1]: 0,
        date[2]: 0,
        date[3]: 0,
        date[4]: 0,
        date[5]: 0,
        date[6]: 0
    }
    for item in pass_logs:
        lists_pass.append(item['info']['date'])
    for item in block_logs:
        lists_block.append(item['info']['date'])
    for item in date:
        for v in lists_pass:
            if item in v:
                dicts[item] = dicts[item] + 1
        for v in lists_block:
            if item in v:
                dicts2[item]=dicts2[item]+1
    return {'date':date,'pass_num':dicts,'block_num':dicts2}


if __name__ == '__main__':
    a=ip_analyse()
    # a = getDate()
    print(a)
