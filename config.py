#! /usr/bin/env python

import os.path

class CafdConfig :

   cfg_file_name = 'cafd.config' # default name
   
   def __init__(self) :
      if os.path.exists(self.cfg_file_name) :
         cfgfile = open(self.cfg_file_name)
         config = cfgfile.read().split('\n')
         self.path_4_obj_files = config[0]
         self.screendim = config[1].split(',')
         
   def obj_path(self) :
      return self.path_4_obj_files
      
   def screen_width(self) :
      return self.screendim[0]

   def screen_height(self) :
      return self.screendim[1]