# -*- coding: utf-8 -*-

'''
Created on 2019��3��19��

@author: tian

'''

import numpy as np
import sklearn
import random
import warnings


from sklearn.model_selection import train_test_split, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing


file_name = 'Calssification_0920_7-7.5.txt'
compared_file_name_1 = 'Calssification_0920_0-1.txt'
compared_file_name_2 = 'Calssification_0920_0-2.txt'
compared_file_name_3 = 'Calssification_0920_0-3.txt'
compared_file_name_4 = 'Calssification_0920_0-4.txt'
compared_file_name_5 = 'Calssification_0920_0-5.txt'
compared_file_name_6 = 'Calssification_0920_0-6.txt'
compared_file_name_7 = 'Calssification_0920_0-7.txt'

int_len = 54 #number of features + label(1)


def main():
    warnings.filterwarnings('ignore')
    random.seed(0)
    data = load_txt_NAN(file_name, int_len)
    
    compared_data_1 = load_txt_NAN(compared_file_name_1, int_len)
    compared_data_2 = load_txt_NAN(compared_file_name_2, int_len)
    compared_data_3 = load_txt_NAN(compared_file_name_3, int_len)
    compared_data_4 = load_txt_NAN(compared_file_name_4, int_len)
    compared_data_5 = load_txt_NAN(compared_file_name_5, int_len)
    compared_data_6 = load_txt_NAN(compared_file_name_6, int_len)
    compared_data_7 = load_txt_NAN(compared_file_name_7, int_len)
    
    
    x, y = np.split(data, (int_len,), axis=1)
    
    #compared data set test 
    x_1, y_1 = np.split(compared_data_1, (int_len,), axis=1)
    x_2, y_2 = np.split(compared_data_2, (int_len,), axis=1)
    x_3, y_3 = np.split(compared_data_3, (int_len,), axis=1)
    x_4, y_4 = np.split(compared_data_4, (int_len,), axis=1)
    x_5, y_5 = np.split(compared_data_5, (int_len,), axis=1)
    x_6, y_6 = np.split(compared_data_6, (int_len,), axis=1)
    x_7, y_7 = np.split(compared_data_7, (int_len,), axis=1)
    
    int_len0 = 48
    x_1 = x_1[:, : int_len0] #int_len
    x_2 = x_2[:, : int_len0] #int_len
    x_3 = x_3[:, : int_len0] #int_len
    x_4 = x_4[:, : int_len0] #int_len
    x_5 = x_5[:, : int_len0] #int_len
    x_6 = x_6[:, : int_len0] #int_len
    x_7 = x_7[:, : int_len0] #int_len
    x = x[:, : int_len0]

    y = y[:,:1]

    print (x[:,13])

    min_max_scaler = preprocessing.MinMaxScaler()
    x = min_max_scaler.fit_transform(x)
    x_1 = min_max_scaler.fit_transform(x_1)
    x_2 = min_max_scaler.fit_transform(x_2)
    x_3 = min_max_scaler.fit_transform(x_3)
    x_4 = min_max_scaler.fit_transform(x_4)
    x_5 = min_max_scaler.fit_transform(x_5)
    x_6 = min_max_scaler.fit_transform(x_6)
    x_7 = min_max_scaler.fit_transform(x_7)
    
    '''for single feature classification
    id = 47
    x = x[:,  id].reshape(-1, 1)
    x_1 = x_1[:,  id].reshape(-1, 1)
    x_2 = x_2[:,  id].reshape(-1, 1)
    x_3 = x_3[:,  id].reshape(-1, 1)
    x_4 = x_4[:,  id].reshape(-1, 1)
    x_5 = x_5[:,  id].reshape(-1, 1)
    x_6 = x_6[:,  id].reshape(-1, 1)
    x_7 = x_7[:,  id].reshape(-1, 1)
    '''
    
    print ('0-1 h')
    cross_validation(x_1, y)
    print ('0-2 h')
    cross_validation(x_2, y)
    print ('0-3 h')
    cross_validation(x_3, y)
    print ('0-4 h')
    cross_validation(x_4, y)
    print ('0-5 h')
    cross_validation(x_5, y)
    print ('0-6 h')
    cross_validation(x_6, y)
    print ('0-7 h')
    cross_validation(x_7, y)
    print ('0-7.5 h')
    cross_validation(x, y)



def trip_type(s):
    it = {'1': 1, '0': 0}
    return int(it[str(s)])


#load txt including NAN
def load_txt_NAN(file_name, data_len):
    data = np.loadtxt(file_name, dtype = 'str', delimiter = ' ', converters={data_len: trip_type}, encoding='UTF-8')
    data_temp = []
    for i in range(len(data)):
        data_temp.append([])
        for j in range(len(data[i])):
            if data[i][j] == 'nan':
                data_temp[-1].append(np.nan)
            else:
                data_temp[-1].append(float(data[i][j]))
   
    return np.array(data_temp)


    
def cross_validation(x, y):
    scoring = ['accuracy','precision_macro', 'recall_macro', 'f1_macro']
        #Logistic regression
    print ('Logistic regression')
    clf_rfc = LogisticRegression(solver='liblinear', C = 1000, penalty = 'l2')
    scores = cross_validate(clf_rfc, x, y.ravel(), cv = 10, scoring=scoring, return_train_score=False)  #cv为迭代次数。
    sorted(scores.keys())
    
    print('测试结果：', scores['test_accuracy'].mean(), scores['test_precision_macro'].mean(), scores['test_recall_macro'].mean(), scores['test_f1_macro'].mean()) 
    

if __name__=="__main__":
    main()