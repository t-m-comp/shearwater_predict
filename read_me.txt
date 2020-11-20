The program consists of 2 steps: feature extraction and classification:
First run "Main_read_depth_accto_trip.py" to obtain features varying different time segments and use fuction "write_txt" (line 175) to write features into txt.
Then use "Classification.py" to perform cross validation on different time segments.

1.Main_read_depth_accto_trip.py
Feature extraction code.
Function "bird_trip_define_label" in line 623 is used to extract features from GPS.
Function "bird_trip_number_of_dives_hour" in line 938 is used to extract features from water depth.
Please set locations of data file (Lines 27 - 34).

2.Calculate_angle_speed.py
Compute features such as, speed and orientation.

3.Calssification.py
Cross validation code.

4.Read_Data.py
Read data (GPS ot water depth) from csv and txt.

5.FPT_R.py
Calculate FPT(first passage time) use R.

6.Boxplot_code.R
Box plot code.


Used lib in Python

1.numpy
2.math
3.pyproj
4.sklearn
5.random
6.warnings
7.xlrd
8.csv
9.os
10.codecs
11.datetime
12.import xlwt
13.rpy2


Used lib in R
1.adehabitatLT