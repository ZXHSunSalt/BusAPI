#-*- coding:utf-8 -*-
'''
Created on 2019��5��10��

@author: Administrator
'''
from QueueUtils.__init__ import *
import Configuration

address = Configuration.configs['address']
port = Configuration.configs['port']
queue_name1 = Configuration.configs['queue_name1']
listener_name1 = Configuration.configs['listener_name1']

def send_to_queue1(msg):
    '''
    FUNCTION:RECEIVE MESSAGE FROM CLIENT AND SEND MESSAGE TO QUEUE1
    '''
    conn = stomp.Connection([(address,port)],heartbeats=(60000,60000))
    #conn = stomp.Connection11([(address,post)])
    conn.start()
    conn.connect('admin','admin',wait=True)
    conn.send(queue_name1,msg)
    conn.disconnect()   
    

def receive_from_queue1():
    '''
    FUNCTION:RECEIVE MESSAGE FROM QUEUE1 AND SEND MESSAGES TO QUEUE2 THROUGH LISTENER1
    '''
    conn = stomp.Connection([(address,port)],heartbeats=(60000,60000))
    #conn = stomp.Connection11([(address,post)])
    conn.set_listener(listener_name1, Listener1.Listener1(conn))
    conn.start()
    conn.connect('admin','admin',wait=True)
    conn.subscribe(queue_name1,id=1,ack='client')
    return conn
