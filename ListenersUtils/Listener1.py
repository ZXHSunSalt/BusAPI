#-*- coding:utf-8 -*-
'''
Created on 2019��5��10��

@author: Administrator
'''

import Configuration
import json,os,cv2
from skimage import io
from utils import L1
from QueueUtils import Queue2,Queue3
from Reconnection import connect_and_subscribe1

path = Configuration.configs['path']
img_path = Configuration.configs['img_path']
log_path = Configuration.configs['log_path']

# num = 0
error_count = 1 

class Listener1(object):
    '''
    FUNCTION: DEFINE A LISTENER CLASS FOR QUEUE1
            1.GET THE CLIENT MESSAGE-ID,TYPE,PICS,IMAGES OF VIDEO
            2.RETURN ALL THE DATA
    '''
    def __init__(self,conn):
        self.conn = conn

    def on_error(self,headers,message):
        print('QUEUE1 received an error "%s"'% message)
 
    def on_disconnected(self):
        print('QUEUE1 disconnect')
        connect_and_subscribe1(self.conn)

    def on_heartbeat_timeout(self):
#         connect_and_subscribe1(self.conn)
        print('queue1 heartbeat timeout')

    def on_message(self, headers, message1):
        global num
        global error_count
        try:
           # transform json data to dict type
           message = json.loads(message1)
           # get relevant params
           bus_id = message['id']
           guid = message['guid']
           creat_time = message['creat_time']
           input_type = message['type']
           pics = message['pics']
           video = message['video']

           i = 0
           new_path = path+guid+'/'
  
           img_txt_path = img_path+guid
           fileList = []
           if not os.path.exists(new_path):
               os.makedirs(new_path)
               
           if len(pics)==0 and len(video)==0:
               error_msg = 'nodata'
               error_value = {'id':bus_id,
                              'creat_time':creat_time,
                              'input_type':input_type,
                              'results':'error',
                              'output_type':error_msg
                             }
               error_value = json.dumps(error_value)
               Queue3.send_to_queue3(error_value)
               self.conn.ack(headers["message-id"],1)
           else:
               with open(img_path+guid+'.txt','a+') as fi:
                   for pic in pics:
                       try:
                           fileList.append(pic)
                           img = io.imread(pic)
                           img = cv2.resize(img,(227,227))
                           img_name = input_type+str(i)+'.jpg'
                           cv2.imwrite(new_path+input_type+str(i)+'.jpg',img)
                           i += 1
                           fi.write(new_path+img_name+'\n')
                       except:
                           with open(log_path+'Queue1_log.txt','a+') as f:
                               error_num_count = 'the num of wrong data is:'+str(error_count)+'\n'
                               log_msg = 'car_id:['+bus_id+']'+','+'creat_time'+creat_time+'\n'
                               f.write(error_num_count)
                               f.write(log_msg)
                           f.close()
                           error_count += 1
                           error_msg = 'pic_error'
                           error_value = {'id':bus_id,
                                          'creat_time':creat_time,
                                          'input_type':input_type,
                                          'results':'error',
                                          'output_type':error_msg
                                         }
                           error_value = json.dumps(error_value)
                           Queue3.send_to_queue3(error_value)
                           with open(log_path+'Queue2_log.txt','a+') as f:
                               send_msg = 'send_msg:'+error_value
                               f.write(send_msg+'\n')
                           print('Queue1 load pic Error!')   
                            
                   # transform video into images and save images
                   for v_url in video:
                       try:
                           fileList.append(v_url)
                           video_images = L1.video_process(v_url)
                           for img in video_images:
                               img = cv2.resize(img,(227,227))
           #                             try:
           #                                 img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
           #                             except:
           #                                 pass
                               img_name = input_type+str(i)+'.jpg'
                               cv2.imwrite(new_path+input_type+str(i)+'.jpg',img)
                               i += 1
                               fi.write(new_path+img_name+'\n')
                             
                       except:
                           with open(log_path+'Queue1_log.txt','a+') as f:
                               error_num_count = 'the num of wrong data is:'+str(error_count)+'\n'
                               log_msg = 'car_id:['+bus_id+']'+','+'creat_time'+creat_time+'\n'
                               f.write(error_num_count)
                               f.write(log_msg)
                           f.close()    
                           error_count += 1
                           error_msg = 'video_error'
                           error_value = {'id':bus_id,
                                     'creat_time':creat_time,
                                     'input_type':input_type,
                                     'results':'error',
                                     'output_type':error_msg
                                       }
                           error_value = json.dumps(error_value)
                           Queue3.send_to_queue3(error_value)
                           with open(log_path+'Queue2_log.txt','a+') as f:
                               send_msg = 'send_msg:'+error_value
                               f.write(send_msg+'\n')
                           print('Queue1 load video Error!')     
               fi.close()
               # define the param of listener1 which will be sent to queue2
               listener1_value = {"id":bus_id,\
                                  "guid":guid,\
                                  "creat_time":creat_time,\
                                  "type":input_type,\
                                  "img_txt_path":img_txt_path,\
                                  "pic_addr":new_path
                       }
               out1 = json.dumps(listener1_value)
               Queue2.send_to_queue2(out1)
               self.conn.ack(headers["message-id"],1)
               print('process [%s] data,message_id:%s'%(bus_id,headers["message-id"]))

        except:
            print('QUEUE1 error!')

    
