# -*- coding: utf-8 -*-
'''
Created on 2017��10��8��

@author: Tian
'''

from __future__ import division
import numpy as np
from math import *
from pyproj import Proj, transform

def Cal_speed(Lon, Lat, times):
    bird_speed = []
    
    for i in range(len(Lat)):
        if (i == 0) or ((times[i] - times[i-1]).seconds > 200 and i < len(Lat) - 1):
            dis_temp = Cal_GPS_to_dis(Lon[i], Lat[i], Lon[i+1], Lat[i+1])
            temp_speed = dis_temp / (times[i+1] - times[i]).seconds
        elif (i == len(Lat) - 1) or ((times[i+1] - times[i]).seconds > 200 and i > 0):
            dis_temp = Cal_GPS_to_dis(Lon[i-1], Lat[i-1], Lon[i], Lat[i])
            temp_speed = dis_temp / (times[i] - times[i-1]).seconds
        elif i < len(Lon) - 1:
            dis_temp = Cal_GPS_to_dis(Lon[i-1], Lat[i-1], Lon[i], Lat[i]) + \
            Cal_GPS_to_dis(Lon[i], Lat[i], Lon[i+1], Lat[i+1])
            temp_speed = dis_temp / (times[i+1] - times[i-1]).seconds
            #temp_speed = (temp_speed_ave * (times[i+1] - times[i]).seconds / (times[i] - times[i-1]).seconds)
        
        #print dis_temp
        if temp_speed > 100:
            print (dis_temp, times[i])
        bird_speed.append(temp_speed)
    
    return bird_speed
            
def Cal_angle(Lon, Lat, times):
    bird_angle = []
    bird_angle.append(0)
    #change gps to xy
    x, y = proj_tran(Lon, Lat)
    
    bird_mv = [[x[i + 1] - x[i], y[i + 1] - y[i]]for i in range(len(x) - 1)]
    
    for i in range(len(bird_mv) - 1):
        if bird_mv[i] == [0.0, 0.0]:
            bird_angle.append(single_angle(bird_mv[i+1], bird_mv[i-1]))
        elif bird_mv[i+1] == [0.0, 0.0]:
            bird_angle.append(0.0)
        else:
            bird_angle.append(single_angle(bird_mv[i+1], bird_mv[i]))
    
    bird_angle.append(0)
    
    return bird_angle

def Cal_anglespeed(bird_angle, times):
    bird_anglespeed = []
    
    for i in range(len(bird_angle)):
        if (i == 0) or ((times[i] - times[i-1]).seconds > 200 and i < len(bird_angle) - 1):
            #dis_temp = Cal_GPS_to_dis(Lon[i], Lat[i], Lon[i+1], Lat[i+1])
            temp_speed = (bird_angle[i+1] - bird_angle[i]) / (times[i+1] - times[i]).seconds
        elif (i == len(bird_angle) - 1) or ((times[i+1] - times[i]).seconds > 200 and i > 0):
            #dis_temp = Cal_GPS_to_dis(Lon[i-1], Lat[i-1], Lon[i], Lat[i])
            temp_speed = (bird_angle[i] - bird_angle[i-1]) / (times[i] - times[i-1]).seconds
        elif i < len(bird_angle) - 1:
            #dis_temp = Cal_GPS_to_dis(Lon[i-1], Lat[i-1], Lon[i], Lat[i]) + \
            #Cal_GPS_to_dis(Lon[i], Lat[i], Lon[i+1], Lat[i+1])
            temp_speed = (bird_angle[i+1] - bird_angle[i-1]) / (times[i+1] - times[i-1]).seconds
            #temp_speed = (temp_speed_ave * (times[i+1] - times[i]).seconds / (times[i] - times[i-1]).seconds)
        
        if temp_speed > 100:
            print (temp_speed, times[i])
        bird_anglespeed.append(temp_speed)
    
    return bird_anglespeed

def Cal_accelerate(bird_angle, times):
    bird_acc = []
    
    for i in range(len(bird_angle)):
        if (i == 0) or ((times[i] - times[i-1]).seconds > 200 and i < len(bird_angle) - 1):
            #dis_temp = Cal_GPS_to_dis(Lon[i], Lat[i], Lon[i+1], Lat[i+1])
            temp_speed = (bird_angle[i+1] - bird_angle[i]) / ((times[i+1] - times[i]).seconds / 60)
        elif (i == len(bird_angle) - 1) or ((times[i+1] - times[i]).seconds > 200 and i > 0):
            #dis_temp = Cal_GPS_to_dis(Lon[i-1], Lat[i-1], Lon[i], Lat[i])
            temp_speed = (bird_angle[i] - bird_angle[i-1]) / ((times[i] - times[i-1]).seconds / 60)
        elif i < len(bird_angle) - 1:
            #dis_temp = Cal_GPS_to_dis(Lon[i-1], Lat[i-1], Lon[i], Lat[i]) + \
            #Cal_GPS_to_dis(Lon[i], Lat[i], Lon[i+1], Lat[i+1])
            temp_speed = (bird_angle[i+1] - bird_angle[i-1]) / ((times[i+1] - times[i-1]).seconds / 60)
            #temp_speed = (temp_speed_ave * (times[i+1] - times[i]).seconds / (times[i] - times[i-1]).seconds)
        
        #if temp_speed > 100:
            #print temp_speed, times[i]
        bird_acc.append(temp_speed)
    
    return bird_acc


def Cal_depth_change(bird_depth):
    #bird_depth_diff_abs = []
    bird_depth_diff = [0]
    for i in range(len(bird_depth) - 1):
        temp_speed = bird_depth[i+1] - bird_depth[i]
        #bird_depth_diff_abs.append(abs(temp_speed))
        bird_depth_diff.append(temp_speed)
    
    return bird_depth_diff#, bird_depth_diff_abs


def Cal_depth_diff(bird_depth, times):
    bird_depth_diff_abs = []
    bird_depth_diff = []
    for i in range(len(bird_depth)):
        if (i == 0) or ((times[i] - times[i-1]).seconds > 20 and i < len(bird_depth) - 1):
            #dis_temp = Cal_GPS_to_dis(Lon[i], Lat[i], Lon[i+1], Lat[i+1])
            temp_speed = (bird_depth[i+1] - bird_depth[i]) / (times[i+1] - times[i]).seconds
        elif (i == len(bird_depth) - 1) or ((times[i+1] - times[i]).seconds > 20 and i > 0):
            #dis_temp = Cal_GPS_to_dis(Lon[i-1], Lat[i-1], Lon[i], Lat[i])
            temp_speed = (bird_depth[i] - bird_depth[i-1]) / (times[i] - times[i-1]).seconds
        elif i < len(bird_depth) - 1:
            #dis_temp = Cal_GPS_to_dis(Lon[i-1], Lat[i-1], Lon[i], Lat[i]) + \
            #Cal_GPS_to_dis(Lon[i], Lat[i], Lon[i+1], Lat[i+1])
            temp_speed = (bird_depth[i+1] - bird_depth[i-1]) / (times[i+1] - times[i-1]).seconds
            #temp_speed = (temp_speed_ave * (times[i+1] - times[i]).seconds / (times[i] - times[i-1]).seconds)
        
        #if temp_speed > 100:
            #print temp_speed, times[i]
        bird_depth_diff_abs.append(abs(temp_speed))
        bird_depth_diff.append(temp_speed)
    
    return bird_depth_diff, bird_depth_diff_abs

#distance from lat&lon
def Cal_GPS_to_dis(Lon_a, Lat_a, Lon_b, Lat_b):
    Ra = 6378.140
    Rb = 6356.755
    
    if Lon_a == Lon_b and Lat_a == Lat_b:
        return 0
    else:
        flatten = (Ra - Rb) / Ra
        Rad_lat_a = radians(Lat_a)
        Rad_lon_a = radians(Lon_a)
        Rad_lat_b = radians(Lat_b)
        Rad_lon_b = radians(Lon_b)
        
        Pa = atan(Rb / Ra * tan(Rad_lat_a))
        Pb = atan(Rb / Ra * tan(Rad_lat_b))
        xx = acos(sin(Pa) * sin(Pb) +  cos(Pa) * cos(Pb) * cos(Rad_lon_a - Rad_lon_b))
        
        c1 = (sin(xx) - xx) * (sin(Pa) + sin(Pb)) **  2 / cos(xx / 2) ** 2
        c2 = (sin(xx) + xx) * (sin(Pa) - sin(Pb)) **  2 / sin(xx / 2) ** 2
        dr = flatten / 8 * (c1 - c2)
        
        distance = Ra * (xx + dr) * 1000

        return distance
    
    
def proj_tran(Lon, Lat):
    p_gps = Proj(init = 'epsg:2486')
    p_proj = Proj(init = 'epsg:2458') #japan
    
    x1, y1 = p_gps(Lon, Lat)
    x2, y2 = transform(p_gps, p_proj, x1, y1, radians = True)
    
    return x2, y2

#calculate angle
def single_angle(mv, ref_mv = [1,0]):
    x1 = np.array(ref_mv, dtype=np.float)
    x2 = np.array(mv, dtype=np.float)
    
    Lx1 = np.sqrt(x1.dot(x1))
    Lx2 = np.sqrt(x2.dot(x2))
    
    if Lx1 * Lx2 == 0 :
        if Lx2 == 0.0:#停止
            return 0
        else:
            print (Lx1,Lx2, mv)
    #elif round(x1[0]*x2[1] - x1[1]*x2[0], 4) == 0.0:
    #    print x1[0]*x2[1],  x1[1]*x2[0], x1[0]*x2[1] - x1[1]*x2[0]
    #    if(x2[0] > 0.0) :
    #       angle_abs = 0
    #   else:
    #       angle_abs = round(-np.pi, 2)
    else:
        cos_ang = x1.dot(x2) / (Lx1 * Lx2)
        if cos_ang <= -1.0:
            angle_abs = np.pi
            print (cos_ang)
        else:    
            angle_abs = round(np.arccos(cos_ang), 2)
            if np.isnan(np.arccos(cos_ang)):
                print ('1')#cos_ang

    sign = 1#= sign_angle(x1, x2)
    
    return sign * angle_abs


#sign of angle
def sign_angle(p1, p2):
    sign = np.cross(p1, p2)
    if sign >= 0 :
        sign = 1
    else:
        sign = -1
        
    return sign