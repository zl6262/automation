# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 13:52:24 2021

@author: Zl6262
"""

import laspy
import math

"""file path"""
ori_file_path = 'D:/Program Projects/GIS/proj1/point_cloud/out.las'
mod_file_path = 'D:/Program Projects/GIS/proj1/point_cloud/points_modified11.las'


""" the box coordinates to be mapped"""
xmin_to_map = 121.440679
xmax_to_map = 121.443968
ymin_to_map = 31.026270
ymax_to_map = 31.028821


mins = [xmin_to_map, ymin_to_map]
maxs = [xmax_to_map, ymax_to_map]

def cal_ratio(ori_mins, ori_maxs,
              mins, maxs):
    """
    calculate the scale factors and offset factors
    """
    ratio_x = abs((maxs[0] - mins[0]) / (ori_maxs[0] - ori_mins[0]))
    ratio_y = abs((maxs[1] - mins[1]) / (ori_maxs[1] - ori_mins[1]))
    
    offset_x = ((maxs[0] + mins[0]) - (ori_maxs[0] + ori_mins[0]) * ratio_x) / 2
    offset_y = ((maxs[1] + mins[1]) - (ori_maxs[1] + ori_mins[1]) * ratio_y) / 2
    
    return ((ratio_x, ratio_y),(offset_x, offset_y))
    
    
    
# def cal_rot(a,b,c, x,y,z):

#     rot_mat = [[math.cos(a)*math.cos(c)-math.cos(b)*math.sin(a)*math.sin(c), -math.cos(b)*math.cos(c)*math.sin(a)-math.cos(a)*math.sin(c), math.sin(a)*math.sin(b)],
#           [math.cos(y)*math.sin(a)+math.cos(a)*math.cos(b)*math.sin(y), math.cos(a)*math.cos(b)*math.cos(c)-math.sin(a)*math.sin(c), -math.cos(a)*math.sin(b)],
#           [math.sin(b)*math.sin(c), math.cos(c)*math.sin(b), math.cos(b)]]
#     res_x = rot_mat[0][0]*x + rot_mat[0][1]*x + rot_mat[0][2]*x
#     res_y = rot_mat[]


def read_las(ori_file_path,mod_file_path):
    with laspy.open(ori_file_path) as ori_las:
        ori_mins = ori_las.header.mins
        ori_maxs = ori_las.header.maxs
        ori_scales = ori_las.header.scales
        ori_offsets = ori_las.header.offsets
        print(ori_mins, ori_maxs, ori_scales, ori_offsets)
    
    ratios, offsets = cal_ratio(ori_mins/ori_scales, ori_maxs/ori_scales, mins, maxs)
    las = laspy.read(ori_file_path)
    print(ratios[0], offsets[0], offsets[1])
    las.header.scales = [ratios[0], ratios[1],0.01/5]
    las.header.offsets = [offsets[0], offsets[1],6]
    
    las.write(mod_file_path)
    las = laspy.read(ori_file_path)
    return las
    

a = read_las(ori_file_path,mod_file_path)