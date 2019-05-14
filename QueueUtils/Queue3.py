#-*- coding:utf-8 -*-
'''
Created on 2019��5��10��

@author: Administrator
'''
from QueueUtils import *
import Configuration
from ListenersUtils import Listener3

address = Configuration.configs['address']
port = Configuration.configs['port']
queue_name3 = Configuration.configs['queue_name3']
listener_name3 = Configuration.configs['listener_name3']
def send_to_queue3(final_out):
    '''
    FUNCITON:SEND MESSAGES TO QUEUE3
    '''
    conn = stomp.Connection([(address,port)],heartbeats=(60000,60000))
    #conn = stomp.Connection11([(address,post)])
    conn.start()
    conn.connect('admin','admin',wait=True)
    conn.send(queue_name3,final_out)
    conn.disconnect()
#     conn.disconnect()
        

def receive_from_queue3():
    '''
    FUNCTION:GET THE RESULTS OF EACH IMAGE AND SEND THE FINAL RESULTS THROUGH LISTENER3    
    '''
    conn = stomp.Connection([(address,port)],heartbeats=(60000,60000))
    #conn = stomp.Connection11([(address,post)])
    conn.set_listener(listener_name3, Listener3.Listener3(conn))
    conn.start()
    conn.connect('admin','admin',wait=True)
    conn.subscribe(queue_name3,id=3)
    return conn