#-*- coding:utf-8 -*-
'''
Created on 2019��5��10��

@author: Administrator
'''
from Reconnection import connect_and_subscribe3

class Listener3(object):
    '''
    FUNCITON: RECEIVE PIC AND PICS OF VIDEO'S RESULTS, GET THE FINAL RESULTS  
    '''
    def __init__(self,conn):
        self.conn = conn
        
    def on_disconnected(self):
        print('QUEUE3 disconnect')
        connect_and_subscribe3(self.conn)

    def on_heartbeat_timeout(self):
        print('queue3 heartbeat timeout')
        
#     receive_from_queue2()
    def on_message(self, headers, msg): 
        print(msg)
        print('QUEUE3 SUCCESED')