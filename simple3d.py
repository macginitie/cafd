import csv
import math
import random
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
   
    
def rotate(v, axis, angle):
   ax = axis.lower()
   if ax == 'x':
      return rotX(v, angle)
   elif ax == 'y':
      return rotY(v, angle)
   else:
      return rotZ(v, angle)
      

def getRandomColor() : 
   rgb = []
   rgb.append(random.random())
   rgb.append(random.random())
   rgb.append(random.random())
   return rgb
   

def getRandomDarkColor() : 
   rgb = []
   rgb.append(random.random()/2.)
   rgb.append(random.random()/2.)
   rgb.append(random.random()/2.)
   return rgb
   

def getRandomBlueColor() : 
   rgb = []
   rgb.append(random.random()/2.)
   rgb.append(random.random()/2.)
   rgb.append(random.random())
   return rgb

    
class Simple3d :
   "3d object representation & manipulation"
   # vertex coordinate indices
   XCOORD = 0
   YCOORD = 1
   ZCOORD = 2
   # face color indices
   F_RED = 3
   F_GREEN = 4
   F_BLUE = 5
   F_ALPHA = 6
   # edge color indices
   E_RED = 2
   E_GREEN = 3
   E_BLUE = 4
   E_ALPHA = 5
   
   
   def __init__(self, path=None, name=None) :
      self.name = name
      self.path = path
      self.edge = []
      self.face = []
      self.vertex = []
      self.normal = []
      
   
   def debug(self) :
      "print the object data"
      print( "name:", self.name )
      print( "path:", self.path )
      print( "edge:" )
      for e in self.edge :
         print( e[0], e[1], e[2], e[3], e[4], e[5] )
      print( "face:" )
      for f in self.face :
         print( f[0], f[1], f[2], f[3], f[4], f[5], f[6] )
      print( "vertex:" )
      for v in self.vertex :
         print( v[0], v[1], v[2] )
      print( "normal:" )
      for n in self.normal :
         print( n[0], n[1], n[2] )
         
      
   def read_vertices(self, vfile) :
      "read the list of x,y,z values from objname.vertices"
      reader = csv.reader(open(vfile, 'r'), delimiter=',')
      for row in reader :
         self.append_vertex( float(row[0]), float(row[1]), float(row[2]) )
         
   
   def read_edges(self, efile) :
      "read the list of edges from objname.edges"
      reader = csv.reader(open(efile, 'r'), delimiter=',')
      for row in reader :
         self.append_edge( int(row[0]), int(row[1]), (float(row[2]), float(row[3]), float(row[4]), float(row[5])) )
         
   
   def read_faces(self, ffile) :
      "read the list of faces from objname.faces"
      reader = csv.reader(open(ffile, 'r'), delimiter=',')
      for row in reader :
         print(row)
         self.append_face( int(row[0]), int(row[1]), int(row[2]), (float(row[3]), float(row[4]), float(row[5]), float(row[6])) )
         
   
   def compute_face_normals(self) :
      self.normal = []
      dbg_help = 0
      try :
         for f in self.face :
            # vector from 1st vertex in face to 2nd
            v1 = [self.vertex[f[0]][0] - self.vertex[f[1]][0], self.vertex[f[0]][1] - self.vertex[f[1]][1], self.vertex[f[0]][2] - self.vertex[f[1]][2]]
            # vector from 1st vertex in face to 3rd
            v2 = [self.vertex[f[0]][0] - self.vertex[f[2]][0], self.vertex[f[0]][1] - self.vertex[f[2]][1], self.vertex[f[0]][2] - self.vertex[f[2]][2]]
            # cross product (v1 X v2)
            abnrml = (v1[1]*v2[2] - v1[2]*v2[1], v1[2]*v2[0] - v1[0]*v2[2], v1[0]*v2[1] - v1[1]*v2[0])
            # Euclidean length for normalization
            vec_len = math.sqrt(abnrml[0]**2 + abnrml[1]**2 + abnrml[2]**2)
            self.append_normal(abnrml[0]/vec_len, abnrml[1]/vec_len, abnrml[2]/vec_len)
            dbg_help += 1
      except :
         print('error in face {0} of {1}'.format(dbg_help, len(self.face)-1))
         print(v1,v2,abnrml,vec_len)
         print(sys.exc_info()[0])


   def load_object(self, path, name) :
      "read object data from 3 related files"
      self.path = path
      self.name = name
      if path == None or len(path) == 0 :
         fname = name
      else :
         fname = path + name if path[-1] == '/' else path + '/' + name
      # open path/name.vertices
      self.read_vertices(fname + ".vertices")
      # open path/name.edges
      self.read_edges(fname + ".edges")
      # open path/name.faces
      self.read_faces(fname + ".faces")
      self.compute_face_normals()
      
      
   def store_object(self, path, name) :
      "write object data to 3 related files"
      self.path = path
      self.name = name
      if path == None or len(path) == 0 :
         fname = name
      else :
         fname = path + name if path[-1] == '/' else path + '/' + name
      # store path/name.vertices
      self.write_vertices(fname + ".vertices")
      # store path/name.edges
      self.write_edges(fname + ".edges")
      # store path/name.faces
      self.write_faces(fname + ".faces")
      
      
   def write_vertices(self, vfile) :
      "write the list of x,y,z values to objname.vertices"
      writer = csv.writer(open(vfile, 'w', newline=''), delimiter=',')
      for v in self.vertex :
         writer.writerow(v)
         
   
   def write_edges(self, efile) :
      "write the list of edges to objname.edges"
      writer = csv.writer(open(efile, 'w', newline=''), delimiter=',')
      for e in self.edge :
         writer.writerow(e)
         
   
   def write_faces(self, ffile) :
      "write the list of faces to objname.faces"
      writer = csv.writer(open(ffile, 'w', newline=''), delimiter=',')
      for f in self.face :
         writer.writerow(f)
         
   
   def store_as_wf_obj(self, path, name, type='f') :
      "write object data to single 'WaveFront'-format .obj file"
      self.path = path
      self.name = name
      if path == None or len(path) == 0 :
         fname = name
      else :
         fname = path + name if path[-1] == '/' else path + '/' + name
      # open output file
      with open(fname, 'w') as objfile :
         objfile.write('#Name:' + name + '\n')
         if (type == 'f') :
            objfile.write('#Type:face_specified\n')
         else :
            objfile.write('#Type:edge_specified\n')
         objfile.write('\n')   
         "write the list of x,y,z values to obj file"
         for v in self.vertex :
            objfile.write('v ' + str(v[0]) + ' ' + str(v[1]) + ' ' + str(v[2]) + '\n')
         objfile.write('\n')
         if (type == 'f') :
            for f in self.face :
               objfile.write('f ' + str(f[0]+1) + ' ' + str(f[1]+1) + ' ' + str(f[2]+1) + '\n')
         else :
            for e in self.edge :
               objfile.write('l ' + str(e[0]+1) + ' ' + str(e[1]+1) + '\n')
               
      
   def append_vertex(self, x, y, z) :
      "add a 3D point to the object"
      self.vertex.append([x, y, z])
      

   def append_edge(self, v1, v2, color=(0.0, 0.0, 0.0, 1.0)) :
      "add a pair of indices into the vertex list, which defines an edge"
      r,g,b,a = color
      self.edge.append([v1, v2, r, g, b, a])
      

   def append_face(self, v1, v2, v3, color) :
      "only triangles are currently supported"
      # r=0.5, g=0.5, b=0.5, a=1.0
      r,g,b,a = color
      self.face.append([v1, v2, v3, r, g, b, a])
      
      
   def append_normal(self, x, y, z) :
      "add a normal to the list of face normals"
      self.normal.append([x, y, z])
      

   def connect_last(self, color=(0.0, 0.0, 0.0, 1.0)) :
      "add an edge betwen the 2 most-recently-added vertices"
      r,g,b,a = color
      self.append_edge(len(self.vertex)-2, len(self.vertex)-1, (r, g, b, a))
      
      
   def rotate(self, axis, angle):
      if axis.lower() == 'y':
         self.rotY(angle)
      elif axis.lower() == 'z':  
         self.rotZ(angle)
      else:
         self.rotX(angle)      
         
         
   def rotX(self, angle) :
      "rotate object angle radians about the X axis"
      c = math.cos(angle)
      s = math.sin(angle)
      newV = []
      for v in self.vertex :        
         newY = v[1]*c - v[2]*s
         newZ = v[1]*s + v[2]*c
         newV.append([v[0], newY, newZ])
      self.vertex = newV
      self.compute_face_normals()
      
         
   def rotY(self, angle) :
      "rotate object angle radians about the Y axis"
      c = math.cos(angle)
      s = math.sin(angle)
      newV = []
      for v in self.vertex :        
         newX = v[0]*c - v[2]*s
         newZ = v[0]*s + v[2]*c
         newV.append([newX, v[1], newZ])
      self.vertex = newV
      self.compute_face_normals()
      
         
   def rotZ(self, angle) :
      "rotate object angle radians about the Z axis"
      c = math.cos(angle)
      s = math.sin(angle)
      newV = []
      for v in self.vertex :        
         newX = v[0]*c - v[1]*s
         newY = v[0]*s + v[1]*c
         newV.append([newX, newY, v[2]])
      self.vertex = newV
      self.compute_face_normals()
      
         
   def move(self, vector) :
      "displace object by vector"
      newV = []
      for v in self.vertex :        
         newX = v[0] + vector[0]
         newY = v[1] + vector[1]
         newZ = v[2] + vector[2]
         newV.append([newX, newY, newZ])
      self.vertex = newV
      newN = []
      for n in self.normal :        
         newX = n[0] + vector[0]
         newY = n[1] + vector[1]
         newZ = n[2] + vector[2]
         newN.append([newX, newY, newZ])
      self.normal = newN
      
      
   def z_sort(self, sort_type) :
      newF = []
      faceZ = []
      index = 0
      for f in self.face :
         if sort_type == "min" :
            zval = min(self.vertex[f[0]][2], self.vertex[f[1]][2])
            zval = min(zval, self.vertex[f[2]][2])
         elif sort_type == "max" :
            zval = max(self.vertex[f[0]][2], self.vertex[f[1]][2])
            zval = max(zval, self.vertex[f[2]][2])
         else :       # compute avg z value of @ face
            zval = (self.vertex[f[0]][2] + self.vertex[f[1]][2] + self.vertex[f[2]][2])/3.0
         faceZ.append([zval, index])
         index += 1
      # sort on zval
      faceZ.sort(key=lambda fz: fz[0], reverse=True)
      # normals must be sorted to match
      newN = []
      for f in faceZ :
         index = f[1]
         newF.append(self.face[index])
         if index < len(self.normal) :
            newN.append(self.normal[index])
      self.face = newF
      self.normal = newN
      
   
   # added lines are opaque black by default
   def extrude_linear(self, p0, p1, num_new_pts, red = 0.0, green = 0.0, blue = 0.0, alpha = 1.0) :
      "add vertices to object by 'extruding' along a line"
      # to do: faces
      dx = float(p1[0] - p0[0])/num_new_pts
      dy = float(p1[1] - p0[1])/num_new_pts
      dz = float(p1[2] - p0[2])/num_new_pts
      for i in range(num_new_pts+1) :
         self.append_vertex( i*dx + p0[0], i*dy + p0[1], i*dz + p0[2] )
         if (i > 0) :            
            self.connect_last(red, green, blue, alpha)
            
			
   def copy_vertices(self, first, last, vector, scale) :
      "copy a set of vertices, displaced by a vector & scaled"
      for i in range(first,last+1) :
         newPt = self.vertex[i]
         newX = (newPt[0] + vector[0])*scale
         newY = (newPt[1] + vector[1])*scale
         newZ = (newPt[2] + vector[2])*scale
         self.append_vertex(newX, newY, newZ)
         
		
   def copy_edges(self, first, last, offset) :
      "replicate a set of edges, offsetting @ vertex index"
      for i in range(first,last+1) :
         e = self.edge[i]
         self.append_edge(e[0]+offset, e[1]+offset, e[2], e[3], e[4], e[5])
         

   def getRandomColor(self) : 
      rgb = []
      rgb.append(random.random())
      rgb.append(random.random())
      rgb.append(random.random())
      return rgb
      
         
   def getRandomDarkColor(self) : 
      rgb = []
      rgb.append(random.random()/2.)
      rgb.append(random.random()/2.)
      rgb.append(random.random()/2.)
      return rgb
      

   def getRandomBlueColor(self) : 
      rgb = []
      rgb.append(random.random()/2.)
      rgb.append(random.random()/2.)
      rgb.append(random.random())
      return rgb
      

   def assign_random_colors(self) :
      "assign a random color to each edge & each face"
      for e in self.edge :
         color = getRandomColor()
         e[2] = color[0]
         e[3] = color[1]
         e[4] = color[2]
         # alpha         
      for f in self.face :
         color = getRandomColor()
         f[3] = color[0]
         f[4] = color[1]
         f[5] = color[2]
         # alpha         
         

   def assign_random_dark_colors(self) :
      "assign a random 'dark' color to each edge & each face"
      for e in self.edge :
         color = getRandomDarkColor()
         e[self.E_RED] = color[0]
         e[self.E_GREEN] = color[1]
         e[self.E_BLUE] = color[2]
         # alpha         
      for f in self.face :
         color = getRandomDarkColor()
         f[self.F_RED] = color[0]
         f[self.F_GREEN] = color[1]
         f[self.F_BLUE] = color[2]
         # alpha         
         
         
   def assign_random_blue_colors(self) :
      "assign a random 'blue-ish' color to each edge & each face"
      for e in self.edge :
         color = getRandomBlueColor()
         e[self.E_RED] = color[0]
         e[self.E_GREEN] = color[1]
         e[self.E_BLUE] = color[2]
         # alpha         
      for f in self.face :
         color = getRandomBlueColor()
         f[self.F_RED] = color[0]
         f[self.F_GREEN] = color[1]
         f[self.F_BLUE] = color[2]
         # alpha         
         
   
   def assign_grey_shade(self, eye_coord) :
      """ 
      assign a shade of grey to each face based on the angle
      between the face normal & vector from face to 'eye' coords 
      """
      index = 0
      print('calcul8ing ' + str(len(self.face)) + ' dot products... ', end='')
      # TODO: time 
      # ts = 
      for f in self.face :         
         f_center_x = (self.vertex[f[0]][0] + self.vertex[f[1]][0] + self.vertex[f[2]][0]) / 3.0
         f_center_y = (self.vertex[f[0]][1] + self.vertex[f[1]][1] + self.vertex[f[2]][1]) / 3.0
         f_center_z = (self.vertex[f[0]][2] + self.vertex[f[1]][2] + self.vertex[f[2]][2]) / 3.0
         eye_vector = (eye_coord[0] - f_center_x, eye_coord[1] - f_center_y, eye_coord[2] - f_center_z)
         eye_vector_mag = math.sqrt(eye_vector[0]*eye_vector[0] + eye_vector[1]*eye_vector[1] + eye_vector[2]*eye_vector[2])
         normal_mag = math.sqrt(self.normal[index][0]*self.normal[index][0] + self.normal[index][1]*self.normal[index][1] + self.normal[index][2]*self.normal[index][2])
         # dot_product
         dot_product = eye_vector[0]*self.normal[index][0] + eye_vector[1]*self.normal[index][1] + eye_vector[2]*self.normal[index][2]
         # cos(theta) where theta is the angle between the face normal & vector from face to 'eye' coords
         dot_product /= (eye_vector_mag*normal_mag)
         # print(dot_product)
         # to do: map better?
         # if dot_product < 0.0 : dot_product *= -1.0
         if dot_product > 1.0 : 
            shade = 1.0 
         elif dot_product < -1.0 :
            shade = -1.0
         else : 
            shade = dot_product
         self.face[index][self.F_RED] = shade
         self.face[index][self.F_GREEN] = shade
         self.face[index][self.F_BLUE] = shade
         index += 1
      print('completed.')
      
         
   def assign_aqua_shade(self, eye_coord) :
      """ 
      assign a shade of aqua (blue-green) to each face based on the angle
      between the face normal & vector from face to 'eye' coords 
      """
      index = 0
      print('calcul8ing ' + str(len(self.face)) + ' dot products')
      for f in self.face :         
         f_center_x = (self.vertex[f[0]][0] + self.vertex[f[1]][0] + self.vertex[f[2]][0]) / 3.0
         f_center_y = (self.vertex[f[0]][1] + self.vertex[f[1]][1] + self.vertex[f[2]][1]) / 3.0
         f_center_z = (self.vertex[f[0]][2] + self.vertex[f[1]][2] + self.vertex[f[2]][2]) / 3.0
         eye_vector = (eye_coord[0] - f_center_x, eye_coord[1] - f_center_y, eye_coord[2] - f_center_z)
         eye_vector_mag = math.sqrt(eye_vector[0]*eye_vector[0] + eye_vector[1]*eye_vector[1] + eye_vector[2]*eye_vector[2])
         normal_mag = math.sqrt(self.normal[index][0]*self.normal[index][0] + self.normal[index][1]*self.normal[index][1] + self.normal[index][2]*self.normal[index][2])
         # dot_product
         dot_product = eye_vector[0]*self.normal[index][0] + eye_vector[1]*self.normal[index][1] + eye_vector[2]*self.normal[index][2]
         # cos(theta) where theta is the angle between the face normal & vector from face to 'eye' coords
         dot_product /= (eye_vector_mag*normal_mag)
         # print(dot_product)
         # to do: map better?
         # if dot_product < 0.0 : dot_product *= -1.0
         if dot_product > 1.0 : 
            shade = 1.0 
         elif dot_product < -1.0 :
            shade = -1.0
         else : 
            shade = dot_product
         self.face[index][self.F_RED] = 0.0 if (shade >= 0.0) else -0.001  # since the cafd screen b.g. is "light" make this dark for contrast
         self.face[index][self.F_GREEN] = shade
         self.face[index][self.F_BLUE] = shade
         index += 1
      print('calcul8d ' + str(len(self.face)) + ' dot products')
      
      
   def replitranslacate(self, vector) :
      # add a copy displaced by vector = replicate + translate
      vlen = len(self.vertex)
      for i in range(vlen) :
         self.append_vertex(self.vertex[i][0] + vector[0], self.vertex[i][1] + vector[1], self.vertex[i][2] + vector[2])        
      for i in range(len(self.edge)) :
         self.append_edge(self.edge[i][0] + vlen, self.edge[i][1] + vlen, self.edge[i][2], self.edge[i][3], self.edge[i][4], self.edge[i][5])
      for i in range(len(self.face)) :
         self.append_face(self.face[i][0] + vlen, self.face[i][1] + vlen, self.face[i][2] + vlen, self.face[i][3], self.face[i][4], self.face[i][5], self.face[i][6])
         
         
   def repliscalecate(self, vector) :
      # add a copy scaled by vector = replicate + scale
      vlen = len(self.vertex)
      for i in range(vlen) :
         self.append_vertex(self.vertex[i][0] * vector[0], self.vertex[i][1] * vector[1], self.vertex[i][2] * vector[2])        
      for i in range(len(self.edge)) :
         self.append_edge(self.edge[i][0] + vlen, self.edge[i][1] + vlen, self.edge[i][2], self.edge[i][3], self.edge[i][4], self.edge[i][5])
      for i in range(len(self.face)) :
         self.append_face(self.face[i][0] + vlen, self.face[i][1] + vlen, self.face[i][2] + vlen, self.face[i][3], self.face[i][4], self.face[i][5], self.face[i][6])
         

   def assimilate(self, other) :
      vlen = len(self.vertex)
      for v in other.vertex :
         self.append_vertex(v[0], v[1], v[2])
      for f in other.face :
         self.append_face(f[0] + vlen, f[1] + vlen, f[2] + vlen, f[3], f[4], f[5], f[6])
      for e in other.edge :
         self.append_edge(e[0] + vlen, e[1] + vlen, e[2], e[3], e[4], e[5])
         
         
   def bounding_box(self) :
      xrange = [0,0]
      yrange = [0,0]
      zrange = [0,0]
      for v in self.vertex:
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
      return (xrange, yrange, zrange) 
      

if __name__ == '__main__' :
   o = Simple3d()
   o.load_object('objects', 'test')
   o.debug()
   o.z_sort()
   o.debug()
   
   print( 'extrude 0,0,0 to 2,2,2 in 3' )
   o = Simple3d()
   o.extrude_linear( (0,0,0), (2.0,2.0,2.0), 3 )
   o.debug()
   
   print( 'extrude 0,0,0 to -2,-2,-2 in 3, red' )
   o.extrude_linear( (0,0,0), (-2.0,-2.0,-2.0), 3, 1.0, 0.0, 0.0, 1.0 )
   o.debug()
   
   # save number of vertices so far
   nv = len(o.vertex)
   print( 'copy vertices 0 through 3 displacing (2.0,0.0,0.0) scaling 1.2' )  
   o.copy_vertices(0,3,(2.0,0.0,0.0), 1.2)
   
   print( 'copy edges 0 through 2, offset by (#vertices)' )  
   o.copy_edges(0,2,nv)
   o.debug()
   o.store_object('objects', 'tst2')
