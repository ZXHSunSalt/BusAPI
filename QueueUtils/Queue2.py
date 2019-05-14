#-*- coding:utf-8 -*-
'''
Created on 2019��5��10��

@author: Administrator
'''
from QueueUtils.__init__ import *
from ListenersUtils import LoadModel,Listener2

address = Configuration.configs['address']
port = Configuration.configs['port']
queue_name2 = Configuration.configs['queue_name2']
listener_name2 = Configuration.configs['listener_name2']
def send_to_queue2(out1):
    '''
    FUNCTION:SEND MESSAGE TO QUEUE2
    '''
    conn = stomp.Connection([(address,port)],heartbeats=(60000,60000))
    #conn = stomp.Connection11([(address,post)])
    conn.start()
    conn.connect('admin','admin',wait=True)
    conn.send(queue_name2,out1)
    conn.disconnect()
        

def receive_from_queue2():
    '''
    FUNCTION:RECEIVE PROCESSED DATA FORM QUEUE2 AND SEND MESSAGE TO QUEUE3
    NOTICE: GET THE CLASSIFICATION OF EACH IMAGES AND RETURN THE CLASSIFICATION RESULTS THROUGH LISTENER2
    '''
    conn = stomp.Connection([(address,port)],heartbeats=(60000,60000))
    #conn = stomp.Connection11([(address,post)])
    net = LoadModel.load_model()
    conn.set_listener(listener_name2, Listener2.Listener2(conn,net))
    conn.start()
    conn.connect('admin','admin',wait=True)
    conn.subscribe(queue_name2,id=2,ack='client')
    return conn