# -*- coding: utf-8 -*-

'''
Created on 2019��1��8��

@author: tian

read water depth from files and draw out according to the trip

'''

from __future__ import division
from sklearn import preprocessing
from datetime import datetime, timedelta

import xlrd
import csv
import os
import Read_Data
import numpy as np
import Calculate_angle_speed
import FPT_R
import xlwt
import math
import warnings
# input files
bird_depth_2016_path = 'depth//depth_2016//'
bird_depth_2017_path = 'depth//depth_2017//'
bird_depth_2018_path = 'depth//depth_2018//' #backup//

#GPS
bird_GPS_2016_path = 'input_data//2016//'
bird_GPS_2017_path = 'input_data//2017//'
bird_GPS_2018_path = 'input_data//2018//'



warnings.filterwarnings("ignore")

#struct definition， extracted features
class E_features:
    def __init__(self):
        self.max_speed = []
        self.min_speed = []
        self.avg_speed = []
        self.std_speed = []
        self.median_speed = []
        self.l_quantile_speed = []
        self.h_quantile_speed = []
        self.ptp_speed = []
        self.cv_speed = []
        self.iqr_speed = []
        
        self.max_acceleration = []
        self.min_acceleration = []
        self.avg_acceleration = []
        self.std_acceleration = []
        self.median_acceleration = []
        self.l_quantile_acceleration = []
        self.h_quantile_acceleration = []
        self.ptp_acceleration = []
        self.cv_acceleration = []
        self.iqr_acceleration = []
        
        self.max_displacement_30 = []
        self.avg_displacement_30 = []
        
        self.max_displacement = []
        self.min_displacement = []
        self.avg_displacement = []
        self.std_displacement = []
        self.median_displacement = []
        self.l_quantile_displacement = []
        self.h_quantile_displacement = []
        self.ptp_displacement = []
        self.cv_displacement = []
        self.iqr_displacement = []
        
        self.max_fpt_100 = []
        self.min_fpt_100 = []
        self.avg_fpt_100 = []
        self.median_fpt_100 = []
        self.std_fpt_100 = []
        self.l_quantile_fpt_100 = []
        self.h_quantile_fpt_100 = []
        self.ptp_fpt_100 = []
        self.cv_fpt_100 = []
        self.iqr_fpt_100 = []
        
        self.max_fpt_1000 = []
        self.min_fpt_1000 = []
        self.avg_fpt_1000 = []
        self.median_fpt_1000 = []
        self.std_fpt_1000 = []
        self.l_quantile_fpt_1000 = []
        self.h_quantile_fpt_1000 = []
        self.ptp_fpt_1000 = []
        self.cv_fpt_1000 = []
        self.iqr_fpt_1000 = []
        
        self.max_fpt_10000 = []
        self.min_fpt_10000 = []
        self.avg_fpt_10000 = []
        self.median_fpt_10000 = []
        self.std_fpt_10000 = []
        self.l_quantile_fpt_10000 = []
        self.h_quantile_fpt_10000 = []
        self.ptp_fpt_10000 = []
        self.cv_fpt_10000 = []
        self.iqr_fpt_10000 = []
        
        self.max_fpt_500 = []
        self.min_fpt_500 = []
        self.avg_fpt_500 = []
        self.median_fpt_500 = []
        self.std_fpt_500 = []
        self.l_quantile_fpt_500 = []
        self.h_quantile_fpt_500 = []
        self.ptp_fpt_500 = []
        self.cv_fpt_500 = []
        self.iqr_fpt_500 = []
        
        self.max_fpt_5000 = []
        self.min_fpt_5000 = []
        self.avg_fpt_5000 = []
        self.median_fpt_5000 = []
        self.std_fpt_5000 = []
        self.l_quantile_fpt_5000 = []
        self.h_quantile_fpt_5000 = []
        self.ptp_fpt_5000 = []
        self.cv_fpt_5000 = []
        self.iqr_fpt_5000 = []
        
        self.max_fpt_50000 = []
        self.min_fpt_50000 = []
        self.avg_fpt_50000 = []
        self.median_fpt_50000 = []
        self.std_fpt_50000 = []
        self.l_quantile_fpt_50000 = []
        self.h_quantile_fpt_50000 = []
        self.ptp_fpt_50000 = []
        self.cv_fpt_50000 = []
        self.iqr_fpt_50000 = []
        
        self.max_water_depth = []
        self.min_water_depth = []
        self.avg_water_depth = []
        self.std_water_depth = []
        self.median_water_depth = []
        self.ptp_water_depth = []
        
        self.bird_ori_start2end = []
        self.bird_ori_avg = []
        self.bird_ori_std = []
        
        self.dis_se = []
        self.sst = []
        self.distant = []
        self.start_time = []
        self.end_time = []
        self.sum_hour = 0
        self.sum_hour_s = []
        self.sum_hour_l = []
        self.trip_hour = []
        self.dive_per_hour = []
        self.sex = []
        self.label = []  #0: short, 1: long
        
        self.dive_sum_result = []
        self.sum_dives = []
        self.single_dives = []
        self.multi_dives = []
    
    #write feature file
    def write_txt(self, file_name):
        temp_file_name = file_name + '.txt'
        print (temp_file_name)
        
        f = open(temp_file_name, 'w+')
        for i in range(len(self.max_speed)):
            print (i, len(self.dis_se), len(self.sst), len(self.label), len(self.ptp_water_depth))
            
            temp_data = str(self.ptp_acceleration[i]) + ' ' + str(self.ptp_displacement[i]) + ' ' + str(self.ptp_speed[i]) + ' ' + str(self.ptp_fpt_100[i]) + ' ' + str(self.ptp_fpt_1000[i])\
            + ' ' + str(self.ptp_fpt_500[i]) + ' ' + str(self.ptp_fpt_5000[i]) + ' ' + \
                        str(self.max_acceleration[i]) + ' ' + str(self.max_displacement[i]) + ' ' + str(self.max_speed[i]) + ' ' + str(self.max_fpt_100[i]) + ' ' + str(self.max_fpt_1000[i])\
            + ' ' + str(self.max_fpt_500[i]) + ' ' + str(self.max_fpt_5000[i]) + ' ' + \
                        str(self.min_acceleration[i]) + ' ' + str(self.min_displacement[i]) + ' ' + str(self.min_speed[i]) + ' ' + str(self.min_fpt_100[i]) + ' ' + str(self.min_fpt_1000[i])\
            + ' ' + str(self.min_fpt_500[i]) + ' ' + str(self.min_fpt_5000[i]) + ' ' + \
                        str(self.avg_acceleration[i]) + ' ' + str(self.avg_displacement[i]) + ' ' + str(self.avg_speed[i]) + ' ' + str(self.avg_fpt_100[i]) + ' ' + str(self.avg_fpt_1000[i])\
            + ' ' + str(self.avg_fpt_500[i]) + ' ' + str(self.avg_fpt_5000[i]) + ' ' + \
                        str(self.median_acceleration[i]) + ' ' + str(self.median_displacement[i]) + ' ' + str(self.median_speed[i]) + ' ' + str(self.median_fpt_100[i]) + ' ' + str(self.median_fpt_1000[i])\
            + ' ' + str(self.median_fpt_500[i]) + ' ' + str(self.median_fpt_5000[i]) + ' ' + \
                        str(self.std_acceleration[i]) + ' ' + str(self.std_displacement[i]) + ' ' + str(self.std_speed[i]) + ' ' + str(self.std_fpt_100[i]) + ' ' + str(self.std_fpt_1000[i])\
            + ' ' + str(self.std_fpt_500[i]) + ' ' + str(self.std_fpt_5000[i]) + ' ' + \
                    str(self.ptp_water_depth[i]) + ' ' + str(self.max_water_depth[i]) + ' ' + str(self.min_water_depth[i]) + ' ' + str(self.avg_water_depth[i]) + ' ' + str(self.median_water_depth[i])\
            + ' ' + str(self.std_water_depth[i]) + ' ' + \
                        str(self.bird_ori_start2end[i]) + ' ' + str(self.bird_ori_avg[i]) + ' ' + str(self.bird_ori_std[i]) + ' ' + \
                        str(self.dis_se[i]) + ' ' + str(self.sst[i]) + ' ' + str(self.distant[i]) + ' ' + str(self.label[i]) + '\n' #str(self.bird_ori_start2end[i]) + ' ' + str(self.bird_ori_avg[i]) + ' ' + str(self.bird_ori_std[i]) + ' ' + \
            
            f.write(temp_data)
    
        f.close()    
    
    
    def write_xlsm_sum(self, file_name):
        f = xlwt.Workbook()
        sheet = f.add_sheet('test') #创建sheet
    
        #将数据写入第 i 行，第 j 列
        print (len(self.label), len(self.ptp_speed))
        sheet.write(0, 0, 'ptp_acceleration')
        sheet.write(0, 1, 'ptp_displacement') 
        sheet.write(0, 2, 'ptp_speed')
        sheet.write(0, 3, 'ptp_fpt_100') 
        sheet.write(0, 4, 'ptp_fpt_1000') 
        sheet.write(0, 5, 'ptp_fpt_500')
        sheet.write(0, 6, 'ptp_fpt_5000') 
        sheet.write(0, 7, 'max_acceleration')
        sheet.write(0, 8, 'max_displacement') 
        sheet.write(0, 9, 'max_speed') 
        sheet.write(0, 10, 'max_fpt_100') 
        sheet.write(0, 11, 'max_fpt_1000')
        sheet.write(0, 12, 'max_fpt_500')
        sheet.write(0, 13, 'max_fpt_5000') 
        
        sheet.write(0, 14, 'min_acceleration')     
        sheet.write(0, 15, 'min_displacement') 
        sheet.write(0, 16, 'min_speed') 
        sheet.write(0, 17, 'min_fpt_100') 
        sheet.write(0, 18, 'min_fpt_1000')
        sheet.write(0, 19, 'min_fpt_500') 
        sheet.write(0, 20, 'min_fpt_5000') 

        sheet.write(0, 21, 'avg_acceleration')    
        sheet.write(0, 22, 'avg_displacement')
        sheet.write(0, 23, 'avg_speed') 
        sheet.write(0, 24, 'avg_fpt_100') 
        sheet.write(0, 25, 'avg_fpt_1000')
        sheet.write(0, 26, 'avg_fpt_500') 
        sheet.write(0, 27, 'avg_fpt_5000') 

        sheet.write(0, 28, 'median_acceleration')    
        sheet.write(0, 29, 'median_displacement') 
        sheet.write(0, 30, 'median_speed') 
        sheet.write(0, 31, 'median_fpt_100') 
        sheet.write(0, 32, 'median_fpt_1000')
        sheet.write(0, 33, 'median_fpt_500') 
        sheet.write(0, 34, 'median_fpt_5000') 

        sheet.write(0, 35, 'std_acceleration') 
        sheet.write(0, 36, 'std_displacement') 
        sheet.write(0, 37, 'std_speed') 
        sheet.write(0, 38, 'std_fpt_100') 
        sheet.write(0, 39, 'std_fpt_1000')
        sheet.write(0, 40, 'std_fpt_500') 
        sheet.write(0, 41, 'std_fpt_5000') 

        sheet.write(0, 42, 'ori_s2e')
        sheet.write(0, 43, 'avg_ori') 
        sheet.write(0, 44, 'std_ori') 
        
        sheet.write(0, 45, 'dis_se')
        sheet.write(0, 46, 'sst')
        sheet.write(0, 47, 'distant')
        sheet.write(0, 48, 'label')
        sheet.write(0, 49, 'sex')
        
        sheet.write(0, 50, 'ptp_water_depth')
        sheet.write(0, 51, 'max_water_depth')
        sheet.write(0, 52, 'min_water_depth')
        sheet.write(0, 53, 'avg_water_depth')
        sheet.write(0, 54, 'median_water_depth')
        sheet.write(0, 55, 'std_water_depth')
        
        i = 1
        #for data in self.dive_per_hour:
        for j in range(len(self.ptp_speed)):
                #sheet.write(i, j, data[j])
            sheet.write(i, 0, str(self.ptp_acceleration[i-1]))     
            sheet.write(i, 1, str(self.ptp_displacement[i-1])) 
            sheet.write(i, 2, str(self.ptp_speed[i-1]))
            sheet.write(i, 3, str(self.ptp_fpt_100[i-1])) 
            sheet.write(i, 4, str(self.ptp_fpt_1000[i-1]))
            sheet.write(i, 5, str(self.ptp_fpt_500[i-1]))
            sheet.write(i, 6, str(self.ptp_fpt_5000[i-1])) 

            sheet.write(i, 7, self.max_acceleration[i-1]) 
            sheet.write(i, 8, self.max_displacement[i-1]) 
            sheet.write(i, 9, self.max_speed[i-1]) 
            sheet.write(i, 10, self.max_fpt_100[i-1]) 
            sheet.write(i, 11, self.max_fpt_1000[i-1])
            sheet.write(i, 12, self.max_fpt_500[i-1])
            sheet.write(i, 13, self.max_fpt_5000[i-1]) 

            sheet.write(i, 14, self.min_acceleration[i-1]) 
            sheet.write(i, 15, self.min_displacement[i-1]) 
            sheet.write(i, 16, self.min_speed[i-1]) 
            sheet.write(i, 17, self.min_fpt_100[i-1]) 
            sheet.write(i, 18, self.min_fpt_1000[i-1])
            sheet.write(i, 19, self.min_fpt_500[i-1]) 
            sheet.write(i, 20, self.min_fpt_5000[i-1]) 

            sheet.write(i, 21, self.avg_acceleration[i-1])
            sheet.write(i, 22, self.avg_displacement[i-1])
            sheet.write(i, 23, self.avg_speed[i-1]) 
            sheet.write(i, 24, self.avg_fpt_100[i-1]) 
            sheet.write(i, 25, self.avg_fpt_1000[i-1])
            sheet.write(i, 26, self.avg_fpt_500[i-1]) 
            sheet.write(i, 27, self.avg_fpt_5000[i-1]) 

            sheet.write(i, 28, self.median_acceleration[i-1]) 
            sheet.write(i, 29, self.median_displacement[i-1]) 
            sheet.write(i, 30, self.median_speed[i-1]) 
            sheet.write(i, 31, self.median_fpt_100[i-1]) 
            sheet.write(i, 32, self.median_fpt_1000[i-1])
            sheet.write(i, 33, self.median_fpt_500[i-1]) 
            sheet.write(i, 34, self.median_fpt_5000[i-1]) 

            sheet.write(i, 35, self.std_acceleration[i-1]) 
            sheet.write(i, 36, self.std_displacement[i-1]) 
            sheet.write(i, 37, self.std_speed[i-1]) 
            sheet.write(i, 38, self.std_fpt_100[i-1]) 
            sheet.write(i, 39, self.std_fpt_1000[i-1])
            sheet.write(i, 40, self.std_fpt_500[i-1]) 
            sheet.write(i, 41, self.std_fpt_5000[i-1]) 

            sheet.write(i, 42, self.bird_ori_start2end[i-1])
            sheet.write(i, 43, self.bird_ori_avg[i-1])
            sheet.write(i, 44, self.bird_ori_std[i-1])
            
            sheet.write(i, 45, self.dis_se[i-1])
            sheet.write(i, 46, str(self.sst[i-1]))
            sheet.write(i, 47, str(self.distant[i-1]))
            sheet.write(i, 48, self.label[i-1])
            sheet.write(i, 49, self.sex[i-1])
            
            sheet.write(i, 50, self.ptp_water_depth[i-1])
            sheet.write(i, 51, self.max_water_depth[i-1])
            sheet.write(i, 52, self.min_water_depth[i-1])
            sheet.write(i, 53, self.avg_water_depth[i-1])
            sheet.write(i, 54, self.median_water_depth[i-1])
            sheet.write(i, 55, self.std_water_depth[i-1])
            
            i = i + 1
        
        f.save(file_name + '.xls') #保存文件
    
        
FPT_radius = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

trip_start_de = 0
trip_hour_define = 5

awa_lon = 139.2403165
awa_lat = 38.463616


t_sum = E_features()   #features in trips
            
long_t = []
short_t = []

def main(): 
    
    depth_file_2016_names = read_file_in_folder(bird_depth_2016_path)
    depth_file_2017_names = read_file_in_folder(bird_depth_2017_path)
    depth_file_2018_names = read_file_in_folder(bird_depth_2018_path)
    
    GPS_file_2016_names = read_file_in_folder(bird_GPS_2016_path)
    GPS_file_2017_names = read_file_in_folder(bird_GPS_2017_path)
    GPS_file_2018_names = read_file_in_folder(bird_GPS_2018_path)
    
    depth_files = [depth_file_2016_names, depth_file_2017_names, depth_file_2018_names]
    GPS_files = [GPS_file_2016_names, GPS_file_2017_names, GPS_file_2018_names]
    
    #
    for i in range(len(depth_files)):
        for j in range(0, len(depth_files[i])):
            Trip_time = Read_Data.Read_bird_trip(GPS_files[i][j], 0, 99)
            GPS_Lon = Read_Data.Read_bird_trip(GPS_files[i][j], 5, 0)
            GPS_Lat = Read_Data.Read_bird_trip(GPS_files[i][j], 6, 0)
            water_depth_trip = read_depth_trip_txt(depth_files[i][j])
                        
            bird_trip_define_label(Trip_time, GPS_Lon, GPS_Lat, trip_day_define, trip_hour_define, index_sex, sst_data, trip_index)
            bird_trip_number_of_dives_hour(Trip_time, trip_day_define, trip_hour_define, index_sex, water_depth_data)
            
    
        
    t_sum.write_xlsm_sum('features_' + str(trip_start_de) + '-' + str(trip_hour_define))
    
    
    print ('fin')


# read file names in a folder
def read_file_in_folder(folder_path):
    file_name = os.listdir(folder_path)
    file_names = []
    for filename in file_name:
        file_names.append(os.path.join(folder_path, filename))

    return file_names



#calculate water depth difference for a bird, water depth: []
def water_depth_difference(water_depth):
    #bird trip
    for i in range(len(water_depth)):
        water_depth_difference_trip(water_depth[i])
    
    return water_depth


#calculate difference of water depth in a trip 2017, 25Hz, 2018 1Hz
def water_depth_difference_trip(water_depth):
    for i in range(len(water_depth)-1):
        water_depth[len(water_depth)-i-1][1] = water_depth[len(water_depth)-i-1][1] - water_depth[len(water_depth)-i-2][1]
    
    water_depth[0][1] = 0
    
    return 0


# return a list of the start time index of a single dive
def dive_start_index(water_difference):
    dive_start_time_index_temp = []
    i = 0
    
    while (i < len(water_difference)):
        if water_difference[i] >= 2.0:
            n = bird_single_dive_cal(i, water_difference)
            #print n
            if n != -1:
                #start dive i, end dive n
                dive_start_time_index_temp.append(i-1) #can not be 0
                #depth_time_num.append(n)
                i = n    
        
        i += 1
    
    return dive_start_time_index_temp


#find a dive, sampling rate: 1Hz 
def bird_single_dive_cal(start_point, water_difference):
    sum_diff = 0.0
    sum_diff += water_difference[start_point]
    j = 0
    #k = 0
    for i in range(1,31): # duration of a dive < 30s
        #calculate diff of depth
        if start_point + i >= len(water_difference):
            return -1
        sum_diff += water_difference[start_point + i]
        
        if sum_diff <= 0.0:
            return -1
        if sum_diff >= 5.0:
            j = i
            break
        
    if sum_diff < 5.0:
        return -1
    
    k = start_point + j + 1
    k0 = k
    while (sum_diff > 0.3):
        if k >= len(water_difference) or k - k0 > 30:
            return -1
        
        sum_diff += water_difference[k]
        #print k, sum_diff
        k += 1
            
    return k-1


#read depth trip files
def read_depth_trip_txt(file_name): #0: trip no. 1: datetime, 2: depth
    temp = []
    
    f = open(file_name)
    lines = f.readlines()
    #print (lines[-1].split('\n')[0]).split(' ')[0]
    num_trip = int((lines[-1].split('\n')[0]).split(' ')[0])
    
    #print num_trip, len(lines)
    
    for i in range(num_trip):
        temp.append([])

    for line in lines:
        line_temp = line.split('\n')[0] #date time depth
        line_temp_0 = line_temp.split(' ') # ['date', 'time', 'depth']
        
        number_temp = int(line_temp_0[0]) - 1
        temp_time = line_temp_0[1] + ' ' + line_temp_0[2]
        temp_date_time = datetime.strptime(temp_time, "%Y-%m-%d %H:%M:%S.%f")  + timedelta(seconds = int(3600 * 9))
        temp_depth = float(line_temp_0[3])
        #print line, type(line)
        temp[number_temp].append([temp_date_time, temp_depth])
    
    f.close()
    
    return np.array(temp)


#calculate speed from GPS data
def bird_speed_computation(GPS_Lon, GPS_Lat, GPS_time, is_acc = 0, window_size = 0): #time, GPS: lon, lat
    temp = []
    
    for i in range(len(GPS_time)):
        speed_trip_temp = bird_speed_trip_computation(GPS_Lon[i], GPS_Lat[i], GPS_time[i], is_acc, window_size)
        temp.extend(speed_trip_temp)
        
    return temp


#calculate bird speed per trip
def bird_speed_trip_computation(GPS_Lon, GPS_Lat, GPS_Time, is_acc = 0, window_size = 0):
    temp = []
    
    for i in range(len(GPS_Time)-1):
        speed_temp = speed_computation(GPS_Lon[i], GPS_Lat[i], GPS_Lon[i+1], GPS_Lat[i+1], GPS_Time[i], GPS_Time[i+1])
        
        if i == 0:
            temp.append(speed_temp)
        
        temp.append(speed_temp)
    
    if is_acc == 1: #acceleration
        temp = acceleration_cpmputation(temp, GPS_Time) 
    
    return temp 


#calculate speed (A->B)
def speed_computation(GPS_Lon_A, GPS_Lat_A, GPS_Lon_B, GPS_Lat_B, Time_A, Time_B):#GPS: Lon, Lat
    dis = Calculate_angle_speed.Cal_GPS_to_dis(GPS_Lon_A, GPS_Lat_A, GPS_Lon_B, GPS_Lat_B)    
    speed = dis / (Time_B - Time_A).seconds

    return speed

#calculate angle from 2 vectors, mv_0 -> mv_1
def single_angle_ori(mv_0, mv_1):
    x_0 = np.array(mv_0, dtype=np.float)
    x_1 = np.array(mv_1, dtype=np.float)
    Lx1 = np.sqrt(x_0.dot(x_0))
    Lx2 = np.sqrt(x_1.dot(x_1))
    
    if Lx1 * Lx2 == 0 :
        if Lx1 == 0.0:#停止
            return 0
        else:
            #print (Lx1,Lx2, mv_0, mv_1)
            return 0
    
    cos_ang = x_0.dot(x_1) / round((Lx1 * Lx2), 5)
    cos_ang = round(cos_ang, 4)
    
    if np.isnan(np.arccos(cos_ang)):
        angle = 0
    else:
        angle = round(np.arccos(cos_ang), 4) * sign_angle(x_0, x_1)
    
    return angle

# calculate sign of angle, p1 -> p2, 顺时针 +， 逆时针 -
def sign_angle(p1, p2):
    sign = np.cross(p1, p2)
    if sign >= 0 :
        sign = 1
    else:
        sign = -1
    
    return sign


#calculate acceleration
def acceleration_cpmputation(speed, GPS_time):
    temp = [0]
    
    for i in range(len(speed)-1):
        acc_temp = (speed[i+1] - speed[i]) / (GPS_time[i+1] - GPS_time[i]).seconds
        temp.append(acc_temp)
    
    return temp


#displacement per bird
def displace_distance(GPS_Lon, GPS_Lat, window_size):
    temp = []
    
    for i in range(len(GPS_Lon)):
        temp_displacement = displace_distance_trip(GPS_Lon[i], GPS_Lat[i], window_size)
        temp.extend(temp_displacement)
    
    return temp


#displacement distant per trip
def displace_distance_trip(GPS_Lon, GPS_Lat, win_size):
    displace = []
    j = 0
    
    for i in range(len(GPS_Lon) - win_size):
        temp = Calculate_angle_speed.Cal_GPS_to_dis(GPS_Lon[i], GPS_Lat[i], GPS_Lon[i+win_size], GPS_Lat[i+win_size])
        displace.append(temp)
    
    for i in range(win_size):
        temp = Calculate_angle_speed.Cal_GPS_to_dis(GPS_Lon[len(GPS_Lon) - win_size + i], GPS_Lat[len(GPS_Lat) - win_size + i], GPS_Lon[-1], GPS_Lat[-1])
        displace.append(temp)
    
    return displace




#find long or short trip, judge days > n(t_day) days, extract feature, first m (t_hour) hours and give label
#label: long trip: 1, short trip: 0
#extracted features: max speed, average speed, acceleration, displacement
def bird_trip_define_label(Trip_time, GPS_Lon, GPS_Lat, t_day, t_hour, index_sex, sst_data, water_depth_data, trip_index):
    for i in range(len(Trip_time)):#each trip
        print (len(Trip_time), i)
        t_start = Trip_time[i][0]
        t_end = Trip_time[i][-1]
        Trip_time_temp = np.array(Trip_time[i])
        sst_data[i] = np.array(sst_data[i])
        water_depth_data[i] = np.array(water_depth_data[i])
        
        t_duration = (t_end - t_start).days
        t_days = t_day * 24
        t_hours = (t_end - t_start).days * 24 + ((t_end - t_start).seconds / 3600)

        if t_hours > t_hour: #the sum duration is larger than the first m hours
            #extract features
            time_delta = timedelta(seconds = int(3600 * t_hour))
            speed_temp = bird_speed_trip_computation(GPS_Lon[i], GPS_Lat[i], Trip_time[i])
            acceleration_temp = bird_speed_computation(GPS_Lon[i], GPS_Lat[i], Trip_time[i], 1)
            bird_ori = seabird_orientation(GPS_Lon[i], GPS_Lat[i])
            sst_time = sst_data[i][:,0]
            sst_temperature = sst_data[i][:,1]
            
            water_depth_time = water_depth_data[i][:,0]
            water_depth= water_depth_data[i][:,1]
            
            start_time = Trip_time[i][0] + timedelta(seconds = int(3600 * trip_start_de))
            start_time = datetime(start_time.year, start_time.month, start_time.day, start_time.hour, start_time.minute, 59, 000)
            end_time = Trip_time[i][0] + time_delta
            end_time = datetime(end_time.year, end_time.month, end_time.day, end_time.hour, end_time.minute, 10, 000)
            
            if len(np.where(Trip_time_temp == start_time)[0]) == 0:
                start_time = Trip_time[i][0] + timedelta(seconds = int(3600 * trip_start_de))
                while (len(np.where(Trip_time_temp == start_time)[0]) == 0):  # and end_time <= end_time_end
                    start_time -= timedelta(seconds = 1)
                
                print ('a', start_time, Trip_time[i][0] + time_delta)
                
            
            if len(np.where(Trip_time_temp == end_time)[0]) == 0:
                end_time = Trip_time[i][0] + time_delta
                while (len(np.where(Trip_time_temp == end_time)[0]) == 0):  # and end_time <= end_time_end
                    end_time += timedelta(seconds = 1)
                print ('a', end_time, Trip_time[i][0] + time_delta)
                
            
            start_index = np.where(Trip_time_temp == start_time)[0][0]
            end_index = np.where(Trip_time_temp == end_time)[0][0]
            
            
            
            if (end_index-start_index) == 0:
                end_index+=1
                start_index-=1
                
            
            if len(np.where(water_depth_time == Trip_time[i][0] + timedelta(seconds = int(3600 * trip_start_de)))[0]) == 0:
                start_time = Trip_time[i][0] + timedelta(seconds = int(3600 * trip_start_de))
                while (len(np.where(Trip_time_temp == start_time)[0]) == 0):  # and end_time <= end_time_end
                    start_time -= timedelta(seconds = 1)
            
            
            water_depth_start_index = np.where(water_depth_time == start_time)[0][0]
            
            if len(np.where(water_depth_time == Trip_time[i][0] + time_delta)[0]) == 0:
                end_time = Trip_time[i][0] + time_delta
                while (len(np.where(Trip_time_temp == end_time)[0]) == 0):  # and end_time <= end_time_end
                    end_time += timedelta(seconds = 1)
                    
            
            water_depth_end_index = np.where(water_depth_time == end_time)[0][0]
            water_depth_temp = water_depth[water_depth_start_index: water_depth_end_index+1]
                
            fpt_temp_100 = FPT_R.py_2_R_return_appoint(GPS_Lon[i][start_index: end_index+1], GPS_Lat[i][start_index: end_index+1], Trip_time[i][start_index: end_index+1], 100, t_hour-trip_start_de)
            fpt_temp_1000 = FPT_R.py_2_R_return_appoint(GPS_Lon[i][start_index: end_index+1], GPS_Lat[i][start_index: end_index+1], Trip_time[i][start_index: end_index+1], 1000, t_hour-trip_start_de)
            fpt_temp_10000 = FPT_R.py_2_R_return_appoint(GPS_Lon[i][start_index: end_index+1], GPS_Lat[i][start_index: end_index+1], Trip_time[i][start_index: end_index+1], 10000, t_hour-trip_start_de)
            fpt_temp_500 = FPT_R.py_2_R_return_appoint(GPS_Lon[i][start_index: end_index+1], GPS_Lat[i][start_index: end_index+1], Trip_time[i][start_index: end_index+1], 500, t_hour-trip_start_de)
            fpt_temp_5000 = FPT_R.py_2_R_return_appoint(GPS_Lon[i][start_index: end_index+1], GPS_Lat[i][start_index: end_index+1], Trip_time[i][start_index: end_index+1], 5000, t_hour-trip_start_de)
            fpt_temp_50000 = FPT_R.py_2_R_return_appoint(GPS_Lon[i][start_index: end_index+1], GPS_Lat[i][start_index: end_index+1], Trip_time[i][start_index: end_index+1], 50000, t_hour-trip_start_de)
            
            if (GPS_Lat[i][start_index] == GPS_Lat[i][end_index]):
                bird_ori_start2end_temp = [0]
            elif (GPS_Lon[i][start_index] == GPS_Lon[i][end_index]):
                bird_ori_start2end_temp = [math.pi/2]
            else:
                bird_ori_start2end_temp = seabird_orientation([GPS_Lon[i][start_index], GPS_Lon[i][end_index]], [GPS_Lat[i][start_index], GPS_Lat[i][end_index]])
            
            #displacement between start point and end point
            dis_se_temp = Calculate_angle_speed.Cal_GPS_to_dis(GPS_Lon[i][start_index], GPS_Lat[i][start_index], GPS_Lon[i][end_index], GPS_Lat[i][end_index])
            distant_sum_temp = bird_distant(GPS_Lon[i], GPS_Lat[i], start_index, end_index+1)
            
            displacement_temp = bird_displacement_aj(GPS_Lon[i], GPS_Lat[i], start_index, end_index+1)
            
            max_displacement_temp = max(displacement_temp)
            min_displacement_temp = min(displacement_temp)
            avg_displacement_temp = np.mean(displacement_temp)
            median_displacement_temp = np.median(displacement_temp)
            std_displacement_temp = np.std(displacement_temp, ddof = 1)
            ptp_displacement_temp = np.ptp(displacement_temp)
            
            if np.isnan(np.std(displacement_temp, ddof = 1)):
                cv_displacement_temp = np.std(displacement_temp, ddof = 0) / avg_displacement_temp
            
            max_speed_temp = max(speed_temp[start_index: end_index+1])
            min_speed_temp = min(speed_temp[start_index: end_index+1])
            avg_speed_temp = np.mean(speed_temp[start_index: end_index+1])
            median_speed_temp = np.median(speed_temp[start_index: end_index+1])
            std_speed_temp = np.std(speed_temp[start_index: end_index+1], ddof = 1)
            ptp_speed_temp = np.ptp(speed_temp[start_index: end_index+1])
            
            
            max_acceleration_temp = max(acceleration_temp[start_index: end_index+1])
            min_acceleration_temp = min(acceleration_temp[start_index: end_index+1])
            avg_acceleration_temp = np.mean(acceleration_temp[start_index: end_index+1])
            median_acceleration_temp = np.median(acceleration_temp[start_index: end_index+1])
            std_acceleration_temp = np.std(acceleration_temp[start_index: end_index+1], ddof = 1)
            ptp_acceleration_temp = np.ptp(acceleration_temp[start_index: end_index+1])
           
            
            if len(fpt_temp_100) == 0: 
                fpt_temp_100 = [np.nan]
                continue

            max_fpt_temp_100 = max(fpt_temp_100)
            min_fpt_temp_100 = min(fpt_temp_100)
            avg_fpt_temp_100 = np.mean(fpt_temp_100)
            median_fpt_temp_100 = np.median(fpt_temp_100)
            std_fpt_temp_100 = np.std(fpt_temp_100)
            ptp_fpt_temp_100 = np.ptp(fpt_temp_100)
              
          
            if len(fpt_temp_500) == 0: 
                fpt_temp_500 = [np.nan]
                continue
            
            max_fpt_temp_500 = max(fpt_temp_500)
            min_fpt_temp_500 = min(fpt_temp_500)
            avg_fpt_temp_500 = np.mean(fpt_temp_500)
            median_fpt_temp_500 = np.median(fpt_temp_500)
            std_fpt_temp_500 = np.std(fpt_temp_500, ddof = 1)
            ptp_fpt_temp_500 = np.ptp(fpt_temp_500)
            
            if len(fpt_temp_1000) == 0:
                fpt_temp_1000 = [np.nan]
                continue
            
            max_fpt_temp_1000 = max(fpt_temp_1000)
            min_fpt_temp_1000 = min(fpt_temp_1000)
            avg_fpt_temp_1000 = np.mean(fpt_temp_1000)
            median_fpt_temp_1000 = np.median(fpt_temp_1000)
            std_fpt_temp_1000 = np.std(fpt_temp_1000, ddof = 1)
            ptp_fpt_temp_1000 = np.ptp(fpt_temp_1000)
            
            if len(fpt_temp_5000) == 0:
                fpt_temp_5000 = [np.nan]
                continue
            
            max_fpt_temp_5000 = max(fpt_temp_5000)
            min_fpt_temp_5000 = min(fpt_temp_5000)
            avg_fpt_temp_5000 = np.mean(fpt_temp_5000)
            median_fpt_temp_5000 = np.median(fpt_temp_5000)
            std_fpt_temp_5000 = np.std(fpt_temp_5000, ddof = 1)
            ptp_fpt_temp_5000 = np.ptp(fpt_temp_5000)
            
            if len(fpt_temp_10000) == 0:
                fpt_temp_10000 = [np.nan]
                continue
            
            max_fpt_temp_10000 = max(fpt_temp_10000)
            min_fpt_temp_10000 = min(fpt_temp_10000)
            avg_fpt_temp_10000 = np.mean(fpt_temp_10000)
            median_fpt_temp_10000 = np.median(fpt_temp_10000)
            std_fpt_temp_10000 = np.std(fpt_temp_10000, ddof = 1)
            ptp_fpt_temp_10000 = np.ptp(fpt_temp_10000)
            
            if len(fpt_temp_50000) == 0:
                fpt_temp_50000 = [np.nan]
                continue
            
            max_fpt_temp_50000 = max(fpt_temp_50000)
            min_fpt_temp_50000 = min(fpt_temp_50000)
            avg_fpt_temp_50000 = np.mean(fpt_temp_50000)
            median_fpt_temp_50000 = np.median(fpt_temp_50000)
            std_fpt_temp_50000 = np.std(fpt_temp_5000, ddof = 1)
            ptp_fpt_temp_50000 = np.ptp(fpt_temp_50000)
            
            avg_bird_ori = np.mean(bird_ori[start_index: end_index+1])
            std_bird_ori = np.std(bird_ori[start_index: end_index+1], ddof = 1)
            
            
            t_sum.avg_speed.append(avg_speed_temp)
            t_sum.min_speed.append(min_speed_temp)
            t_sum.max_speed.append(max_speed_temp)
            t_sum.median_speed.append(median_speed_temp)
            t_sum.std_speed.append(std_speed_temp)
            t_sum.ptp_speed.append(ptp_speed_temp)

            t_sum.avg_acceleration.append(avg_acceleration_temp)
            t_sum.min_acceleration.append(min_acceleration_temp)
            t_sum.max_acceleration.append(max_acceleration_temp)
            t_sum.median_acceleration.append(median_acceleration_temp)
            t_sum.std_acceleration.append(std_acceleration_temp)
            t_sum.ptp_acceleration.append(ptp_acceleration_temp)

            t_sum.avg_displacement.append(avg_displacement_temp)
            t_sum.min_displacement.append(min_displacement_temp)
            t_sum.max_displacement.append(max_displacement_temp)
            t_sum.median_displacement.append(median_displacement_temp)
            t_sum.std_displacement.append(std_displacement_temp)
            t_sum.ptp_displacement.append(ptp_displacement_temp)
            
            t_sum.max_fpt_100.append(max_fpt_temp_100)
            t_sum.min_fpt_100.append(min_fpt_temp_100)
            t_sum.avg_fpt_100.append(avg_fpt_temp_100)
            t_sum.median_fpt_100.append(median_fpt_temp_100)
            t_sum.std_fpt_100.append(std_fpt_temp_100)
            t_sum.ptp_fpt_100.append(ptp_fpt_temp_100)
            
            t_sum.max_fpt_1000.append(max_fpt_temp_1000)
            t_sum.min_fpt_1000.append(min_fpt_temp_1000)
            t_sum.avg_fpt_1000.append(avg_fpt_temp_1000)
            t_sum.median_fpt_1000.append(median_fpt_temp_1000)
            t_sum.std_fpt_1000.append(std_fpt_temp_1000)
            t_sum.ptp_fpt_1000.append(ptp_fpt_temp_1000)
            
            t_sum.max_fpt_10000.append(max_fpt_temp_10000)
            t_sum.min_fpt_10000.append(min_fpt_temp_10000)
            t_sum.avg_fpt_10000.append(avg_fpt_temp_10000)
            t_sum.median_fpt_10000.append(median_fpt_temp_10000)
            t_sum.std_fpt_10000.append(std_fpt_temp_10000)
            t_sum.ptp_fpt_10000.append(ptp_fpt_temp_10000)
            
            t_sum.max_fpt_500.append(max_fpt_temp_500)
            t_sum.min_fpt_500.append(min_fpt_temp_500)
            t_sum.avg_fpt_500.append(avg_fpt_temp_500)
            t_sum.median_fpt_500.append(median_fpt_temp_500)
            t_sum.std_fpt_500.append(std_fpt_temp_500)
            t_sum.ptp_fpt_500.append(ptp_fpt_temp_500)
            
            t_sum.max_fpt_5000.append(max_fpt_temp_5000)
            t_sum.min_fpt_5000.append(min_fpt_temp_5000)
            t_sum.avg_fpt_5000.append(avg_fpt_temp_5000)
            t_sum.median_fpt_5000.append(median_fpt_temp_5000)
            t_sum.std_fpt_5000.append(std_fpt_temp_5000)
            t_sum.ptp_fpt_5000.append(ptp_fpt_temp_5000)
            
            t_sum.max_fpt_50000.append(max_fpt_temp_50000)
            t_sum.min_fpt_50000.append(min_fpt_temp_50000)
            t_sum.avg_fpt_50000.append(avg_fpt_temp_50000)
            t_sum.median_fpt_50000.append(median_fpt_temp_50000)
            t_sum.std_fpt_50000.append(std_fpt_temp_50000)
            t_sum.ptp_fpt_50000.append(ptp_fpt_temp_50000)
                      
            t_sum.bird_ori_start2end.append(bird_ori_start2end_temp[0])
            t_sum.bird_ori_avg.append(0)         
            t_sum.bird_ori_std.append(0)               
            
            t_sum.sst.append(average_sst)
            t_sum.dis_se.append(dis_se_temp)                              
            t_sum.distant.append(distant_sum_temp)
            t_sum.trip_hour.append(t_hours)
            t_sum.start_time.append(t_start.hour)
            t_sum.sex.append(index_sex)
                    
            #distinguish long and short trip and draw
            if t_hours > t_days: #long trip
                t_sum.label.append(1)
                t_sum.sum_hour_l.append(t_hours)
            
            else:   #short trip
                t_sum.label.append(0)
                t_sum.sum_hour_s.append(t_hours)
                
    return 0



def bird_displacement_aj(GPS_Lon, GPS_Lat, start_index, end_index):
    displace = []
    
    for i in range(start_index, end_index-1):
            temp = Calculate_angle_speed.Cal_GPS_to_dis(GPS_Lon[start_index], GPS_Lat[start_index], GPS_Lon[i+1], GPS_Lat[i+1])
            displace.append(temp)

    return displace


def bird_distant(GPS_Lon, GPS_Lat, start_index, end_index):
    distant_temp = 0
    
    for i in range(start_index, end_index-1):
        distant_temp += Calculate_angle_speed.Cal_GPS_to_dis(GPS_Lon[i], GPS_Lat[i], GPS_Lon[i+1], GPS_Lat[i+1])
    
    return distant_temp


#calculate the orientation of sea birds (v, [1,0](lat))
def seabird_orientation(GPS_Lon, GPS_Lat):
    lat_vec = [1, 0]
    bird_ori = []
    #project GPS to map
    ax1 = Basemap(llcrnrlon = min(GPS_Lon), llcrnrlat = min(GPS_Lat), urcrnrlon = max(GPS_Lon), urcrnrlat = max(GPS_Lat),
                           projection = 'merc', resolution = 'f')
     
    x, y = ax1(GPS_Lon, GPS_Lat)
    
    for i in range(len(x)-1):
        move_vec = [abs(x[i+1] - x[i]), y[i+1] - y[i]]
        move_vec = preprocessing.normalize(np.array(move_vec).reshape(1,-1))[0].tolist()
        ori_temp = single_angle_ori(lat_vec, move_vec)
        bird_ori.append(ori_temp)

    return bird_ori


# calculate number of dives in i to j hour
def bird_trip_number_of_dives_hour(Trip_time, GPS_Lon, GPS_Lat, t_day, t_hour, index_sex, water_difference):
    for i in range(len(Trip_time)):#each trip
        t_start = Trip_time[i][0]
        t_end = Trip_time[i][-1]
        
        water_difference_temp = np.array(water_difference[i])
        water_depth_difference_trip(water_difference_temp)
        
        depth_time_temp = water_difference_temp[:, 0]
        depth_data_temp = water_difference_temp[:, 1]
        
        t_duration = (t_end - t_start).days
        t_days = t_day * 24
        t_hours = (t_end - t_start).days * 24 + ((t_end - t_start).seconds / 3600)
        #print t_hours
        if t_hours >= 7.5: #the sum duration is larger than the first m hours
            #extract features
            time_delta = timedelta(seconds = int(3600 * t_hour))
            
            start_time = Trip_time[i][0] + timedelta(seconds = int(3600 * trip_start_de))
            start_time = datetime(start_time.year, start_time.month, start_time.day, start_time.hour, start_time.minute, 00, 000)
            end_time = Trip_time[i][0] + time_delta
            end_time = datetime(end_time.year, end_time.month, end_time.day, end_time.hour, end_time.minute, 59, 000)

            
            #find range of depth time
            while (len(np.where(depth_time_temp == start_time)[0]) == 0):  # and end_time <= end_time_end
                start_time += timedelta(seconds = 1)
                if (start_time >= Trip_time[i][0] + time_delta):
                    return 0
            
            if len(np.where(depth_time_temp == start_time)[0]) == 0:
                print ('a', start_time, Trip_time[i][0] + time_delta)
                
            
            while (len(np.where(depth_time_temp == end_time)[0]) == 0):  # and end_time <= end_time_end
                end_time -= timedelta(seconds = 1)
                if (end_time <= Trip_time[i][0] + timedelta(seconds = int(3600 * trip_start_de))):
                    return 0
            
            if len(np.where(depth_time_temp == end_time)[0]) == 0:
                print ('a', end_time, Trip_time[i][0] + time_delta)
                break
            
            depth_start_index = np.where(depth_time_temp == start_time)[0][0]
            depth_end_index = np.where(depth_time_temp == end_time)[0][0]
            
            
            dive_start_time_index = dive_start_index(depth_data_temp)
            
            single_dive, multi_dive = detect_dive_type(dive_start_time_index, depth_time_temp)
            number_dive = [i for i in dive_start_time_index if i >= depth_start_index and i <=depth_end_index]
            number_dive_single = [i for i in single_dive if i >= depth_start_index and i <=depth_end_index]
            number_dive_multi = [i for i in multi_dive if i >= depth_start_index and i <=depth_end_index]
            
            
            
            if len(number_dive) == 0:
                number_dives = 0
            else:
                number_dives = len(number_dive)
            
            if len(number_dive_single) == 0:
                number_dives_single = 0
            else:
                number_dives_single = len(number_dive_single)
            
            if len(number_dive_multi) == 0:
                number_dives_multi = 0
            else:
                number_dives_multi = len(number_dive_multi)
            
            t_sum.trip_hour.append(t_hours)
            t_sum.start_time.append(t_start.hour)
            t_sum.sex.append(index_sex)
            t_sum.sum_dives.append(number_dives)
            t_sum.single_dives.append(number_dives_single)
            t_sum.multi_dives.append(number_dives_multi)

            if t_hours > t_days: #long trip
                t_sum.label.append(1)
                t_sum.sum_hour_l.append(t_hours)
            else:   #short trip
                t_sum.label.append(0)
                t_sum.sum_hour_s.append(t_hours)
    return 0

#detect single dive and multiple dive
def detect_dive_type(dive_index, depth_time):
    single_dive = []
    multi_dive = []
    
    if len(dive_index) == 0:
        return single_dive, multi_dive
    if len(dive_index) == 1:
        single_dive.append(dive_index[0])
        return single_dive, multi_dive
    
    dive_num_temp = [dive_index[0]]
    for i in range(len(dive_index)-1):
        time_diff = (depth_time[dive_index[i+1]] - depth_time[dive_index[i]]).seconds
        #print (dive_index[i], dive_index[i+1], time_diff, dive_num_temp)
        if time_diff <= 300:
            dive_num_temp.append(dive_index[i+1])
        else:
            if len(dive_num_temp) == 1:
                single_dive.append(dive_num_temp[0])
            else:
                multi_dive.append(dive_num_temp[0])
            dive_num_temp = [dive_index[i+1]]
    
    return single_dive, multi_dive

if __name__=="__main__":
    main()
    
    
    
