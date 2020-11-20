# -*- coding: utf-8 -*-


'''
Created on 2017��4��4��

@author: Tian
'''

import xlrd
import csv
import os
import codecs
import numpy as np
from datetime import datetime, timedelta

#column: 2 time, 9 date, 99 datetime
def Read_bird_trip(file_name, column, type = 0):
    temp = []
    
    num_trip_temp = read_csv(file_name, 0, 0)
    num_trip = np.array(list(set(num_trip_temp)))
    num_trip.astype(int) #number of trips
    
    for i in range(len(num_trip)):
        temp.append([])
    
    reader = csv.reader(open(file_name, 'r'))
    for i, rows in enumerate(reader):
        if i == 0:
            continue
        if type == 0:
            temp[int(rows[0]) - 1].append(float(rows[column]))
        elif type == 1:
            temp[int(rows[0]) - 1].append(rows[column])
        elif type == 99: #write datetime
            date_temp = rows[9].split('/')[2] + '-' + rows[9].split('/')[1] + '-' + rows[9].split('/')[0] + ' ' + rows[2] + '.000'
            date_time = datetime.strptime(date_temp,"%Y-%m-%d %H:%M:%S.%f") + timedelta(seconds = int(3600 * 9))
            temp[int(rows[0]) - 1].append(date_time)
            
    #print temp
    
    return temp


def Read_data_in_folder(folder_path, rows, type = 0):
    file_names = read_file_in_folder(folder_path)
    #print file_names
    depth = read_files(file_names, rows, type)
    
    return depth
    #print file_name

def read_files(file_names, list, type):
    temp = []
    for i in range(len(file_names)):
        #print file_names[i]
        temp.extend(read_csv(file_names[i], list, type))
        
    return temp
    

def read_file_in_folder(folder_path):
    file_name = os.listdir(folder_path)
    file_names = []
    for filename in file_name:
        file_names.append(os.path.join(folder_path, filename))
    
    return file_names

def read_csv(name, list, type): #type: 0: float, 1: string 
    temp = []
    reader = csv.reader(open(name, 'r'))
    for i, rows in enumerate(reader):
        if i == 0:
            continue
        if type == 0:
            temp.append(float(rows[list]))
        else:
            temp.append(rows[list])
    return temp

#read bat data from file path
def read_batdata(file_path):
    #Times = []  
    Longitude = []
    Latitude = []
    #Capture = []
    
    #a = open_xlsm(file_path, Times, 0)
    #open_xlsm(file_path, X_axis, 1)
    open_xlsm(file_path, Longitude, 3)
    open_xlsm(file_path, Latitude, 4)
    #print Times
    return Longitude, Latitude 


def open_xlsm(file_path, temp, row):
    data = xlrd.open_workbook(file_path) #open xls
    
    sheet = data.sheet_by_index(0)
    #sheet = data.sheet_by_name(sheet)
    nrows = sheet.nrows # row of sheet

    for i in range(nrows): # 
        if i == 0: # 
            continue
        temp.append(sheet.cell(i, row).value)
        
    return nrows

def read_txt(file_name):
    temp = []
    
    f = open(file_name)
    
    lines = f.readlines()
    
    for line in lines:
        temp.append(int(line[:-1]))
    f.close()
    
    return temp

def read_txt_d(file_name):
    temp = []
    
    f = open(file_name)
    
    lines = f.readlines()
    
    for line in lines:
        temp.append(float(line[:-1]))
    f.close()
    
    return temp

def write(file_ame, input_data):
    f = codecs.open(file_ame, 'a', 'utf-8')
    for i in input_data:
        f.write(str(i)+'\r\n')
    
    f.close()