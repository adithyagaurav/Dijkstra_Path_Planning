import cv2
import matplotlib.pyplot as plt
import numpy
import numpy as np
import math

def draw_triangle_occupancy(pt1, pt2, pt3, map, occ_mode):
    x1, y1 = pt1[0], pt1[1]
    x2, y2 = pt2[0], pt2[1]
    x3, y3 = pt3[0], pt3[1]
    m1, m2, m3 = (y2 - y1) / (x2 - x1), (y3-y2)/(x3-x2), (y1-y3)/(x1-x3)
    c1, c2, c3 = (y1 * x2 - x1 * y2) / (x2 - x1), (y2*x3 - x2*y3)/(x3-x2), (y3*x1 - x3*y1)/(x1-x3)
    for x in range(400):
        for y in range(250):
            if ((occ_mode[0]=='lower' and y - (m1 * x + c1)<0) or (occ_mode[0]=='upper' and y - (m1 * x + c1)>=0)) and \
                    ((occ_mode[1]=='lower' and y - (m2 * x + c2)<0) or (occ_mode[1]=='upper' and y - (m2 * x + c2)>=0)) and\
                    ((occ_mode[2] == 'lower' and y - (m3 * x + c3) < 0) or (occ_mode[2] == 'upper' and y - (m3 * x + c3) >= 0)):
                map[y, x] = 1
            else:
                map[y, x] = 0
    return np.flipud(map)
def draw_circle(center, radius, map):
    x_c, y_c = center[0], center[1]
    for x in range(400):
        for y in range(250):
            if math.sqrt((x-x_c)**2 + (y-y_c)**2)<radius:
                map[y,x]=1
            else:
                map[y,x]=0
    return np.flipud(map)
def draw_rect(pt_top_left, pt_bottom_right, map):
    x_tl, y_tl = pt_top_left[0], pt_top_left[1]
    x_br, y_br = pt_bottom_right[0], pt_bottom_right[1]
    for x in range(400):
        for y in range(250):
            if x>x_tl and x<x_br and y>y_tl and y<y_br:
                map[y,x]=1
            else:
                map[y,x]=0
    return np.flipud(map)
def create_map():
    map = np.zeros((250, 400), dtype = np.float32)
    map_poly_123 = draw_triangle_occupancy((36.0, 185.0), (115.0, 250.0-40), (105.0-25.0,180.0), map.copy(), occ_mode=['lower', 'upper', 'upper'])
    map_poly_134 = draw_triangle_occupancy((36.0, 185.0), (105.0-25.0,180.0), (105.0,100.0), map.copy(), occ_mode=['lower', 'lower', 'upper'])
    map_poly = cv2.bitwise_or(map_poly_123, map_poly_134)
    map_circle = draw_circle((400.0-100.0, 250.0-65.0), 40.0, map.copy())
    map_hex_123 = draw_triangle_occupancy((400-200-35, 100+20.2), (400-200, 100+40.4), (400-200+35, 100+20.2), map.copy(), occ_mode=['lower', 'lower', 'upper'])
    map_hex_456 = draw_triangle_occupancy((400 - 200 - 35, 100 - 20.2), (400 - 200, 100 - 40.4),
                                          (400 - 200 + 35, 100 - 20.2), map.copy(),
                                          occ_mode=['upper', 'upper', 'lower'])
    map_rect = draw_rect((400 - 200 - 35, 100 - 20.2), (400-200+35, 100+20.2) ,map.copy())
    map_hex = map_hex_123+map_hex_456+map_rect
    map_final = map_poly + map_circle + map_hex
    return map_final