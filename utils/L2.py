#-*- coding:utf-8 -*-
'''
Created on 2019��5��10��

@author: Administrator
'''
import numpy as np
from numba.cuda.args import Out

def type_judgement(result_num,input_type):
    '''
    This function is designed for judging whether the original results are consistent with the predicted results
    '''
    type_dict1 = {'smoke':0, 'distraction':1, 'abnormaldriving':2,'call':3,'fatigue':4,'other':5}
    type_dict2 = {0:'smoke', 1:'distraction', 2:'abnormaldriving',3:'call',4:'fatigue',5:'other'}
    output_type = []
    results = []
    # transform input type-list to str
    input_type = "".join(input_type)
    # the output of result is 'yes' or 'no'
    flag_y = 0
    flag_n = 0
    for i in result_num:
        output_type.append(type_dict2[i])
        if type_dict1[input_type] == i:
            result = 'yes'
            results.append(result)
            flag_y += 1
        else:
            result = 'no'
            results.append(result)
            flag_n += 1
    print(results,output_type)       
    return results,output_type
def get_final_result(output_results,input_type):
    '''
    THIS FUNCTION IS DESIGNED FOR OUTPUT THE FINAL RESULT ACCORDING THE IMAGE AND VIDEO CLASSIFICAITON OUTPUT RESUTLS
    '''
    # COUNT THAT HOW MANY YES AND NO IN THE OUTPUT RESUTL
    count_n = 0
    count_y = 0
    for each in output_results:
        if each == "no":
            count_n += 1
        else:
            count_y += 1
    total_num = len(output_results)
    percent = count_y/total_num
    print(percent)
    if input_type == "smoke":
        if percent  > 0:
            final_result = 'yes'
        else:
            final_result = 'no'
    elif input_type == "distraction":
        if percent > 0.5:
            final_result = 'yes'
        else:
            final_result = 'no'
    elif input_type == "abnormaldriving":
        if percent > 0.5:
            final_result = 'yes'
        else:
            final_result = 'no'
    elif input_type == "call":
        if percent > 0.8:
            final_result = 'yes'
        else:
            final_result = 'no'
    elif input_type == "fatigue":
        if percent > 0.3:
            final_result = 'yes'
        else:
            final_result = 'no'
#     if count_n >= count_y:
#         final_result = 'no'
#     else:
#         final_result = 'yes'
    return final_result

def get_final_type(output_type):
    '''
    THIS FUNCTION IS DESIGNED FOR OUTPUT THE FINAL RESULT ACCORDING THE IMAGE AND VIDEO CLASSIFICAITON OUTPUT RESUTLS
    '''
    # COUNT THAT HOW MANY YES AND NO IN THE OUTPUT RESUTL
    count_0 = 0
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count_5 = 0
    type_dict = {0:'smoke', 1:'distraction', 2:'abnormaldriving',3:'call',4:'fatigue',5:'other'}
    for i in range(len(output_type)):
        if output_type[i] == "smoke":
            count_0 += 1
        elif output_type[i] == "distraction":
            count_1 += 1
        elif output_type[i] == "abnormaldriving":
            count_2 += 1
        elif output_type[i] == "call":
            count_3 += 1
        elif output_type[i] == "fatigue":
            count_4 += 1
        elif output_type[i] == "other":
            count_5 += 1
    counts = [count_0,count_1,count_2,count_3,count_4,count_5]
    # get the index of the maxmium value in counts
    out_index = np.array(counts).argmax()
    #print(out_index)
    final_output_type =  type_dict[out_index]
    
    return final_output_type
