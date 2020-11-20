# -*- coding: utf-8 -*-
'''
Created on 2017年10月12日

@author: tian
'''

#using R in python
from rpy2 import robjects
from rpy2.robjects.packages import importr
adehabitatLT = importr('adehabitatLT')
xlsx = importr('xlsx')
from pyproj import Proj, transform

import os
import xlrd
import numpy as np


def py_2_R_return_appoint(Lon, Lat, bird_times, radious, interval):
    result = []
    x_temp, y_temp = proj_tran(Lon, Lat)

    bird_time_temp = [bird_times[i] for i in range(len(bird_times))]
    time_temp = robjects.vectors.POSIXct(bird_time_temp)
    x_a = robjects.vectors.FloatVector(x_temp)
    y_a = robjects.vectors.FloatVector(y_temp)
    robjects.globalenv['x_a'] = x_a
    robjects.globalenv['y_a'] = y_a
    robjects.globalenv['time_temp'] = time_temp
    robjects.globalenv['radius'] = radious
    rscript = '''
        x_1 = array(dim = length(x_a))
        y_1 = array(dim = length(y_a))
        for(i in 1:length(x_a))
        {
            x_1[i] <- x_a[i]
            y_1[i] <- y_a[i]    
        }
        temp = c(x_1, y_1)
        data <- matrix(temp, nrow = length(x_a))
        bird_tra <- as.ltraj(xy = data, date = time_temp, id = "Bird", typeII = TRUE)
        fpt_re <- fpt(bird_tra, seq(radius, radius, length = 1))
        fpt_data <- data.frame(fpt_re[[1]])
        fpt_data[is.na(fpt_data)]<-1000000
        return (fpt_data)
    '''
    
    data = robjects.r(rscript)
    
    data_temp = [i for i in data[0]]# if i != 1000000
    
    for i in range(len(data_temp)):
        if data_temp[i] == 1000000:
            data_temp[i] = 3600 * interval
    
    return data_temp

def proj_tran(Lon, Lat):
    p_gps = Proj(init = 'epsg:2486')
    p_proj = Proj(init = 'epsg:2458') #japan
    
    x1, y1 = p_gps(Lon, Lat)
    x2, y2 = transform(p_gps, p_proj, x1, y1, radians = True)
    
    return x2, y2