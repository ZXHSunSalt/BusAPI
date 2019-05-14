#-*- coding:utf-8 -*-
'''
Created on 2019��5��10��

@author: Administrator
'''
import Configuration
import sys,os
import numpy as np

# transform all the data of image numpy array
np.set_printoptions(threshold=np.inf)

caffe_root=Configuration.configs['caffe_root']
sys.path.insert(0,caffe_root+'python')
##set parameters to sheild the lod display of caffe model 
os.environ["GLOG_minloglevel"]= '3'
import caffe

def load_model():
    caffe.set_mode_gpu()
    caffe.set_device(0)
    # import caffe model
    model_def = Configuration.configs['model_prototxt_path']
    model_weights = Configuration.configs['caffe_model_path']
    net=caffe.Net(model_def, model_weights, caffe.TEST)
    return net