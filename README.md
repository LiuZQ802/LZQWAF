# WEB应用防火墙

## WAF核心引擎函数模块

### main

- main()  

    调用入口

- handle_response(client_socket) 

    接受客户端请求，并传入filter中进行过滤判别，然后传入response里接受真实服务器请求

### config

配置模块

- 调剂级别及部署方式状态
- 动作状态码
- socket配置
- 代理服务器及真实服务器地址和端口
- 数据库信息
- 请求处理正则

### set_config

防火墙配置信息的操作

- write_conf()

    初始化操作

-  get_waf_status()

    获得防火墙状态

- set_waf_status(status)

    设置防火墙状态，注意传参必须是字符串

- get_real_host()

    获得内容服务器的ip

- set_real_host(host)

    设置内容服务器ip

- get_real_port()

    获得内容服务器端口

- set_real_port(port)

    设置内容服务器端口

- get_proxy_host()

    获得代理服务器ip,即防火墙所部署的防火墙ip

- set_proxy_host(host)

    设置防火墙代理服务器ip

- get_proxy_port()

    获得防火墙代理服务器端口

- set_proxy_port(port)

    设置防火墙代理服务器端口

- get_service_name()

    获得服务器名称，指HTTP或HTTPS

- set_service_name(name)

    设置服务器名称

- get_database_ip()

    获得防火墙数据库的ip

- ser_database_ip(ip)

    设置防火墙数据库的ip

- get_database_login_info()

    获得防火墙数据库的登录用户名密码，返回以列表形式

- set_databse_login_info(user,passwd)

    设置防火墙数据库的登录用户名密码

- get_database_name()

    获得防火墙数据库库名

- set_database_name(name)

    设置防火墙数据库的库名

- get_cc_minutes()

    获得cc攻击判断时间的范围，即获取几分钟内

- set_cc_minutes(minutes)

    设置分钟

- get_cc_times()

    获取cc攻击判断时最大请求数

- set_cc_times(times)

    设置最大请求数，必须传字符串

### filer

过滤模块

- do_filter(client_socket,client_req)

    filter模块对外调用函数

- get_message(client_socket,client_req)

    过滤请求信息，返回关键信息json
    
- is_pass(regular,message)

    传入正则表达式regular和数据message

    判断数据是否匹配正则表达式，匹配则代表有非法信息，那么返回False，反之返回True

- is_prohibit(ip，message):

    传入ip，判断该ip是否被禁止访问

- do_url(message,url)

    传入信息，和url，判断是否有敏感目录文件等

- do_get(message,url)

    判断get请求是否有非法信息
    
- do_post(message,body)

    处理post请求中的post信息，有几个分支，一个处理登录情况，一个处理xss，一个处理命令执行

- do_post_login(message,data,path) 

    对post类型的sql注入进行拦截判断

- do_post_xss(message,data,path)

    对post类型的xss进行判断拦截   存储型XSS

- do_post_type(message,data,path)

    对文件上传时的文件类型进行白名单匹配

- do_post_type_suffix(message,data,path)

    对文件上传时的文件后缀进行黑名单匹配
    
- do_post_exe(message,data,path)

    命令执行特殊字符或敏感字符过滤

- is_illegal_ask(message,minutes,times)

    判断是否多次非法请求，minutes表示判断多长时间内的，以分钟为单位；times表示最大请求次数

    
    
    

### response

根据动作选择是否向真实服务器发送请求，并获取真实服务器请求转发给客户

- do_response(client_socket,proxy_req,action)

    response模块对外主要调用函数，跟据action选择放行拦截还是其他

- response_pass(client_socket,client_req)

    放行动作，向真实服务器发送请求，并获取真实服务器response再转发给客户

- response_block(client_socket,message)

    拦截动作，丢弃用户请求，返回拦截警告
    
- response_prohibit(client_socket,message)

    禁止访问，丢弃用户请求，返回禁止访问警告

### waf_db

数据库操作模块

类DataBase

init  连接数据库

del  关闭数据库

get_db()  连接数据库

execute(sql)   执行sql语句，返回cursor

select_rules(table)  传入表名，查询规则数据，返回数据，字典形式

select_logs（table）传入表名,查询日志数据，返回字典形式

add_rules(table,info)传入表明，数据字典，插入规则信息

add_logs(table,info)，传入表明，日志信息(json形式)插入日志

delete_info(table,id)，传入表名，id，删除 表中信息，

get_rules_url()  查询url规则

get_rules_get()  查询get规则

get_rules_post()   查询post规则

add_rules_url(info) 插入url规则，字典形式

add_rules_get(info)插入get规则，字典形式

add_rules_post(info)插入post规则，字典形式

delete_rules_url(id) 根据id删除url规则

delete_rules_get(id)根据id删除get规则

delete_rules_post(id)根据id删除post规则

get_logs_waf()获得防火墙日志信息，返回字典

add_logs_waf(info)传入日志信息，字典形式,插入

delete_logs_waf(id)根据id删除日志信息

get_prohibit_ip() 得到被删除的ip信息

delete_prohibit_ip(id)根据id删除被封禁的ip信息，相当于解封

add_prohibit_ip(ip,date） 添加被封禁的ip信息，相当于封禁,传进去ip和被封时间

change_prohibit_status(id,status)  修改ip封禁的状态



### load_rules

加载规则模块

- load_rules()

    把数据库中的规则加载到本地，总对外调用函数

- write_files(name,data)

    写文件操作，文件地址是name，要写入数据是data

- load_rules_url(db,path)

    加载数据库中url规则数据到本地文件中，db指数据库句柄，path，文件地址

- load_rules_get(db,path)

    加载数据库中get规则数据到本地文件中，db指数据库句柄，path，文件地址

- load_rules_post(db,path)

    加载数据库中post规则数据到本地文件中，db指数据库句柄，path，文件地址
    
- load_prohibit_ip(db,path)

    加载数据库中被封禁的ip信息到本地，db指数据库句柄，path，文件地址



### utils

插件小工具模块

- log(message,level=0)

    颜色输出，根据level级别选择输出类型

- ip_info(ip)

    通过调用API接口，获取相应IP地址的回应状态 国家 省 市 是否使用代理  ip等信息

    返回字典
    
- change_to_json(data)

    将数据dic转换成json，返回json数据

- change_to_dict(data)

    将json转换成字典，返回字典

### logs

记录日志信息

- ip_is_database(ip)

    判断传进来的ip是否在数据库日志中有记录

- add_pass_logs(message)

    添加正常放行日志

- add_block_logs(message,action,type,s)

    添加拦截日志

    message指传过来的ip、地址、时间、端口等基本信息

    action表示描述信息

    type表示非法请求的行为类别

    s表示注入点的注入信息，即非法信息

- add_error_logs(error,exception)

    添加程序运行过程中的错误日志

    error表示错误描述

    exception表示异常信息



## 前端页面设计

### main

flask主函数

- page_404(e)

    404界面

- index()

    主页面

- logs_pass()

    返回放行日志的html页面及放行日志

- logs_block()

    返回拦截日志的html页面及拦截日志

- logs_error()

    返回程序运行错误日志的html页面及错误日志

- url_rules_manage()

    返回url规则html页面

- get_rules_manage()

    返回get规则的html页面

- post_rules_manage()

    返回post规则的html页面

- tansfer_url_data()

    POST  返回url规则数据

- transfer_get_data()

    POST  返回get规则数据

- transfer_post_data()

    POST 返回post规则数据

- change_status_url()

    修改url规则状态：开还是关  POST传输

- change_status_get()

    修get规则状态：开还是关  POST传输

- change_status_post()

    修改post规则状态：开还是关  POST传输

- remove_rules_url()

    删除url规则  POST传输

- remove_rules_get()

    删除get规则  POST传输

- remove_rules_post()

    删除post规则  POST传输

- add_rules_url()

    添加url规则，POST传输

- add_rules_get()

    添加get规则，POST传输

- add_rules_post()

    添加post规则，POST传输

- rules_delete()

    清空日志，根据前端ajax传过来的数据绝对删除哪个日志，返回是否删除成功

- rank_attack()

    攻击源排行，返回html页面及数据

- rank_type()

    攻击方式排行，返回html页面及数据

- static_type()

    攻击方式统计，配合前端生成可视化表格，POST返回数据

- rank_url()

    url排行榜，返回html页面及数据

- IP_power()

    统计一周内ip访问量，配合前端生成可视化，POST传输数据

- intercept_page()

    返回拦截页面，配合WAF请求此拦截页面

### front_db

前端需要操作的数据库，继承waf里面的waf_db

- init()

    继承waf_db,并且获得数据库句柄

- static_key(key)

    通过传进来的关键字按关键字的统计数排行输出

    还有其他一些函数与waf_db类似

    

## 数据库表设计

创建MySQL数据库，创建一系列数据表

### rules_url

url规则

表结构是

id   regular description  status



id:唯一表示方式

regular:正则表达式

description:描述

status:状态。表示是否使用该正则

### rules_get

get请求黑名单

表结构是

id  regular description status



id:唯一表示方式

regular:正则表达式

description:描述

status:状态。表示是否使用该正则



### rules_post

post请求黑名单

id regular description status



id:唯一表示方式

regular:正则表达式

description:描述

status:状态。表示是否使用该正则



### logs_waf_pass

日志信息,通过日志

id   info 

info包含以下键值    date   ip  port site proxy  method  url   isAttack  action



id:唯一标识符

info: 存储日志信息   JSON类型





date：时间   YYYY-MM-DD HH：MM：SS

ip：访问ip

port：访问端口

country:国家

city：省份城市

proxy:是否使用代理

method：访问方法

url : 访问路径，URL地址



### logs_waf_block

防火墙拦截日志

id   info 

info包含以下键值    date   ip  port site proxy  method  url   isAttack  action



id:唯一标识符

info: 存储日志信息   JSON类型





date：时间   YYYY-MM-DD HH：MM：SS

ip：访问ip

port：访问端口

country:国家

city：省份城市

proxy:是否使用代理

method：访问方法

url : 访问路径，URL地址

action:攻击的方式(description)



### logs_waf_error

防火墙出错日志

id   info 

info包含以下键值    date   error exception



id:唯一标识符

info: 存储日志信息   JSON类型





date：时间   YYYY-MM-DD HH：MM：SS

error:错误信息

exception 异常信息

### logs_user_operate

用户操作日志

记录着用户在管理面板的一些操作，包括添加删除修改规则、ip黑名单，删除日志等操作

id info

info 包含以下键值 date behave object operate

id:唯一标识符

info:存储的日志信息



date:时间   YYYY-MM-DD HH：MM：SS

behave 行为，包括 删除、添加、修改

object 操作对象：例如URL规则库、IP黑名单等等

operate 操作:以下为操作信息及描述



### prohibit_ip

封禁的ip表

id  ip date status

id:唯一标识符

ip:被封的ip

date：被封的时间

status 状态

