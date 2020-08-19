cafd
====

computer-aided fish design

This is a simplistic "3D" object viewer written in Python, which relies on pygame.

Despite the name, it does not (yet) provide a user interface for designing objects, only for viewing them.

here is an excerpt of the code:

    if len(sys.argv) < 2 :
        print( "usage: cafd.py object" )
        print( "where object names a set of files in the objects subfolder," )
        print( "to wit:" )
        print( "objects/object.faces" )
        print( "objects/object.edges" )
        print( "objects/object.vertices" )
        exit()

here is another excerpt:

         elif event.key == pygame.K_h :
            print( '===============================================================================' )
            print( '         a: aqua-colorize (show monochrome pseudo-shaded with blue-green tint)' )
            print( '         b: colorize (replace all edge & face colors with random "blue" colors)' )
            print( '         c: colorize (replace all edge & face colors with random colors)' )
            print( '         C: colorize (replace all edge & face colors with random "dark" colors)' )
            print( '         d: debug (print the object data to the console)' )
            print( '         e: toggle erase-between-frames' )
            print( '         f: increase the width of (fatten) the polygon outlines' )
            print( '         F: decrease the width of (or remove) the polygon outlines' )
            print( '      h(H): print this help info' )
            print( '         i: (in) move object toward viewer ( -z )' )
            print( '         l: (re)load object (restore original orientation & colors)' )
            print( '         o: (out) move object away from viewer ( +z )' )
            print( '         q: quit' )
            print( '         r: record object to file (appends "-new" to original name)' )
            print( '         s: change z-sort mode (min, max, avg)' )
            print( '         u: un-colorize (show monochrome pseudo-shaded)' )
            print( '         v: vectorize (record object to .svg file representation)' )
            print( '         w: toggle between wireframe & "solid" representation' )
            print( '      x(X): rotate cw(CCW) about the x axis' )
            print( '      y(Y): rotate cw(CCW) about the y axis' )
            print( '      z(Z): rotate cw(CCW) about the z axis' )
            print( 'arrow keys: move object left, right, up, down ( -x, +x, +y, -y )' )
            print( '===============================================================================' )

