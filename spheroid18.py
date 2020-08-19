#! /usr/bin/env python

import simple3d
import random
import math
import sys

def rotX(v, angle) :
    "rotate vertex v angle radians about the X axis"
    c = math.cos(angle)
    s = math.sin(angle)
    newY = v[1]*c - v[2]*s
    newZ = v[1]*s + v[2]*c
    return [v[0], newY, newZ]

def rotY(v, angle) :
    "rotate vertex v angle radians about the Y axis"
    c = math.cos(angle)
    s = math.sin(angle)
    newX = v[0]*c - v[2]*s
    newZ = v[0]*s + v[2]*c
    return [newX, v[1], newZ]
     
def rotZ(v, angle) :
    "rotate vertex v angle radians about the Z axis"
    c = math.cos(angle)
    s = math.sin(angle)
    newX = v[0]*c - v[1]*s
    newY = v[0]*s + v[1]*c
    return [newX, newY, v[2]]
    
def getRandomColor() : 
    rgb = []
    rgb.append(random.random())
    rgb.append(random.random())
    rgb.append(random.random())
    return rgb

# radians for rotations
theta = math.radians(180/20)   # divide semicircle into 20 segments

print('init...')
fish = simple3d.Simple3d()

first_pt = [0.0, -2.0, 0.0]
fish.append_vertex(first_pt[0], first_pt[1], first_pt[2])
new_pt = first_pt
last_pt_idx = 0
for lat in range(19) :
    new_pt = rotZ(new_pt, theta)
    fish.append_vertex(new_pt[0], new_pt[1], new_pt[2])
    last_pt_idx += 1
    lat_start = last_pt_idx
    new_lat_pt = new_pt
    for long in range(39) :
        new_lat_pt = rotY(new_lat_pt, theta)
        fish.append_vertex(new_lat_pt[0], new_lat_pt[1], new_lat_pt[2])
        last_pt_idx += 1
        fish.connect_last(0.0, 0.0, 0.0, 1.)
        color = getRandomColor()
        if lat_start + long + 40 < 761 :
            fish.append_edge(last_pt_idx, lat_start + long, 0.0, 0.0, 0.0, 1.)
            fish.append_edge(last_pt_idx, lat_start + long + 40, 0.0, 0.0, 0.0, 1.)
            fish.append_face(last_pt_idx, lat_start + long, lat_start + long + 40, color[0], color[1], color[2], 1.)
    fish.append_edge(lat_start, last_pt_idx, 0.0, 0.0, 0.0, 1.0) # closes the circle
    if lat_start + 79 < 761 :
        fish.append_edge(lat_start, last_pt_idx, 0.0, 0.0, 0.0, 1.0)
        fish.append_edge(lat_start, lat_start + 79, 0.0, 0.0, 0.0, 1.0)
        fish.append_face(lat_start, last_pt_idx, lat_start + 79, 0.0, 0.0, 0.0, 1.0)

nvertices = len(fish.vertex)
print(nvertices, "vertices")
        
# object gets named after the script that made it
objname = sys.argv[0][0:-3]
fish.store_object("objects", objname)
# make a wavefront .obj version for Inkscape
# TO DO: make this work on non-Windows OS
#fish.store_as_wf_obj("/Program Files/Inkscape/share/extensions/Poly3DObjects", objname + '.obj')
fish.store_as_wf_obj("objects", objname + '.obj')

print('done.')