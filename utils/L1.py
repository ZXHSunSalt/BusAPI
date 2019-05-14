#-*- coding:utf-8 -*-
'''
Created on 2019��5��10��

@author: Administrator
'''

import cv2

def video_process(video_full_path):
        '''
        This function is designed for getting video image and return a list of image in the video
        video_full_path:the url of image
        '''
        # the frequency of extracting frames
        EXTRACT_FREQUENCY = 10 
        # read video data
        cap_video = cv2.VideoCapture(video_full_path)
        # flag for the frequency of reading video
        count = 1
        video_img = []
        
        # extract the frames/images 
        while True:
            rval,frame = cap_video.read()
            if rval == True:
                if count % EXTRACT_FREQUENCY == 0:
                    video_img.append(frame)
            else:
                break
            count += 1
        
        # finish video process
        cap_video.release()
        cv2.destroyAllWindows()
        return  video_img
