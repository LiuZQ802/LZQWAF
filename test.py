# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Project :  LZQWAF
@File    :  test
@Author  :  刘子琦
@Data    :  2022/5/9
@Description:
    
"""
from threading import Thread
from time import sleep
import random

def cc(thread):
    for i in range(3):
        print(thread+'\n')
        sleep(random.randint(0,1))


def test():
    i=0
    while True:
        print(str(i)+'\n')
        thread = Thread(target=cc, args=('这是进程'+str(i),))
        thread.setDaemon(True)
        thread.start()
        i+=1
test()