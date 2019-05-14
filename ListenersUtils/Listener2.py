#-*- coding:utf-8 -*-
'''
Created on 2019��5��10��

@author: Administrator
'''
import Configuration
import json,os,sys,shutil
import numpy as np
from QueueUtils import Queue2,Queue3
from Reconnection import connect_and_subscribe2
from utils import L2

# transform all the data of image numpy array
np.set_printoptions(threshold=np.inf)

caffe_root=Configuration.configs['caffe_root']
sys.path.insert(0,caffe_root+'python')
##set parameters to sheild the lod display of caffe model 
os.environ["GLOG_minloglevel"]= '3'
import caffe

path = Configuration.configs['path']
img_path = Configuration.configs['img_path']
log_path = Configuration.configs['log_path']

num = 0

class Listener2(object):
    '''
    FUNCTION: RECEIVE DATA FROM QUEUE1 AND CLASSIFY THE DATA,FINALLY, SEND THE CLASSIFICAITON RESULT TO QUEUE3
    '''
    def __init__(self,conn,net):
        self.conn = conn
        self.net = net
        print('load net')
        
    def on_error(self,headers,message):
        print('QUEUE2 received an error "%s"'% message)
 
    def on_disconnected(self):
        print('QUEUE2 disconnect')
        connect_and_subscribe2(self.conn)
        
    def on_heartbeat_timeout(self):
        print('queue2 heartbeat timeout')

    def on_message(self, headers, msg):
        global num
        try:
            #message = json.loads(msg.encode('utf-8'))
            message = json.loads(msg)
            message_id = headers['message-id']
            bus_id = message['id']
            guid = message['guid']
            creat_time = message['creat_time']
            input_type = message['type']
            img_txt_path = message['img_txt_path']
            
            txt_path = img_txt_path+'.txt'
            with open(txt_path,'r') as img_f:
                img_lists = img_f.read()
                
            result_num = self.img_judgement(self.net,img_lists,bus_id,creat_time,input_type,message_id)
            if len(result_num) == 0:
                pass
            else:
                pic_results ,output_type_lists= L2.type_judgement(result_num,input_type)        
                final_result = L2.get_final_result(pic_results,input_type)
                final_output_type = L2.get_final_type(output_type_lists)
    
                listener_value = {'id':bus_id,
                                  'creat_time':creat_time,
                                  'input_type':input_type,
                                  'results':final_result,
                                  'output_type':final_output_type
                    }
                final_out = json.dumps(listener_value)
                Queue3.send_to_queue3(final_out)
    #                 try:
                self.conn.ack(headers["message-id"],2)
    #                 except:
    #                     print('queue2 ack connection error')
                num += 1
                print('Have processed %d data,message-id:%s:'%(num,headers["message-id"]))
                            
                with open(log_path+'Queue2_log.txt','a+') as f:
                    log_msg = 'Have processed:'+'['+str(num)+']'+'data'+'|'+'message-id:'+headers["message-id"]+'\n'
                    f.write(log_msg+'\n')
                    send_msg = 'send_msg:'+final_out
                    f.write(send_msg+'\n')
                f.close()
                new_path = path+guid+'/'
                if os.path.exists(new_path):
                    shutil.rmtree(new_path)
                os.remove(txt_path)
        except:
            print('QUEUE2 ERRORS')
                  
    def img_judgement(self,net,img_lists,bus_id,creat_time,input_type,message_id):
        '''
        This function is designed for image classification.
        There are several steps in this function: 1.import caffe model
                                                  2.do image pre-processing
                                                  3.do classification according to the caffe model and return the output result
                                                    (the type of output result is int number )
        '''
        result_nums = []
        caffe.set_mode_gpu()
        caffe.set_device(0)

        img_lists = img_lists.split()

        for each in img_lists:
            # do image pre-processing

            transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
            transformer.set_transpose('data', (2, 0, 1))
            transformer.set_raw_scale('data', 227)
            transformer.set_channel_swap('data', (2, 1, 0))
            
            new_pic=caffe.io.load_image(each)
            transformed_image = transformer.preprocess('data',new_pic)
            # copy the image data into the memory allocated for the net
            self.net.blobs['data'].data[...] = transformed_image
            
            # perform classification
            output = net.forward()
            # the output probability vector for the first image in the batch
            output_prob = output['prob'][0]  
            type_result_num = output_prob.argmax()
            result_nums.append(type_result_num)
            print(result_nums)
        return result_nums
