#! /usr/bin/env python

"""
sor == surface of revolution
"""

import csv
import math
import simple3d
import sys


def read_spline_pts(fname) :
    reader = csv.reader(open(fname, 'r'), delimiter=',')
    pts = []
    for row in reader :
        pts.append( [float(row[0]), float(row[1]), 0.0] )
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
    
# radians for rotations
theta = math.radians(180/lat_lines)   # divide semicircle into lat_lines segments
rho = math.radians(360/long_lines)   # divide circle into long_lines segments

# radius
try:
    radius = double(sys.argv[3])
except:
    radius = 10.0

# axis of rotation
try:
    axis = sys.argv[4].lower()
except:
    axis = 'x'    
    
if has_zero_in_rotation_axis(pts, axis):
    print('error in point list: value too close to the axis of rotation is not allowed')
    exit()

# inkscape object folder a.k.a. our output folder
try:
    inkscape_dir = sys.argv[5]
except:
    # Windows default location
    inkscape_dir = "/Program Files/Inkscape/share/extensions/Poly3DObjects"
    # cwd
    inkscape_dir = "./"
    
print( lat_lines, long_lines, radius, axis, inkscape_dir )    
    
fish = simple3d.Simple3d()


redval = 0.0
redincr = 0.1
last_pt_idx = 0
for lat in range(lat_lines) :
    redval += redincr
    if redval > 1.0:
        redval = 0.0
    new_pt = pts[lat]
    fish.append_vertex(new_pt[0], new_pt[1], new_pt[2])
    last_pt_idx += 1
    #fish.connect_last(0.0, 0.0, 0.0, 1.)
    if lat < (lat_lines - 1) :
        lat_start = last_pt_idx
        new_lat_pt = new_pt
        print(new_lat_pt)
        for long in range(long_lines - 1) :
            new_lat_pt = simple3d.rotate(new_lat_pt, axis, rho)
            fish.append_vertex(new_lat_pt[0], new_lat_pt[1], new_lat_pt[2])
            last_pt_idx += 1
            fish.connect_last(0.5, 0.0, 0.0, 0.2)
            color = simple3d.getRandomColor()
            fish.append_edge(last_pt_idx, last_pt_idx - long_lines, redval, 0.0, 0.5, 0.4)
            fish.append_face(last_pt_idx - long_lines, last_pt_idx - 1, last_pt_idx, redval, color[1], color[2], 1.)
            fish.append_face(last_pt_idx - long_lines, last_pt_idx - (1+long_lines), last_pt_idx - 1, redval, color[1], color[2], 1.)
        # bridge the gap between 1st & last "sector" of the pi ;-)
        fish.append_edge(last_pt_idx, 1 + (last_pt_idx - long_lines), 0.3, 0.0, 0.3, 0.5)
        #fish.append_edge(last_pt_idx + 1, 1 + (last_pt_idx - long_lines), 0.8, 0.0, 0.5, 0.4)
        #fish.append_face(last_pt_idx, last_pt_idx + 1, 1 + (last_pt_idx - long_lines), 1.0, 0.0, 0.0, 1.)
        fish.append_face(1 + (last_pt_idx - long_lines), last_pt_idx - long_lines, last_pt_idx, 0.0, 0.0, 1.0, 1.)

nvertices = len(fish.vertex)
print(nvertices, "vertices")
        
# object gets named after the script that made it
objname = sys.argv[0][0:-3] + '-' + str(lat_lines) + '-' + str(long_lines) + '-' + axis
fish.store_object("objects", objname)
# make a wavefront .obj version for Inkscape
fish.store_as_wf_obj(inkscape_dir, objname + '.obj')

print('done.')