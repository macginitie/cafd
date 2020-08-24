#! /usr/bin/env python

"""
sor <== surface of revolution
"""

import csv
import math
import simple3d
import sys

"""
TO DO: put the parameters (radius etc.) into the spline file
... or @ least use argparse
"""

def read_spline_pts(fname) :
    reader = csv.reader(open(fname, 'r'), delimiter=',')
    pts = []
    for row in reader :
        pts.append( [float(row[0]), float(row[1]), 1.0] )
    return pts
    

def has_zero_in_rotation_axis(pts, axis):    
    idx = 0 if axis == 'x' else 1
    epsilon = 0.01
    for pt in pts:
        if abs(0.0 - pt[idx]) < epsilon:
            return True
    return False
    
    
try:
    infile = sys.argv[1]
except:    
    infile = 'bspline-pt-list.txt'
    
pts = read_spline_pts(infile)

# number of "latitude" lines
try:
    lat_lines = len(pts)
except:
    lat_lines = 10
    
# number of "longitude" lines
try:
    long_lines = int(sys.argv[2])
except:
    long_lines = 10
    q
# radians for rotations
theta = math.radians(180/lat_lines)   # divide semicircle into lat_lines segments
rho = math.radians(360/long_lines)   # divide circle into long_lines segments

# radius
try:
    radius = double(sys.argv[3])
except:
    radius = 10.0  # 2DO: base it on spline pts

# axis of rotation
try:
    axis = sys.argv[4].lower()
except:
    axis = 'x'    
    
if has_zero_in_rotation_axis(pts, axis):
    print('error in point list: value too close to the axis of rotation is not allowed')
    exit()
    
print( lat_lines, long_lines, radius, axis )    
    
fish = simple3d.Simple3d()

red = (1.0, 0.0, 0.0, 1.0)
green = (0.0, 1.0, 0.0, 1.0)
blue = (0.0, 0.0, 1.0, 1.0)
black = (0.0, 0.0, 0.0, 1.0)
magenta = (1.0, 0.0, 1.0, 1.0)
colors = [red, green, blue, black, magenta]
color_idx = 0

for lat in range(lat_lines) :
    new_pt = pts[lat]
    fish.append_vertex(new_pt[0], new_pt[1], new_pt[2])

    for long in range(long_lines - 1) :
        new_pt = simple3d.rotate(new_pt, axis, rho)
        fish.append_vertex(new_pt[0], new_pt[1], new_pt[2])
        fish.connect_last(blue)
        last_pt_idx = len(fish.vertex) - 1
        if last_pt_idx >= long_lines:
            fish.append_edge(last_pt_idx, last_pt_idx - long_lines, colors[color_idx])
            if long < long_lines - 2:
                fish.append_face(last_pt_idx - long_lines, 1+(last_pt_idx - long_lines), last_pt_idx, colors[color_idx])
            else:
                fish.append_face(last_pt_idx - long_lines, (lat-1) * long_lines, last_pt_idx, colors[color_idx])
    
    # bridge the gap between 1st & last "sector" of the pi ;-)
    fish.append_edge(last_pt_idx, 1 + (last_pt_idx - long_lines), blue)
    
    if lat < (lat_lines-1):
        fish.append_edge(1 + (last_pt_idx - long_lines), last_pt_idx+1, colors[(color_idx+1) % len(colors)])
        fish.append_face(1+(last_pt_idx - long_lines), 2+(last_pt_idx - long_lines), last_pt_idx+1, colors[(color_idx+1) % len(colors)])
        
    color_idx = (color_idx+1) % len(colors)

nvertices = len(fish.vertex)
print(nvertices, "vertices")
        
# object gets named after the script that made it
# 2DO: format or % plz
objname = sys.argv[0][0:-3] + '-' + str(lat_lines) + '-' + str(long_lines) + '-' + str(radius) + '-' + axis
fish.store_object("objects", objname)

print('done.')