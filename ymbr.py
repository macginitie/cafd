#! /usr/bin/env python

import simple3d
import random
import sys
import math

# radians for rotations
theta = math.radians(180/43)   # divide semicircle into 43 segments
num_cubes = 86
# vertical displacement per cube
incr = 0.02
# cube size
edge_len = 0.3

print('init...')
fish = simple3d.Simple3d()

first_pt = [0.0, 0.0, 3.0]
fish.append_vertex(first_pt[0], first_pt[1], first_pt[2]) #0
alpha = 1
while alpha < (8*num_cubes) :
    new_pt = simple3d.rotY(first_pt, alpha*theta)
    #new_pt[2] += (alpha*incr)
    print('alpha, y, z = ', alpha, new_pt[1], new_pt[2])
    # vertices
    fish.append_vertex(new_pt[0], new_pt[1], new_pt[2]) #1
    fish.append_vertex(new_pt[0] + edge_len, new_pt[1], new_pt[2]) #2
    fish.append_vertex(new_pt[0] + edge_len, new_pt[1] + edge_len, new_pt[2]) #3
    fish.append_vertex(new_pt[0] + edge_len, new_pt[1] + edge_len, new_pt[2] + edge_len) #4
    fish.append_vertex(new_pt[0], new_pt[1] + edge_len, new_pt[2] + edge_len) #5
    fish.append_vertex(new_pt[0], new_pt[1], new_pt[2] + edge_len) #6
    fish.append_vertex(new_pt[0] + edge_len, new_pt[1], new_pt[2] + edge_len) #7
    fish.append_vertex(new_pt[0], new_pt[1] + edge_len, new_pt[2]) #8
    # edges
    color = simple3d.getRandomDarkColor()
    fish.append_edge(alpha, alpha + 1, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 1, alpha + 2, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 2, alpha + 3, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 3, alpha + 4, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 4, alpha + 5, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 5, alpha + 6, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha, alpha + 7, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha, alpha + 5, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 6, alpha + 1, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 6, alpha + 3, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 7, alpha + 4, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 7, alpha + 2, color[0], color[1], color[2], 1.)
    # faces
    # front
    colorf = simple3d.getRandomColor()
    fish.append_face(alpha, alpha + 2, alpha + 1, colorf[0], colorf[1], colorf[2], 1.)
    fish.append_face(alpha, alpha + 7, alpha + 2, colorf[0], colorf[1], colorf[2], 1.)
    # back
    colorf = simple3d.getRandomColor()
    fish.append_face(alpha + 3, alpha + 4, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
    fish.append_face(alpha + 3, alpha + 5, alpha + 6, colorf[0], colorf[1], colorf[2], 1.)
    # left
    colorf = simple3d.getRandomColor()
    fish.append_face(alpha + 4, alpha + 7, alpha, colorf[0], colorf[1], colorf[2], 1.)
    fish.append_face(alpha + 4, alpha, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
    # right
    colorf = simple3d.getRandomColor()
    fish.append_face(alpha + 1, alpha + 3, alpha + 6, colorf[0], colorf[1], colorf[2], 1.)
    fish.append_face(alpha + 1, alpha + 2, alpha + 3, colorf[0], colorf[1], colorf[2], 1.)
    # top
    colorf = simple3d.getRandomColor()
    fish.append_face(alpha + 2, alpha + 4, alpha + 3, colorf[0], colorf[1], colorf[2], 1.)
    fish.append_face(alpha + 2, alpha + 7, alpha + 4, colorf[0], colorf[1], colorf[2], 1.)
    # bottom
    colorf = simple3d.getRandomColor()
    fish.append_face(alpha, alpha + 1, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
    fish.append_face(alpha + 1, alpha + 6, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
    
    alpha += 8
    
fish.replitranslacate( (0, 0.6, 0) )    
fish.replitranslacate( (0, 1.2, 0) )
fish.replitranslacate( (0, 2.4, 0) )
fish.replitranslacate( (0, 4.8, 0) )
# move up
fish.move((0.0, -2.4, 0.0))
# rot8 90 degrees
fish.rotX(math.pi/2.0)

# object gets named after the script that made it
objname = sys.argv[0][0:-3]
fish.store_object("objects", objname)
# make a wavefront .obj version for Inkscape
fish.store_as_wf_obj("objects", objname + '.obj')

print('done.')