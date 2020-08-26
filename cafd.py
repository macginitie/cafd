#! /usr/bin/env python

import config
import os.path
import pygame
import simple3d
import sys
import view3d
# ... when fits of creativity run strong, more than one programmer or writer 
# has been known to abandon the desktop for the more spacious floor. -- Fred Brooks
from math import floor

def makeRGB(r,g,b) :
   return (floor(r*255),floor(g*255),floor(b*255))

if len(sys.argv) < 2 :
   print( "usage: cafd.py object" )
   print( "where object names a set of 3 files in the objects subfolder," )
   print( "to wit:" )
   print( "objects/object.faces" )
   print( "objects/object.edges" )
   print( "objects/object.vertices" )
   exit()
   
# read path for .obj output from cafd.config   
cfg = config.CafdConfig()
obj_path = cfg.obj_path()
# window dimensions
w = int(cfg.screen_width())  # 900
h = int(cfg.screen_height())  # 900
   
# initial settings
outline_width = 0
wireframe = True
erase = True
move_eye = False
cull_backfaces = True
debug = False

# slightly off-white background
bgcolor = (0xf5,0xf5,0xf5)
# CPU throttle (larger value ==> less CPU hogging)
delay = 200
# key repeat delay, interval
key_delay = 20
key_interval = 20
# radians per key press for rotations
theta = 0.025   # 4.5 degrees
# displacement per key press for i, o
incr = 0.05

fish = simple3d.Simple3d()

fish.load_object("objects", sys.argv[1])
xrange, yrange, zrange = fish.bounding_box()
print('xrange:', xrange, ', yrange:', yrange, ', zrange:', zrange)
xmax = max(abs(xrange[0]), abs(xrange[1]))
ymax = max(abs(yrange[0]), abs(yrange[1]))
zmax = max(abs(zrange[0]), abs(zrange[1]))
maxw = max(xmax, ymax)
maxw = max(zmax, maxw)
eye = (0.0, 0.0, -25.0)
# screen (l,t,r,b), viewport (l,t,r,b), world "frustum" (really a box), eye (x,y,z), distance from eye to screen
#view = view3d.View3d((0,0, w,h), (-10.0,10.0, 10.0,-10.0), (-10.0, 10.0, -10.0, 10.0, -10.0, 10.0), eye, 7.0)
view = view3d.View3d((0,0, w,h), (-maxw, maxw, maxw, -maxw), (-10.0, 10.0, -10.0, 10.0, -10.0, 10.0), eye, 2 * zrange[1])

if debug :
   fish.debug()
   view.debug()

# using +1 here to avoid using -1 elsewhere
screen = pygame.display.set_mode((w+1, h+1))
clock = pygame.time.Clock()
pygame.key.set_repeat(key_delay, key_interval)
sort_mode = "min"
move_eye = True
running = True

while running:
   for event in pygame.event.get() :
   
      if event.type == pygame.QUIT :
         running = False
         
      elif event.type == pygame.KEYUP :
      
         # current list of recognized keys: a,b,c,d,e,f,h,i,l,o,q,r,s,u,w,x,y,z (and the 4 arrows)
         # current list of differenti8d capitals: B,C,D,F,X,Y,Z

         # a,b,c,d,e,f,h,l,r,s,u,w and B,C,D,F are processed on key UP
         
         if event.key == pygame.K_a :
            wireframe = False
            fish.assign_aqua_shade(eye)
         elif event.key == pygame.K_b :
            if current_unicode == "B" :
               cull_backfaces = not cull_backfaces
            else :
               fish.assign_random_blue_colors()
         elif event.key == pygame.K_c :
            if current_unicode == "C" :
               fish.assign_random_dark_colors()
            else :
               fish.assign_random_colors()           
         elif event.key == pygame.K_d :
            if current_unicode == "D" :
                # debug the object
                fish.debug()
            else :
                # toggle debug flag
                debug = not debug
         elif event.key == pygame.K_e :
            if current_unicode == "e" :
                # toggle bg erase
                erase = not erase
            else :
                # toggle move command target between eye & object
                move_eye = not move_eye
         elif event.key == pygame.K_f :
            if current_unicode == "f" :
               outline_width += 1
            else :
               if outline_width > 0 :
                outline_width -= 1
         elif event.key == pygame.K_h :
            print( '===============================================================================' )
            print( '         a: aqua-colorize (show monochrome pseudo-shaded with blue-green tint)' )
            print( '         b: colorize (replace all edge & face colors with random "blue" colors)' )
            print( '         B: turn ' + ('off' if cull_backfaces else 'on') + ' backface culling' )
            print( '         c: colorize (replace all edge & face colors with random colors)' )
            print( '         C: colorize (replace all edge & face colors with random "dark" colors)' )
            print( '         d: turn ' + ('off' if debug else 'on') + ' debugging info' )
            print( '         D: debug (i.e., print the current state of the object to the console)' )
            print( '         e: toggle erase-between-frames' )
            print( '         E: switch to ' + ('move object' if move_eye else 'move "eye"') + ' mode for [i]n/[o]ut' )
            print( '         f: increase the width of (fatten) the polygon outlines' )
            print( '         F: decrease the width of (or remove) the polygon outlines' )
            print( '      h(H): print this help info' )
            print( '      i(I): (in) move object toward viewer ( -z )' )
            print( '         l: (re)load object (restore original orientation & colors)' )
            print( '      o(O): (out) move object away from viewer ( +z )' )
            print( '         q: quit' )
            print( '         r: record object to file (appends "-new" to original name)' )
            print( '         s: change z-sort mode (min, max, avg)' )
            print( '         u: un-colorize (show monochrome pseudo-shaded)' )
            print( '         v: vectorize (record object to .svg file representation)' )
            print( '         w: toggle between wireframe & "solid" representation' )
            print( '         W: write object as Wavefront .obj file' )
            print( '      x(X): rotate cw(CCW) about the x axis' )
            print( '      y(Y): rotate cw(CCW) about the y axis' )
            print( '      z(Z): rotate cw(CCW) about the z axis' )
            print( 'arrow keys: move object left, right, up, down ( -x, +x, +y, -y )' )
            print( '===============================================================================' )
         elif event.key == pygame.K_l :
            # reload the object
            fish = simple3d.Simple3d()
            fish.load_object("objects", sys.argv[1])
         elif event.key == pygame.K_r :
            # record the object
            fish.store_object("objects", sys.argv[1] + "-new")
         elif event.key == pygame.K_s :
            # change sort mode
            if sort_mode == "min" :
               sort_mode = "max"
            elif sort_mode == "max" :
               sort_mode = "avg"
            else :
               sort_mode = "min"
            print( "sort_mode = %s" % sort_mode )
         elif event.key == pygame.K_u :
            wireframe = False
            fish.assign_grey_shade(eye)
         elif event.key == pygame.K_v :
            # record the object
            fish.store_object("objects", sys.argv[1] + "-svg")
         elif event.key == pygame.K_w :
            if current_unicode == 'W' :
               fish.store_as_wf_obj(obj_path, sys.argv[1] + ".obj")
               print('object saved to ' + obj_path + sys.argv[1] + ".obj")
            else :
               # toggle wireframe
               wireframe = not wireframe
            
      elif event.type == pygame.KEYDOWN :

         # i,o,x,y,z and X,Y,Z and the arrow keys are processed on key DOWN
      
         current_unicode = event.unicode
         if event.key == pygame.K_i :
            factor = 1.0
            if event.unicode == "I" : factor = 10.0
            # zoom in
            if move_eye :
               view.distance += (factor * incr)
               if debug : print( view.distance )
            else :
               fish.move((0.0, 0.0, -(factor * incr)))
         elif event.key == pygame.K_o :
            factor = 1.0
            if event.unicode == "O" : factor = 10.0
            # zoom out
            if move_eye :
               view.distance -= (factor * incr)
               if debug : print( view.distance )
            else :
               fish.move((0.0, 0.0, (factor * incr)))
         elif event.key == pygame.K_q : 
            # quit
            running = False
         elif event.key == pygame.K_x : 
            # rotate theta radians around X axis
            if event.unicode == "X" :
               # counterclockwise, viewed from +x perspective
               fish.rotX(-theta)
            else :            
               # clockwise, viewed from +x perspective
               fish.rotX(theta)
         elif event.key == pygame.K_y : 
            # rotate theta radians around Y axis
            if event.unicode == "Y" :
               # counterclockwise, viewed from above (+y)
               fish.rotY(-theta)
            else :            
               # clockwise, viewed from above (+y)
               fish.rotY(theta)
         elif event.key == pygame.K_z :
            # rotate theta radians around Z axis 
            if event.unicode == "Z" :
               # counterclockwise, from viewer's perspective
               fish.rotZ(-theta)
            else :            
               # clockwise, from viewer's perspective
               fish.rotZ(theta)
         elif event.key == pygame.K_UP :
            # move up
            fish.move((0.0, incr, 0.0))
         elif event.key == pygame.K_DOWN :
            # move down
            fish.move((0.0, -incr, 0.0))
         elif event.key == pygame.K_LEFT :
            # move left
            fish.move((-incr, 0.0, 0.0))
         elif event.key == pygame.K_RIGHT :
            # move right
            fish.move((incr, 0.0, 0.0))
         
      if erase :
         screen.fill(bgcolor)

      if wireframe :
         for e in fish.edge :
            pygame.draw.aaline(screen, makeRGB(e[2], e[3], e[4]), view.v2s(view.w2v(fish.vertex[e[0]])), view.v2s(view.w2v(fish.vertex[e[1]])))
            if debug :
               print( fish.vertex[e[0]], fish.vertex[e[1]] )
               print( view.w2v(fish.vertex[e[0]]), view.w2v(fish.vertex[e[1]]) )
               print( view.v2s(view.w2v(fish.vertex[e[0]])), view.v2s(view.w2v(fish.vertex[e[1]])) )
               debug = False
      else :
         # z-sort faces
         fish.z_sort(sort_mode)
         for f in fish.face :
            # -1 in f[3] is a kludge to flag "backfaces"
            if cull_backfaces :
                if (f[3] >= 0) :
                    pygame.draw.polygon(screen, makeRGB(f[3], f[4], f[5]), [view.v2s(view.w2v(fish.vertex[f[0]])), view.v2s(view.w2v(fish.vertex[f[1]])), view.v2s(view.w2v(fish.vertex[f[2]]))], outline_width)
            else :
                if (f[3] >= 0) :
                    pygame.draw.polygon(screen, makeRGB(f[3], f[4], f[5]), [view.v2s(view.w2v(fish.vertex[f[0]])), view.v2s(view.w2v(fish.vertex[f[1]])), view.v2s(view.w2v(fish.vertex[f[2]]))], outline_width)
                else :
                    try :
                        pygame.draw.polygon(screen, makeRGB(-f[3], -f[4], -f[5]), [view.v2s(view.w2v(fish.vertex[f[0]])), view.v2s(view.w2v(fish.vertex[f[1]])), view.v2s(view.w2v(fish.vertex[f[2]]))], outline_width)
                    except :
                        print(f[3] if f[3] >= 0 else -f[3], f[4], f[5])
                        print( makeRGB(f[3] if f[3] >= 0 else -f[3], f[4], f[5]))
                        exit()
   
      pygame.display.flip()
   
   # sleep   
   clock.tick(delay)

