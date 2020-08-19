#! /usr/bin/env python

import simple3d
import random
import sys
import math

def verticals(fish, num_liths, z_offset, edge_x, edge_y, edge_z) :

    # radians for rotations
    theta = math.radians(360/num_liths)   # divide circle into num_liths segments

    # 1st lith
    first_pt = [0.0, 0.0, z_offset]
    fish.append_vertex(first_pt[0], first_pt[1], first_pt[2]) #0
    fish.append_vertex(first_pt[0] + edge_x, first_pt[1], first_pt[2]) #1
    fish.append_vertex(first_pt[0] + edge_x, first_pt[1] + edge_y, first_pt[2]) #2
    fish.append_vertex(first_pt[0] + edge_x, first_pt[1] + edge_y, first_pt[2] + edge_z) #3
    fish.append_vertex(first_pt[0], first_pt[1] + edge_y, first_pt[2] + edge_z) #4
    fish.append_vertex(first_pt[0], first_pt[1], first_pt[2] + edge_z) #5
    fish.append_vertex(first_pt[0] + edge_x, first_pt[1], first_pt[2] + edge_z) #6
    fish.append_vertex(first_pt[0], first_pt[1] + edge_y, first_pt[2]) #7

    alpha = 0
    while alpha < (8*num_liths) :
        # vertices
        for pt in range(8) :
            new_vert = simple3d.rotY(fish.vertex[alpha+pt], theta)
            fish.append_vertex(new_vert[0], new_vert[1], new_vert[2])

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
        # ...front
        colorf = simple3d.getRandomColor()
        fish.append_face(alpha, alpha + 2, alpha + 1, colorf[0], colorf[1], colorf[2], 1.)
        fish.append_face(alpha, alpha + 7, alpha + 2, colorf[0], colorf[1], colorf[2], 1.)
        # ...back
        colorf = simple3d.getRandomColor()
        fish.append_face(alpha + 3, alpha + 4, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
        fish.append_face(alpha + 3, alpha + 5, alpha + 6, colorf[0], colorf[1], colorf[2], 1.)
        # ...left
        colorf = simple3d.getRandomColor()
        fish.append_face(alpha + 4, alpha + 7, alpha, colorf[0], colorf[1], colorf[2], 1.)
        fish.append_face(alpha + 4, alpha, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
        # ...right
        colorf = simple3d.getRandomColor()
        fish.append_face(alpha + 1, alpha + 3, alpha + 6, colorf[0], colorf[1], colorf[2], 1.)
        fish.append_face(alpha + 1, alpha + 2, alpha + 3, colorf[0], colorf[1], colorf[2], 1.)
        # ...top
        colorf = simple3d.getRandomColor()
        fish.append_face(alpha + 2, alpha + 4, alpha + 3, colorf[0], colorf[1], colorf[2], 1.)
        fish.append_face(alpha + 2, alpha + 7, alpha + 4, colorf[0], colorf[1], colorf[2], 1.)
        # ...bottom
        colorf = simple3d.getRandomColor()
        fish.append_face(alpha, alpha + 1, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
        fish.append_face(alpha + 1, alpha + 6, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
        
        alpha += 8

# they're really lintels, not plinths
def plinths(fish, num_plinths, z_offset, v_offset, edge_x, edge_y, edge_z) :

    alpha = len(fish.vertex)
    print('plinths starting @ vertex #', alpha, 'edge_x=',edge_x)

    # radians for rotations
    theta = math.radians(360/num_plinths)   # divide circle into num_plinths segments

    # 1st plinth
    first_pt = [0.0, v_offset, z_offset]
    fish.append_vertex(first_pt[0], first_pt[1], first_pt[2]) #0
    fish.append_vertex(first_pt[0] + edge_x, first_pt[1], first_pt[2]) #1
    fish.append_vertex(first_pt[0] + edge_x, first_pt[1] + edge_y, first_pt[2]) #2
    fish.append_vertex(first_pt[0] + edge_x, first_pt[1] + edge_y, first_pt[2] + edge_z) #3
    fish.append_vertex(first_pt[0], first_pt[1] + edge_y, first_pt[2] + edge_z) #4
    fish.append_vertex(first_pt[0], first_pt[1], first_pt[2] + edge_z) #5
    fish.append_vertex(first_pt[0] + edge_x, first_pt[1], first_pt[2] + edge_z) #6
    fish.append_vertex(first_pt[0], first_pt[1] + edge_y, first_pt[2]) #7
    
    for i in range(num_plinths) :
        # vertices
        for pt in range(8) :
            new_vert = simple3d.rotY(fish.vertex[alpha+pt], theta)
            fish.append_vertex(new_vert[0], new_vert[1], new_vert[2])

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
        # ...front
        colorf = simple3d.getRandomColor()
        fish.append_face(alpha, alpha + 2, alpha + 1, colorf[0], colorf[1], colorf[2], 1.)
        fish.append_face(alpha, alpha + 7, alpha + 2, colorf[0], colorf[1], colorf[2], 1.)
        # ...back
        colorf = simple3d.getRandomColor()
        fish.append_face(alpha + 3, alpha + 4, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
        fish.append_face(alpha + 3, alpha + 5, alpha + 6, colorf[0], colorf[1], colorf[2], 1.)
        # ...left
        colorf = simple3d.getRandomColor()
        fish.append_face(alpha + 4, alpha + 7, alpha, colorf[0], colorf[1], colorf[2], 1.)
        fish.append_face(alpha + 4, alpha, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
        # ...right
        colorf = simple3d.getRandomColor()
        fish.append_face(alpha + 1, alpha + 3, alpha + 6, colorf[0], colorf[1], colorf[2], 1.)
        fish.append_face(alpha + 1, alpha + 2, alpha + 3, colorf[0], colorf[1], colorf[2], 1.)
        # ...top
        colorf = simple3d.getRandomColor()
        fish.append_face(alpha + 2, alpha + 4, alpha + 3, colorf[0], colorf[1], colorf[2], 1.)
        fish.append_face(alpha + 2, alpha + 7, alpha + 4, colorf[0], colorf[1], colorf[2], 1.)
        # ...bottom
        colorf = simple3d.getRandomColor()
        fish.append_face(alpha, alpha + 1, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
        fish.append_face(alpha + 1, alpha + 6, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
        
        alpha += 8

print('init...')
fish = simple3d.Simple3d()

num_liths = 24
# lith size
edge_w = 0.3
edge_h = 1.5
edge_d = 0.7
z_offset = 3.0

verticals(fish, num_liths, z_offset, edge_w, edge_h, edge_d)

v_offset = edge_h
edge_w = 1.15
edge_h = 0.3
edge_d = 0.7
num_plinths = math.floor(num_liths/2.0)
print(num_plinths, 'plinths')
plinths(fish, num_plinths, z_offset, v_offset, edge_w, edge_h, edge_d)

# object gets named after the script that made it
objname = sys.argv[0][0:-3]
fish.store_object("objects", objname)
# make a wavefront .obj version for Inkscape
fish.store_as_wf_obj("objects", objname + '.obj')

print('done.')