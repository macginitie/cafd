#! /usr/bin/env python

import simple3d
import random
import math
import sys

def modulo_color_bw(pt_no):
    if (pt_no % 2) == 0:
        return (0., 0., 0.)
    else:
        return (0.9, 0.9, 0.9)
        
colors = [(1.,0.,0.), (1.,1.,0.), (0.,1.,0.), (1.,1.,1.), (0.,1.,1.), (0.,0.,1.), (1.,0.,1.), (0.,0.,0.)]
        
def modulo_color_stripes(pt_no):
    value = colors[pt_no % len(colors)]
    return (value[0], value[1], value[2])
        
munge_list = ['bw', 'stripes', 'scale', 'zscale', 'warp', 'warpscale']

if len(sys.argv) < 3 :
   print( "usage:\npython", sys.argv[0], "object munge1 [munge2...] {munge_param}" )
   print( "where object names a set of files in the objects subfolder," )
   print( "to wit:" )
   print( "objects/object.faces" )
   print( "objects/object.edges" )
   print( "objects/object.vertices" )
   print( "\nand mungeN is in", munge_list )
   print('{munge_param} is optional, depends on the particular munge used')
   exit()
   
#bgcolor = (0xf5,0xf5,0xf5) # default cafd bg

fish = simple3d.Simple3d()

fish.load_object("objects", sys.argv[1])
print('loaded', len(fish.face), 'faces')

munges = []
for i in range(2, len(sys.argv)):
    munges.append(sys.argv[i])
    
if 'bw' in munges:
    index = 0
    for f in fish.face:
        color = modulo_color_bw(index)
        f[fish.F_RED] = color[0]
        f[fish.F_GREEN] = color[1]
        f[fish.F_BLUE] = color[2]
        index += 1
        
if 'stripes' in munges:
    index = 0
    for f in fish.face:
        color = modulo_color_stripes(index)
        f[fish.F_RED] = color[0]
        f[fish.F_GREEN] = color[1]
        f[fish.F_BLUE] = color[2]
        index += 1
        
if 'scale' in munges:
    factor = float(munges[-1]) # TO DO: cmdln option processing
    for i in fish.vertex:
        i[0] *= factor
        i[1] *= factor
        i[2] *= factor
        
if 'zscale' in munges:
    factor = float(munges[-1]) # TO DO: cmdln option processing
    for i in fish.vertex:
        i[2] *= factor
        
if 'warp' in munges:
    factor = float(munges[-1]) # TO DO: cmdln option processing
    for i in fish.vertex:
        for coord in range(3):
            i[coord] += (0.5 - random.random())*factor
            
if 'warpscale' in munges:
    factor = float(munges[-1]) # TO DO: cmdln option processing
    for i in fish.vertex:
        for coord in range(3):
            i[coord] *= (factor + (0.5 - random.random()))

# record the munged object
fname = sys.argv[1]
for arg in sys.argv[2:]:
    fname += ('-' + arg)
fish.store_object("objects", fname)

        