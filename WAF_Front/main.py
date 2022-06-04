# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Project :  Simple-WAF
@File    :  main
@Author  :  刘子琦
@Data    :  2022/4/29
@Description:
    前端运行入口
"""
import datetime
import pytz  # 时区
import re
from flask import Flask, render_template, request, jsonify
from WAF_Front.front_db import front_db
from WAF_Front.analysis import ip_analyse
from WAF_Engine.load_rules import load_rules
import WAF_Engine.set_config as conf
from WAF_Engine.main import main as start
import WAF_Engine.config as C

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

'''
404界面
'''


@app.errorhandler(404)
def page_404(e):
    return render_template('404.html')


'''
主页面
'''


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


'''
放行日志
'''


@app.route('/logs/pass')
def logs_pass():
    db = front_db()
    lists = db.get_logs_waf_pass()
    transfer_lists = []
    i = 1
    for item in lists:
        info = item['info']
        if not info['country'] and info['city']:
            site = info['country'] + info['city']
        elif not info['country']:
            site = info['country']
        elif not info['city']:
            site = info['city']
        else:
            site = ''
        del (info['country'])
        del (info['city'])
        info['site'] = site
        info['id'] = i
        transfer_lists.append(info)
        i += 1
    return render_template('logs_pass.html', lists=transfer_lists)


'''
拦截日志
'''


@app.route('/logs/block')
def logs_block():
    db = front_db()
    lists = db.get_logs_waf_block()
    transfer_lists = []
    i = 1
    for item in lists:
        info = item['info']
        if not info['country'] and info['city']:
            site = info['country'] + info['city']
        elif not info['country']:
            site = info['country']
        elif not info['city']:
            site = info['city']
        else:
            site = ''
        del (info['country'])
        del (info['city'])
        info['site'] = site
        info['id'] = i
        transfer_lists.append(info)
        i += 1
    return render_template('logs_block.html', lists=transfer_lists)


'''
程序运行错误日志
'''


@app.route('/logs/error')
def logs_error():
    db = front_db()
    lists = db.get_logs_waf_error()
    transfer_lists = []
    i = 1
    for item in lists:
        info = item['info']
        info['id'] = i
        transfer_lists.append(info)
        i += 1
    return render_template('logs_error.html', lists=transfer_lists)


'''
用户操作日志
'''


@app.route('/logs/user_operate')
def logs_user_operate():
    db = front_db()
    lists = db.get_logs_user_operate()
    transfer_lists = []
    i = 1
    for item in lists:
        info = item['info']
        info['id'] = i
        transfer_lists.append(info)
        i += 1
    return render_template('logs_user_operate.html', lists=transfer_lists)


'''
URL规则管理
'''


@app.route('/url_rules_manage')
def url_rules_manage():
    return render_template('url_rules_manage.html')


'''
GET规则管理
'''


@app.route('/get_rules_manage')
def get_rules_manage():
    db = front_db()
    lists = db.get_rules_get()
    return render_template('get_rules_manage.html', lists=lists)


'''
POST规则管理
'''


@app.route('/post_rules_manage')
def post_rules_manage():
    return render_template('post_rules_manage.html')


'''
IP封禁管理
'''


@app.route('/ip_prohibit')
def ip_prohibit():
    return render_template('ip_prohibit.html')


'''
传url_rules数据
'''


@app.route('/url_data', methods=['POST'])
def transfer_url_data():
    if request.method == 'POST':
        db = front_db()
        lists = db.get_rules_url()
        return jsonify(lists)


'''
传get_rules数据
'''


@app.route('/get_data', methods=['post'])
def transfer_get_data():
    if request.method == 'POST':
        db = front_db()
        lists = db.get_rules_get()
        return jsonify(lists)


'''
传post_rules数据
'''


@app.route('/post_data', methods=['POST'])
def transfer_post_data():
    if request.method == 'POST':
        db = front_db()
        lists = db.get_rules_post()
        return jsonify(lists)


'''
传IP黑名单
'''


@app.route('/ip_data', methods=['POST'])
def transfer_ip_data():
    if request.method == 'POST':
        db = front_db()
        lists = db.get_prohibit_ip()
        return jsonify(lists)


'''
修改url规则状态
'''


@app.route('/url_rules_manage/change_status_url', methods=['POST'])
def change_status_url():
    if request.method == 'POST':
        db = front_db()
        values = request.values.values()  # 值传过来，获得生成器
        id = next(values)
        status = next(values)
        flag = db.change_url_status(id, status)
        # 如果修改成功，则加载到本地
        if flag:
            load_rules(C.LOAD_URL)
            info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                    'behave': '修改', 'object': 'URL规则库', 'operate': '修改某个URL规则状态为:' + status}
            db.add_logs_user_operate(info)
        return jsonify({'flag': flag, 'status': status, 'id': id})  # 返回给前端数据


'''
修改get规则状态
'''


@app.route('/get_rules_manage/change_status_get', methods=['POST'])
def change_status_get():
    if request.method == 'POST':
        db = front_db()
        values = request.values.values()  # 值传过来，获得生成器
        id = next(values)
        status = next(values)
        flag = db.change_get_status(id, status)
        # 如果修改成功，则加载到本地
        if flag:
            load_rules(C.LOAD_GET)
            info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                    'behave': '修改', 'object': 'GET规则库', 'operate': '修改某个GET规则状态为:' + status}
            db.add_logs_user_operate(info)
        return jsonify({'flag': flag, 'status': status, 'id': id})  # 返回给前端数据


'''
修改post规则状态
'''


@app.route('/post_rules_manage/change_status_post', methods=['POST'])
def change_status_post():
    if request.method == 'POST':
        db = front_db()
        values = request.values.values()  # 值传过来，获得生成器
        id = next(values)
        status = next(values)
        flag = db.change_post_status(id, status)
        # 如果修改成功，则加载到本地
        if flag:
            load_rules(C.LOAD_POST)
            info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                    'behave': '修改', 'object': 'POST规则库', 'operate': '修改某个POST规则状态为:' + status}
            db.add_logs_user_operate(info)
        return jsonify({'flag': flag, 'status': status, 'id': id})  # 返回给前端数据


'''
修改ip黑名单状态
'''


@app.route('/ip_prohibit_manage/change_status_ip', methods=['POST'])
def change_status_ip():
    if request.method == 'POST':
        db = front_db()
        values = request.values.values()  # 接受传过来的值
        id = next(values)
        status = next(values)
        flag = db.change_prohibit_status(id, status)  # 修改状态
        # 如果修改成功，则加载到本地
        if flag:
            load_rules(C.LOAD_PROHIBIT)
            info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                    'behave': '修改', 'object': 'IP黑名单', 'operate': '修改某个IP黑名单状态为:' + status}
            db.add_logs_user_operate(info)
        return jsonify({'flag': flag, 'status': status, 'id': id})


'''
删除url规则
'''


@app.route('/url_rules_manage/remove_rules_url', methods=['POST'])
def remove_rules_url():
    if request.method == 'POST':
        db = front_db()
        values = request.values.values()
        id = next(values)
        flag = db.delete_rules_url(id)  # 根据id删除规则
        # 如果删除成功，则加载到本地
        if flag:
            load_rules(C.LOAD_URL)
            info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                    'behave': '删除', 'object': 'URL规则库', 'operate': '删除一条URL规则'}
            db.add_logs_user_operate(info)
        return jsonify({'flag': flag, 'id': id})


'''
删除get规则
'''


@app.route('/get_rules_manage/remove_rules_get', methods=['POST'])
def remove_rules_get():
    if request.method == 'POST':
        db = front_db()
        values = request.values.values()
        id = next(values)
        flag = db.delete_rules_get(id)  # 根据id删除规则
        # 如果删除成功，则加载到本地
        if flag:
            load_rules(C.LOAD_GET)
            info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                    'behave': '删除', 'object': 'GET规则库', 'operate': '删除一条GET规则'}
            db.add_logs_user_operate(info)
        return jsonify({'flag': flag, 'id': id})


'''
删除post规则
'''


@app.route('/post_rules_manage/remove_rules_post', methods=['POST'])
def remove_rules_post():
    if request.method == 'POST':
        db = front_db()
        values = request.values.values()
        id = next(values)
        flag = db.delete_rules_post(id)  # 根据id删除规则
        # 如果删除成功，则加载到本地
        if flag:
            load_rules(C.LOAD_POST)
            info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                    'behave': '删除', 'object': 'POST规则库', 'operate': '删除一条POST规则'}
            db.add_logs_user_operate(info)
        return jsonify({'flag': flag, 'id': id})


'''
删除IP黑名单
'''


@app.route('/ip_prohibit_manage/remove_ip', methods=['POST'])
def remove_ip():
    if request.method == 'POST':
        db = front_db()
        values = request.values.values()
        id = next(values)
        flag = db.delete_prohibit_ip(id)  # 删除ip黑名单
        # 如果删除成功，则加载到本地
        if flag:
            load_rules(C.LOAD_PROHIBIT)
            info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                    'behave': '删除', 'object': 'IP黑名单', 'operate': '删除一个IP黑名单'}
            db.add_logs_user_operate(info)
        return jsonify({'flag': flag, 'id': id})


'''
添加url规则
'''


@app.route('/url_rules_manage/add_rules_url', methods=['POST'])
def add_rules_url():
    if request.method == 'POST':
        db = front_db()
        info = {}
        values = request.values.values()
        info['regular'] = next(values)
        info['type'] = next(values)
        info['description'] = next(values)
        status = re.search(C.RE_STATUS, next(values))  # 正则匹配
        if status:
            info['status'] = status.group()
        else:
            info['status'] = 'off'  # 默认为off

        flag = db.add_rules_url(info)
        # 如果添加成功，则加载到本地
        if flag:
            load_rules(C.LOAD_URL)
            message = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                       'behave': '添加', 'object': 'URL规则库', 'operate': '新增一条URL规则:' + info['regular']}
            db.add_logs_user_operate(message)
        return jsonify({'flag': flag})


'''
添加get规则
'''


@app.route('/get_rules_manage/add_rules_get', methods=['POST'])
def add_rules_get():
    if request.method == 'POST':
        db = front_db()
        info = {}
        values = request.values.values()
        info['regular'] = next(values)
        info['type'] = next(values)
        info['description'] = next(values)
        status = re.search(C.RE_STATUS, next(values))  # 正则匹配
        if status:
            info['status'] = status.group()
        else:
            info['status'] = 'off'  # 默认为off
        flag = db.add_rules_get(info)
        # 如果添加成功，则加载到本地
        if flag:
            load_rules(C.LOAD_GET)
            message = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                       'behave': '添加', 'object': 'GTE规则库', 'operate': '新增一条GET规则:' + info['regular']}
            db.add_logs_user_operate(message)
        return jsonify({'flag': flag})


'''
添加post规则
'''


@app.route('/post_rules_manage/add_rules_post', methods=['POST'])
def add_rules_post():
    if request.method == 'POST':
        db = front_db()
        info = {}
        values = request.values.values()
        info['regular'] = next(values)
        info['type'] = next(values)
        info['description'] = next(values)
        status = re.search(C.RE_STATUS, next(values))  # 正则匹配
        if status:
            info['status'] = status.group()
        else:
            info['status'] = 'off'  # 默认为off
        flag = db.add_rules_post(info)
        # 如果添加成功，则加载到本地
        if flag:
            load_rules(C.LOAD_POST)
            message = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                       'behave': '添加', 'object': 'POST规则库', 'operate': '新增一条POST规则:' + info['regular']}
            db.add_logs_user_operate(message)
        return jsonify({'flag': flag})


'''
添加ip黑名单
'''


@app.route('/ip_prohibit_manage/add_ip', methods=['POST'])
def add_ip():
    if request.method == 'POST':
        db = front_db()
        values = request.values.values()
        ip = re.search(C.RE_IP, next(values))
        status = re.search(C.RE_STATUS, next(values))
        if ip:
            ip = ip.group()
            date = datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S")  # 时间
            if status:
                status = status.group()
            else:
                status = 'off'  # 若无输入或错误输入状态，状态默认为off
            flag = db.add_prohibit_ip(ip, date, status)
        else:
            flag = False  # ip输入不符合规矩，则添加失败
            # 如果添加成功，则加载到本地
        if flag:
            load_rules(C.LOAD_PROHIBIT)
            info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                    'behave': '添加', 'object': 'IP黑名单', 'operate': '新增IP黑名单'}
            db.add_logs_user_operate(info)
        return jsonify({'flag': flag})


'''
清空日志
'''


@app.route('/rules_manage/delete', methods=['POST'])
def rules_delete():
    if request.method == 'POST':
        db = front_db()
        values = request.values.values()
        name = next(values)
        if name == 'logs_waf_pass':
            flag = db.delete_logs_waf_pass()
            # 删除成功，则将本次删除操作记录在用户操作日志里
            if flag:
                info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                        'behave': '删除', 'object': '正常放行', 'operate': '清空正常放行日志'}
                db.add_logs_user_operate(info)
        elif name == 'logs_waf_block':
            flag = db.delete_logs_waf_block()
            # 删除成功，则将本次删除操作记录在用户操作日志里
            if flag:
                info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                        'behave': '删除', 'object': '拦截日志', 'operate': '清空拦截日志'}
                db.add_logs_user_operate(info)
        elif name == 'logs_waf_error':
            flag = db.delete_logs_waf_error()
            # 删除成功，则将本次删除操作记录在用户操作日志里
            if flag:
                info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                        'behave': '删除', 'object': '运行', 'operate': '清空WAF运行错误日志'}
                db.add_logs_user_operate(info)
        elif name == 'logs_user_operate':
            flag = db.delete_logs_user_operate()
            # 删除成功，则将本次删除操作记录在用户操作日志里
            if flag:
                info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                        'behave': '删除', 'object': '用户操作日志', 'operate': '清空用户操作日志'}
                db.add_logs_user_operate(info)
        else:
            flag = False
        return jsonify({'flag': flag})


'''
攻击源排行
'''


@app.route('/rank/attack')
def rank_attack():
    db = front_db()
    lists = db.static_rank_ip()
    # 聚合国家城市信息
    site = ''
    i = 1
    for item in lists:
        if item['country'] and item['city']:
            site = item['country'] + item['city']
        elif item['country']:
            site = item['country']
        elif item['city']:
            site = item['city']
        del (item['country'])
        del (item['city'])
        item['site'] = site
        item['id'] = i
        i += 1
    lists_ten = []
    if len(lists) > 10:
        for i in range(10):
            lists_ten.append(lists[i])
    else:
        lists_ten = lists
    return render_template('rank_attack.html', lists=lists_ten)


'''
攻击方式排行
'''


@app.route('/rank/type')
def rank_type():
    db = front_db()
    lists = db.static_rank_type()
    id = 1
    for item in lists:
        item['id'] = id
        id += 1
        item['type'] = item['type'].replace('\"', '')
    return render_template('rank_type.html', lists=lists)


'''
攻击方式统计
'''


@app.route('/static/type', methods=['POST'])
def static_type():
    if request.method == 'POST':
        db = front_db()
        lists = db.static_rank_type()
        for item in lists:
            item['type'] = item['type'].replace('\"', '')
        return jsonify(lists)


'''
URL排行
'''


@app.route('/rank/url')
def rank_url():
    db = front_db()
    lists = db.static_rank_url()
    id = 1
    lists_ten = []
    for item in lists:
        item['id'] = id
        id += 1
        item['url'] = item['url'].replace('\"', '')
        item['method'] = item['method'].replace('\"', '')
        lists_ten.append(item)
        if id > 10:
            break
    for item in lists_ten:
        ip_count = db.static_rank_url_ip(item['url'], item['method'])
        item['ip_count'] = ip_count
    return render_template('rank_url.html', lists=lists_ten)


'''
一周内IP访问流量统计
'''


@app.route('/IP/power', methods=['POST'])
def IP_power():
    if request.method == 'POST':
        info = ip_analyse()
        return jsonify(info)


'''
返回WAF系统初始化状态
'''


@app.route('/init_status', methods=['POST'])
def init_status():
    if request.method == 'POST':
        WAF_Status = conf.get_waf_status()
        return jsonify({'status': WAF_Status})


'''
控制系统运行
'''


@app.route('/run', methods=['POST'])
def control_run():
    if request.method == 'POST':
        db = front_db()
        values = request.values.values()
        status = next(values)
        if status == 'true':
            conf.set_waf_status('True')  # 防火墙开
            info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                    'behave': '开启', 'object': 'WAF', 'operate': '开启防火墙'}
            db.add_logs_user_operate(info)
            flag = True
        else:
            conf.set_waf_status('False')  # 防火墙关
            info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                    'behave': '关闭', 'object': 'WAF', 'operate': '关闭防火墙'}
            db.add_logs_user_operate(info)
            flag = False
        return jsonify({'flag': flag})


'''
服务器设置
'''


@app.route('/service_set')
def service_set():
    return render_template('service_set.html')


'''
传参
传服务器数据
'''


@app.route('/service_data', methods=['POST'])
def transfer_service_data():
    if request.method == 'POST':
        data = {'id': 1, 'name': conf.get_service_name(), 'ip': conf.get_real_host(), 'real_port': conf.get_real_port(),
                'proxy_port': conf.get_proxy_port()}
        lists = []
        lists.append(data)
        return jsonify(lists)


'''
修改服务器参数
'''


@app.route('/set_service_data', methods=['POST'])
def set_service_data():
    if request.method == 'POST':
        db = front_db()
        flag = False
        values = request.values.values()
        name = next(values)
        proxy_port = next(values)
        real_ip = next(values)
        real_port = next(values)
        if name:
            flag = conf.set_service_name(name)
            if flag:
                info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                        'behave': '修改', 'object': '服务器参数', 'operate': '修改了服务名称为' + name}
                db.add_logs_user_operate(info)
        if proxy_port:
            flag = conf.set_proxy_port(proxy_port)
            if flag:
                info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                        'behave': '修改', 'object': '服务器参数', 'operate': '修改了代理服务器端口为' + proxy_port}
                db.add_logs_user_operate(info)
        if real_ip:
            flag = conf.set_real_host(real_ip)
            if flag:
                info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                        'behave': '修改', 'object': '服务器参数', 'operate': '修改了真实WEB服务器IP为' + real_ip}
                db.add_logs_user_operate(info)
        if real_port:
            flag = conf.set_real_port(real_port)
            if flag:
                info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                        'behave': '修改', 'object': '服务器参数', 'operate': '修改了真实WEB服务器端口为' + real_port}
                db.add_logs_user_operate(info)
        return jsonify({'flag': flag})


'''
数据库设置
'''


@app.route('/database_set')
def database_set():
    return render_template('database_set.html')


'''
数据库信息传输到前端
'''


@app.route('/database_data', methods=['POST'])
def transfer_database_data():
    if request.method == 'POST':
        data = {'id': 1, 'database_host': conf.get_database_ip(), 'database_user': conf.get_database_login_info()[0],
                'database_passwd': conf.get_database_login_info()[1],
                'database_name': conf.get_database_name()}
        lists = []
        lists.append(data)
        return jsonify(lists)


'''
修改数据库参数
'''


@app.route('/set_database_data', methods=['POST'])
def set_database_data():
    if request.method == 'POST':
        db = front_db()
        flag = False
        values = request.values.values()
        database_host = next(values)
        database_user = next(values)
        database_passwd = next(values)
        database_name = next(values)
        if database_host:
            flag = conf.set_database_ip(database_host)
        if database_user and database_passwd:
            flag = conf.set_database_login_info(database_user, database_passwd)
        if database_name:
            flag = conf.set_database_name(database_name)
        return jsonify({'flag': flag})


'''
非法多次请求参数设置
'''


@app.route('/illegal_ask_set')
def illegal_ask_set():
    return render_template('illegal_ask_set.html')


'''
传参
CC参数传到前端
'''


@app.route('/illegal_ask_data', methods=['POST'])
def illegal_ask_data():
    if request.method == 'POST':
        data = {'id':1,'minutes': conf.get_cc_minutes(), 'times': conf.get_cc_times()}

        lists = []
        lists.append(data)
        return jsonify(lists)

'''
CC参数设置
'''
@app.route('/set_illegal_ask_data',methods=['POST'])
def set_CC_data():
    if request.method=='POST':
        flag=False
        db=front_db()
        values=request.values.values()
        minutes=next(values)
        times=next(values)
        if minutes:
            flag=conf.set_cc_minutes(minutes)
            if flag:
                info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                        'behave': '修改', 'object': 'CC参数', 'operate': '修改了判断时间为' + minutes+'内'}
                db.add_logs_user_operate(info)
        if times:
            flag=conf.set_cc_times(times)
            if flag:
                info = {'date': datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S"),
                        'behave': '修改', 'object': 'CC参数', 'operate': '修改了最大请求次数为' + times+'次'}
                db.add_logs_user_operate(info)
        return jsonify({'flag':flag})
'''
拦截页面
'''


@app.route('/intercept_page')
def intercept_page():
    return render_template('intercept_page.html')


'''
封禁页面
'''


@app.route('/prohibit_page')
def prohibit_page():
    return render_template('prohibit_page.html')


if __name__ == '__main__':
    app.run(port=677, debug=True)
