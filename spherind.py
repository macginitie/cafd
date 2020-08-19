#! /usr/bin/env python

import simple3d
import math
import sys

# number of "latitude" lines
try:
    lat_lines = int(sys.argv[1])
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

print('init...')
fish = simple3d.Simple3d()

first_pt = [0.0, -radius, 0.0]
fish.append_vertex(first_pt[0], first_pt[1], first_pt[2])
fish.append_edge(1, 0, 0.0, 0.0, 0.0, 0.1)
new_pt = first_pt
last_pt_idx = 0
for lat in range(lat_lines) :
    new_pt = simple3d.rotZ(new_pt, theta)
    fish.append_vertex(new_pt[0], new_pt[1], new_pt[2])
    last_pt_idx += 1
    #fish.connect_last(0.0, 0.0, 0.0, 1.)
    if lat < (lat_lines - 1) :
        lat_start = last_pt_idx
        new_lat_pt = new_pt
        for long in range(long_lines - 1) :
            new_lat_pt = simple3d.rotY(new_lat_pt, rho)
            fish.append_vertex(new_lat_pt[0], new_lat_pt[1], new_lat_pt[2])
            last_pt_idx += 1
            fish.connect_last(0.5, 0.0, 0.0, 0.2)
            color = simple3d.getRandomColor()
            if lat == 0 : # 'south' polar cap
                fish.append_edge(last_pt_idx, 0, 0.0, 0.5, 0.0, 0.3)
                fish.append_face(0, last_pt_idx - 1, last_pt_idx, color[0], color[1], color[2], 1.)
            else :
                fish.append_edge(last_pt_idx, last_pt_idx - long_lines, 0.0, 0.0, 0.5, 0.4)
                if (lat % 2) == 0:
                    fish.append_face(last_pt_idx - long_lines, last_pt_idx - 1, last_pt_idx, color[0], color[1], color[2], 1.)
                    fish.append_face(last_pt_idx - long_lines, last_pt_idx - (1+long_lines), last_pt_idx - 1, color[0], color[1], color[2], 1.)
        # bridge the gap between 1st & last "sector" of the pi ;-)
        fish.append_edge(last_pt_idx, 1 + (last_pt_idx - long_lines), 0.3, 0.0, 0.3, 0.5)
        fish.append_edge(last_pt_idx + 1, 1 + (last_pt_idx - long_lines), 0.8, 0.0, 0.5, 0.4)
        if (lat % 2) == 0:
            fish.append_face(last_pt_idx, last_pt_idx + 1, 1 + (last_pt_idx - long_lines), 1.0, 0.0, 0.0, 1.)
            fish.append_face(1 + (last_pt_idx - long_lines), last_pt_idx - long_lines, last_pt_idx, 0.0, 0.0, 1.0, 1.)
    else :
        # 'north' polar cap
        for long in range(long_lines-1) :
            fish.append_edge(last_pt_idx, last_pt_idx - (1+long), 0.0, 0.2, 0.2, 0.6)
            if (lat % 2) == 0:
                color = simple3d.getRandomColor()
                fish.append_face(last_pt_idx - (1+long), last_pt_idx - (2+long), last_pt_idx, color[0], color[1], color[2], 1.)

nvertices = len(fish.vertex)
print(nvertices, "vertices")
        
# object gets named after the script that made it
objname = sys.argv[0][0:-3] + '-' + str(lat_lines) + '-' + str(long_lines)
fish.store_object("objects", objname)
# make a wavefront .obj version for Inkscape
fish.store_as_wf_obj("/Program Files/Inkscape/share/extensions/Poly3DObjects", objname + '.obj')

print('done.')