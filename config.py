#! /usr/bin/env python

import os.path

class CafdConfig :

   cfg_file_name = 'cafd.config' # default name
   
   def __init__(self) :
      if os.path.exists(self.cfg_file_name) :
         cfgfile = open(self.cfg_file_name)
         self.path_4_obj_files = cfgfile.read()
         
   def obj_path(self) :
      return self.path_4_obj_files