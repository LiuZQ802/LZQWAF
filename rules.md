# 正则规则

## URL黑名单

```python
(admin|phpmyadmin|www|wwwroot|root|admin|host)  #匹配敏感目录
```



## GET黑名单

### sql注入

description:         正则

特殊字符:              sql注入|xss|命令执行

```python
(\'|\"|\||\(|\))             #匹配 ' " (  )  |
(/|\\|\*|&)                #匹配 \ / *&
(-|\+|<|>)                    #匹配 - + < >
```

报错注入:              sql注入

```python
(extractvalue|updatexml)
```

敏感字符  sql注入

```python
(\s(union|select|or|and|limit|sleep|benchmark|offset)\s)
(\s(like|rlike|regexp|group|substr|)\s)
```



### 文件包含

伪协议     文件包含 

```
(file://|php://|data://)
```

webshell   文件包含

```python
(phpinfo)
```



### XSS

```python
(<(.*)script>|<img(.*)>|<input(.*)>)
```



## POST黑名单

### POST SQL注入

特殊字符

```python
(\'|\"|\||\(|\))             #匹配 ' " (  )  |
(/|\\|\*|&|\#)                #匹配 \ / *& #
(-|\+|<|>)                    #匹配 - + < >
```

敏感字符

```python
(\s(union|select|or|and|limit|sleep|benchmark|offset)\s)
(\s(like|rlike|regexp|group|substr|)\s)
```

### 文件上传

文件类型白名单

```python
(image/jpeg|image/png|image/jpg)     #只允许上传这些文件类型
```

文件后缀黑名单

```python
(php|htm|jsp|jsw|jsv|jtml|asp|asa|asc|ash|asm|cer|swf|7z) 
```

### XSS

```python
(<(.*)script>|<img(.*)>|<input(.*)>)
```



### 命令执行

```
(ipconfig|ifconfig|cat|tac|less|chmod|more)      #敏感字符
(head|tail|nl|taillf|sort|paste)   #敏感字符
(\||\&|\'|\"|;|\$)   #特殊字符
```

