#! /usr/bin/env python

import simple3d
import math
import sys

def zfunc(x, y, scale = 1.0):
    return math.sin(x*x + y*y) * scale

# number of "x" lines
try:
    x_lines = int(sys.argv[1])
except:
    x_lines = 10
# number of "y" lines
try:
    y_lines = int(sys.argv[2])
except:
    y_lines = 10

# x spacing
try:
    x_step = double(sys.argv[3])
except:
    x_step = 1.0

# y spacing
try:
    x_step = double(sys.argv[4])
except:
    y_step = 1.0

# inkscape object folder
try:
    inkscape_dir = sys.argv[5]
except:
    # default to Windows default location
    inkscape_dir = "/Program Files/Inkscape/share/extensions/Poly3DObjects"

print('init...')

fish = simple3d.Simple3d()

zscale = 10.
x = -(x_lines/x_step)/2
v_num = 0
for i in range(x_lines):
    y = -(y_lines/y_step)/2
    for j in range(y_lines):
        fish.append_vertex(x, y, zfunc(x, y, zscale))
        print(i,j,x,y)
        if v_num > 0 and j > 0:
            fish.append_edge(v_num, v_num - 1)
            fish.append_edge(v_num, v_num - y_lines)
            if v_num > y_lines:
                fish.append_face(v_num, v_num - 1, v_num - y_lines)
                fish.append_face(v_num - y_lines, v_num - 1, v_num - (1+y_lines))
        v_num += 1
        y += y_step
    x += x_step
    
nvertices = len(fish.vertex)
print(nvertices, "vertices")
        
# object gets named after the script (& args) that made it
objname = sys.argv[0][0:-3] + '-' + str(x_lines) + '-' + str(y_lines)
fish.store_object("objects", objname)
# make a wavefront .obj version for Inkscape
fish.store_as_wf_obj(inkscape_dir, objname + '.obj')

print('done.')    
    
