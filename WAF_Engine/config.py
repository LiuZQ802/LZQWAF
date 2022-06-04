# 配置文件

# 调试级别
# -1 自闭 不输出任何信息
# 0 包括白色正常信息全都输出
# 1 输出1级绿色debug及以上信息
# 2 只输出2级红色warning信息
DEBUG_LEVEL = 0


################################################################
# 一些常量

# 动作状态码
ACTION_BLOCK = 'BLOCK'  # 拦截
ACTION_PASS = 'PASS'  # 放行
ACTION_PROHIBIT = 'PROHIBIT'  # 封禁

#################################################################

# socket配置
# 客户请求的超时时间

CLIENT_SOCKET_TIMEOUT = 10

#################################################################

##################################################################
# 数据库   规则表名
TABLENAME_RULES_URL = 'rules_url'  # url黑名单
TABLENAME_RULES_GET = 'rules_get'  # sql黑名单
TABLENAME_RULES_POST = 'rules_post'  # xss黑名单
TABLENAME_LOGS_WAF_PASS = 'logs_waf_pass'  # 防火墙PASS日志
TABLENAME_LOGS_WAF_BLOCK = 'logs_waf_block'  # 防火墙拦截日志
TBALENAME_LOGS_WAF_ERROR = 'logs_waf_error'  # 防火墙出错日志，异常信息
TABLENAME_LOGS_USER_OPERATE = 'logs_user_operate'  # 用户操作日志
TABLENAME_IP_PROHIBIT = 'prohibit_ip'  # 被封禁的ip信息表

##################################################################

# 处理请求的正则表达式

RE_COTENT_LENGTH = r'(?<=Content-Length:)(.*)\n'
RE_METHOD = r'(GET|POST)'  # 匹配出GET还是POST请求
RE_URL = r'(?<=T\s)(.*)(?=\sHTTP)'  # 匹配url，以(GET或POST )开头以(空格HTTP或HTTPS)结尾
RE_AGENT = r'(?<=User-Agent:\s)(.*)(?=\r\n)'  # 匹配userAgent
RE_COOKIE = r'(?<=Cookie:\s)(.*)'  # 匹配cookie
RE_FILES_URL = r'(.*)(?=\?)'  # 将url中目录文件部分匹配出来，即？之前匹配出来
RE_GET_URL = r'(?<=\?)(.*)'  # 将url中get请求部分分离出来，匹配？之后的
RE_GET_SPLIT = r'(?<=\=)(.*)'  # 将get或请求中数据提取出来,提取=后面的数据
RE_POST_SPLIT = r'(.*)(?=\=)'  # 将POST请求中=前面的信息提取出来

RE_POST_UPDATE_TYPE = r'(?<=Content-Type:\s)(.*)\r'  # 获得文件上传时的上传文件类型
RE_POST_UPDATE_SUFFIX = r'(?<=filename\=\")(.*)\"'  # 获得文件上传时文件后缀

RE_IP = r'((?:(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d?\d))'  # 匹配IP地址
RE_STATUS = r'(on|off)'  # 匹配规则状态
##################################################################
# 本地规则文件名

FILE_RULES_PATH = 'rules'  # 规则文件所在文件地址目录

FILENAME_RULES_URL = 'rules_url.json'  # url黑名单文件名
FILENAME_RULES_GET = 'rules_get.json'  # sql黑名单文件名
FILENAME_RULES_POST = 'rules_post.json'  # xss黑名单文件名
FILENAME_IP_PROHIBIT = 'prohibit_ip.json'  # 被封禁的ip表
##################################################################
# 加载的文件
LOAD_GET = 'GET'  # 加载GET
LOAD_POST = 'POST'  # 加载POST
LOAD_URL = 'URL'  # 加载URL
LOAD_PROHIBIT = 'PROHIBIT'  # 加载ip黑名单

##################################################################
