#-*- coding:utf-8 -*-
'''
Created on 2019��5��10��

@author: Administrator
'''
import Configuration
queue_name1 = Configuration.configs['queue_name1']
queue_name2 = Configuration.configs['queue_name2']
queue_name3 = Configuration.configs['queue_name3']

def connect_and_subscribe1(conn):
    conn.start()
    conn.connect('admin','admin',wait=True)
    conn.subscribe(queue_name1,ack='client',id=1)
    print('restart QUEUE1')
    
def connect_and_subscribe2(conn):
    conn.start()
    conn.connect('admin','admin',wait=True)
    conn.subscribe(queue_name2,ack='client',id=2)
    print('restart QUEUE2')

def connect_and_subscribe3(conn):
    conn.start()
    conn.connect('admin','admin',wait=True)
    conn.subscribe(queue_name2,ack='client',id=3)
    print('restart QUEUE3')