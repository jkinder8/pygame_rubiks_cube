Rubik's Cube game using pygame.

A computer version of the classic Rubik's Cube.

usage: python ./RCGame.py [debug]
Supplying the optional debug argument will print a bunch
of the behind the scenes processing going on.

I am no good at Rubik's Cube and use this fantastic site to input the initial data and
let it show me the moves!


https://rubiks-cube-solver.com/
===============================================
Files Description:
Place all below in the same directory.
RCGame.py => Applies the pygame graphical interface.
rubiks_cube.py => Class with methods to build and
manipulate the cube.

Color files:
blue.png
green.png
red.png
white.png
yellow.png
===============================================
RCGame Display:
The sides are 0 through 5.
Top Left can be: 0, 2, 6, or 8, and relates how the current view is 
being displayed.
The large view in the white background section is considered the front.
Ex: Top Left = 0
The 3 x 3 side would be.
0 1 2
3 4 5
6 7 8

Movement:
By clicking the left mousebutton the areas labeled up, down, left, or right,
The view side and top left (orienation) will be updated.

The grey area displays the adjacent sides:
            up
       left    right    back
           down
           
The back side is shown as if hinged to the right side.

Shifting a row or column:
A row or column is shifting by pressing, holding, and dragging the right mouse button, and releasing.
It is looking for 25 captured MOUSEMOTION events
between the right mouse press and release. If fewer are gathered, the request
is ignored. In my testing, 25 captures took place with normal paced drag
across the 3 cells in a row or column.

I used pygame version 1.9.6
