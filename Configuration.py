#-*- coding:utf-8 -*-
'''
Created on 2019年4月12日

@author: Administrator
'''
configs ={
    ## define the post port
    "port":"61613",
    #"address":'106.14.148.134',
    "address":'192.168.1.135',
    ## define queue name and listener name for 3 queues
    "queue_name1" : 'Queue1',
    "listener_name1" : 'Listener1',
    "queue_name2" : 'Queue2',
    "listener_name2" : 'Listener2',
    "queue_name3" : 'Queue3',
    "listener_name3" : 'Listener3',
    
    "path":'/home/jhx/bus/file_cache/',
    "log_path":'/home/jhx/bus/',
    "img_path":'/home/jhx/bus/img_path_cache/',
    "caffe_root" :'/home/jhx/caffe/',
    "model_prototxt_path":'/home/jhx/bus/z/deploy_full_conv.prototxt',
    "caffe_model_path":'/home/jhx/bus/z/model_60000_conv.caffemodel'
}

        
