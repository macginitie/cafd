#! /usr/bin/env python

import bspline
import os.path
import numpy as np
import pygame
import sys
  
  
def screen_pt(worldx, worldy):
    global world
    global viewport
    left, top, right, bottom = 0,1,2,3
    vpx = ((worldx - world[left]) / (world[right] - world[left])) * (viewport[right] - viewport[left]) + viewport[left]
    vpy = ((worldy - world[bottom]) / (world[top] - world[bottom])) * (viewport[top] - viewport[bottom]) + viewport[bottom]
    return (vpx, vpy)
    
    
def save_spline(bsx, bsy):
    with open('bspline-pt-list.txt', 'w') as splinefile :
        for i in range(len(bsx)):
            print(bsx[i], bsy[i])
            splinefile.write(str(bsx[i]) + ',' + str(bsy[i]) + '\n')
    

def draw_ctl_pts(screen, ctr):    
    for i in range(len(ctr)):
        pygame.draw.aaline(screen, (255,0,0), screen_pt(ctr[i,0]-0.1, ctr[i,1]), screen_pt(ctr[i,0]+0.1, ctr[i,1]) )
        pygame.draw.aaline(screen, (255,0,0), screen_pt(ctr[i,0], ctr[i,1]-0.1), screen_pt(ctr[i,0], ctr[i,1]+0.1) )
    
# initial settings

# window dimensions
w = 900
h = 900
# xmin, ymax, xmax, ymin = (l,t,r,b)
viewport = (0, 0, w, h)
# xmin, ymax, xmax, ymin = (l,t,r,b)
world = (-5.0, 5.0, 5.0, -5.0)

# default initial control points
ctr = np.array( [(-3.5 , -4.0), (-2.5, -4.5), (0.0, 0.0), (2.5, 4.5), (3.5, 4.0),] )
selected_pt = 0

# slightly off-white background
bgcolor = (0xf5,0xf5,0xf5)
splinecolor = (0, 0, 0x0f)
# erase between frames
erase = True
# CPU throttle (larger value ==> less CPU hogging)
delay = 200
# key repeat delay, interval
key_delay = 20
key_interval = 20
# displacement per key press for x, y
incr = 0.05

# using +1 here to avoid using -1 elsewhere
screen = pygame.display.set_mode((w+1, h+1))
clock = pygame.time.Clock()
pygame.key.set_repeat(key_delay, key_interval)

# debug
#print(bsx)
#print(bsy)
#print(screen_pt(bsx[0], bsy[0]), screen_pt(bsx[-1],bsy[-1]))

recalc_needed = True

running = True
while running:
    for event in pygame.event.get() :
   
        if event.type == pygame.QUIT :
            running = False
         
        elif event.type == pygame.KEYUP :
      
            if event.key == pygame.K_d :
                # delete current pt., if more than 3 pts.
                if len(ctr) > 3:
                    new = []
                    for i in range(len(ctr)):
                        if (i != selected_pt):
                            new.append(ctr[i])
                    ctr = np.array(new)
                    recalc_needed = True
            elif event.key == pygame.K_h :
                print( '================================================================================' )
                print( '         d: delete selected control point' )
                print( '         h: show this help info' )
                print( '         i: insert new control point' )
                print( '         n: select next control point (modulo #pts)' )
                print( '         p:   "    previous "     "      "      "  ' )
                print( '         q: quit' )
                print( '         s: save spline points' )
                print( '      x(X): move selected control point left(RIGHT)' )
                print( '      y(Y): move selected control point up(DOWN)' )
                print( 'arrow keys: move selected control point left, right, up, down ( -x, +x, +y, -y )' )
                print( '================================================================================' )
            elif event.key == pygame.K_i :
                # insert new control point 
                new = []
                for i in range(len(ctr)):
                    new.append(ctr[i])
                    if (i == selected_pt):
                        # "adjacent to" selected pt
                        new.append((ctr[i,0]+incr, ctr[i,1]+incr))
                ctr = np.array(new)
                # select the new point
                selected_pt += 1
                recalc_needed = True
            elif event.key == pygame.K_n :
                # next pt.
                selected_pt = (1 + selected_pt) % len(ctr)
            elif event.key == pygame.K_p :
                # previous pt.
                selected_pt = (selected_pt - 1) % len(ctr)
            elif event.key == pygame.K_s :
                # save spline points
                save_spline(bsx, bsy)
                print('saved spline pts to "bspline-pt-list.txt"')
            
        elif event.type == pygame.KEYDOWN :

            # x,y,z and X,Y,Z and the arrow keys are processed on key DOWN
      
            current_unicode = event.unicode
            if event.key == pygame.K_q : 
                # quit
                running = False
            elif event.key == pygame.K_x : 
                if current_unicode == "X" :
                    # move selected control point right
                    ctr[selected_pt,0] += incr
                else :
                    # move selected control point left
                    ctr[selected_pt,0] -= incr
                recalc_needed = True
            elif event.key == pygame.K_y : 
                if current_unicode == "Y" :
                    # move selected control point down
                    ctr[selected_pt,1] -= incr
                else :
                    # move selected control point up
                    ctr[selected_pt,1] += incr
                recalc_needed = True
            elif event.key == pygame.K_UP :
                # move selected control point up
                ctr[selected_pt,1] += incr
                recalc_needed = True
            elif event.key == pygame.K_DOWN :
                # move selected control point down
                ctr[selected_pt,1] -= incr
                recalc_needed = True
            elif event.key == pygame.K_LEFT :
                # move selected control point left
                ctr[selected_pt,0] -= incr
                recalc_needed = True
            elif event.key == pygame.K_RIGHT :
                # move s.c.p. right
                ctr[selected_pt,0] += incr
                recalc_needed = True
         
        if erase :
            screen.fill(bgcolor)
            
        if recalc_needed:
            recalc_needed = False
            x = ctr[:,0]
            y = ctr[:,1]
            out = bspline.b_spline(x,y,False)

            bsx = out[0]
            bsy = out[1]
            
        draw_ctl_pts(screen, ctr)
            
        for idx in range(len(bsx) - 1):
            pygame.draw.aaline(screen, splinecolor, screen_pt(bsx[idx], bsy[idx]), screen_pt(bsx[idx+1],bsy[idx+1]) )

        # double buffering
        pygame.display.flip()
   
    # sleep   
    clock.tick(delay)
