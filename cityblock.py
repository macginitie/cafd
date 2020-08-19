#!/usr/bin/python

import config
import random
import simple3d
import sys

class Bldg :

    def __init__(self, width, height, depth, anchor_pt) :
        self.vertex = []
        self.face = []
        self.edge = []
        # foundation
        self.vertex.append(anchor_pt)
        self.vertex.append([anchor_pt[0] + width, anchor_pt[1], anchor_pt[2]])
        self.vertex.append([anchor_pt[0], anchor_pt[1], anchor_pt[2] + depth])
        self.vertex.append([anchor_pt[0] + width, anchor_pt[1], anchor_pt[2] + depth])
        self.edge.append([0,1,0.,0.,0.2,1.])
        self.edge.append([0,2,0.,0.,0.2,1.])
        self.edge.append([2,3,0.,0.,0.2,1.])
        self.edge.append([3,1,0.,0.,0.2,1.])
        # roof
        self.vertex.append([anchor_pt[0], anchor_pt[1] + height, anchor_pt[2]])
        self.vertex.append([anchor_pt[0] + width, anchor_pt[1] + height, anchor_pt[2]])
        self.vertex.append([anchor_pt[0], anchor_pt[1] + height, anchor_pt[2] + depth])
        self.vertex.append([anchor_pt[0] + width, anchor_pt[1] + height, anchor_pt[2] + depth])
        self.edge.append([4,5,0.,0.,0.2,1.])
        self.edge.append([4,6,0.,0.,0.2,1.])
        self.edge.append([6,7,0.,0.,0.2,1.])
        self.edge.append([7,5,0.,0.,0.2,1.])
        # wall corners
        self.edge.append([0,4,0.,0.,0.2,1.])
        self.edge.append([1,5,0.,0.,0.2,1.])
        self.edge.append([2,6,0.,0.,0.2,1.])
        self.edge.append([3,7,0.,0.,0.2,1.])
        # walls
        # front
        self.face.append([0,5,1,0.8,0.8,0.8,1.])
        self.face.append([5,0,4,0.8,0.8,0.8,1.])
        # left
        self.face.append([0,2,4,0.8,0.8,0.8,1.])
        self.face.append([2,6,4,0.8,0.8,0.8,1.])
        # right
        self.face.append([1,5,7,0.8,0.8,0.8,1.])
        self.face.append([7,3,1,0.8,0.8,0.8,1.])
        # top
        self.face.append([5,4,6,0.8,0.8,0.8,1.])
        self.face.append([5,6,7,0.8,0.8,0.8,1.])
        # back
        self.face.append([3,7,6,0.8,0.8,0.8,1.])
        self.face.append([3,6,2,0.8,0.8,0.8,1.])
        # the building has no floor
        
        
if __name__ == '__main__' :
    
    num_bldgs = 10
    if len(sys.argv) > 1 :
        num_bldgs = int(sys.argv[1])
        
    ground_level = -3.
    min_height = 1.    
    max_height = 10.
    min_width = 2.
    max_width = 10.
    min_depth = 2.
    max_depth = 10.
    
    start = -10.
    spacing = 2.
        
    city = simple3d.Simple3d()   
    
    for i in range(num_bldgs) :
        for j in range(num_bldgs) :
            width = min_width + random.random() * max_width
            depth = min_depth + random.random() * max_depth
            height = min_height + random.random() * max_height
            bldg = Bldg(width, height, depth, [start + i*spacing, ground_level, start + j*spacing])
            city.assimilate(bldg)
    
    # object gets named after the script that made it
    objname = sys.argv[0][0:-3]
    city.store_object("objects", objname)
    # make a "wavefront" .obj version for Inkscape
    cfg = config.CafdConfig()
    city.store_as_wf_obj(cfg.obj_path(), objname + '.obj')
    