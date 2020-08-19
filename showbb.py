#!/usr/bin/env python

import simple3d
import sys

fish = simple3d.Simple3d()

fish.load_object("objects", sys.argv[1])
print('loaded', len(fish.face), 'faces')

xrange = [0,0]
yrange = [0,0]
zrange = [0,0]

for v in fish.vertex:
    # X
    if v[0] < xrange[0]:
        xrange[0] = v[0]
    elif v[0] > xrange[1]:
        xrange[1] = v[0]
    # Y
    if v[1] < yrange[0]:
        yrange[0] = v[1]
    elif v[1] > yrange[1]:
        yrange[1] = v[1]
    # Z
    if v[2] < zrange[0]:
        zrange[0] = v[2]
    elif v[2] > zrange[1]:
        zrange[1] = v[2]
        
print('X:', xrange, 'Y:', yrange, 'Z:', zrange)        
        