#-*- coding:utf-8 -*-
import cv2
import numpy as np
import Configuration
import os,sys
import json
# transform all the data of image numpy array
np.set_printoptions(threshold=np.inf)

caffe_root=Configuration.configs['caffe_root']
sys.path.insert(0,caffe_root+'python')
##set parameters to sheild the lod display of caffe model 
os.environ["GLOG_minloglevel"]= '3'
import caffe