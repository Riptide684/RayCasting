# RayCasting

2D rendered simulation of light reflecting off of mirrors in python.

User can add up to 3 lasers, and draw lines in a pygame window. The program then traces the path of the lasers as they reflect off of the mirrors. Physics calculations computed with linear algebra techniques.

How to use:
1. Run the program and navigate to the pygame window.
2. Add up to 3 lasers by clicking the window.
3. Press shift to toggle between placing laser pointers and drawing lines.
4. Click two points to draw a line between them.
5. When the environment is ready to simulate, press enter.
6. The program will display the result in the same pygame window, and then automatically close shortly after.

Notes: 
- max_reflections in the main program can be increased to simulate more reflections of the lasers.
- screen_width and screen_height can be adjusted in the main program.
- Other elements can be reconfigured from their default object attributes.

Libraries required:
- Math
- pygame
- time

Future updates:
- Add the functionality to rotate the laser pointers.
- Check that environment is not malformed.
- Add check for reflecting off of corners.
