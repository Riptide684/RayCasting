import pygame
import math
import time


class Laser():
    # Laser pointer object

    rotation = 0 # Clockwise angle (radians) of laser pointer relative to North
    reflections = 0 # How many times laser has reflected off of a line
    width = 40
    height = 30

    def __init__(self, colour, pos):
        self.colour = colour
        self.pos = pos
        # Associates a child photon to the parent laser
        self.photon = Photon([pos[0] + self.width, pos[1] + (self.height / 2)])
        # Represents the body of the laser pointer on the screen
        self.rectangle = pygame.Rect(pos[0], pos[1], self.width, self.height)


class Photon():
    # Keeps track of laser path

    direction = [1, 0] # Current direction of travel of photon
    current_line = None

    def __init__(self, pos):
        # Current position of photon is at the middle front of the laser
        self.pos = pos

    def reflect(self, vector):
        # Uses formula for reflecting direction vector in line vector
        r = dot(self.direction, vector)
        s = multiply_vector(2*r, vector)
        self.direction = subtract_vectors(s, self.direction)


class Line():
    # Object representing a line
    def __init__(self, start, end):
        self.start = start # Where the line starts
        self.end = end # Where the line ends
        self.vector = get_vector(start, end) # Unit vector which lies on line
        self.length = distance(start, end) # Length of line in pixels


def add_vectors(v1, v2):
    # Function to add two vector quantities
    v3 = []
    for i in range(2):
        v3.append(v1[i] + v2[i])

    return v3


def subtract_vectors(v1, v2):
    # Function to subtract two vector quantities
    v3 = []
    for i in range(2):
        v3.append(v1[i] - v2[i])

    return v3


def multiply_vector(k, v):
    # Function to multiply a vector by a scalar
    v2 = []
    for i in range(2):
        v2.append(k * v[i])

    return v2


def dot(a, b):
    # Function to compute the dot product of two vectors
    total = 0
    for i in range(2):
        total += a[i]*b[i]

    return total


def get_vector(a, b):
    # Gives a unit vector from a to b
    x = b[0] - a[0]
    y = b[1] - a[1]
    modulus = math.sqrt(x**2 + y**2)

    return [x/modulus, y/modulus]


def add_laser(lasers, position):
    # Creates new laser pointer if less than 3 are drawn already
    if len(lasers) < 3:
        lasers.append(Laser(colours[len(lasers)], position))
        return lasers, True

    return lasers, False


def add_line(lines, start, end):
    # Creates a new line from start to end
    if start != end:
        lines.append(Line(start, end))
        return lines, True

    return lines, False


def boundary(width, height):
    # Creates lines to represent the boundary of the window
    boundaries = []
    boundaries.append(Line([0, 0], [width, 0])) # Top boundary
    boundaries.append(Line([0, 0], [0, height])) # Left boundary
    boundaries.append(Line([0, height], [width, height])) # Bottom boundary
    boundaries.append(Line([width, 0], [width, height])) # Right boundary

    return boundaries


def find_collision(photon, lines):
    # Finds the first line that the photon reflects off

    intersections = []  # Array of all points of intersection with line segments

    for line in lines:
        intersection = get_intersection(photon, line) # Gets point of intersection with extended line
        if intersection != None:
            intersections.append([intersection, line])

    min_distance = 10000.0
    closest_intersection = None

    # Finds which point of intersection is closest to the photon
    for intersect in intersections:
        intersect_distance = distance(intersect[0], photon.pos)

        if intersect_distance < min_distance:
            min_distance = intersect_distance
            closest_intersection = intersect

    return closest_intersection


def distance(a, b):
    # Calculates distance between two points, a and b, in pixels
    return math.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)


def get_intersection(photon, line):
    # Calculates the point of intersection of the photon and the line segment

    # Check if photon is already on this line
    if photon.current_line == line:
        return None

    d = photon.direction # Direction of photon travel
    r = line.vector # Direction of line (start to end)
    p = photon.pos # Point where photon currently is
    a = line.start # Point where line starts

    denominator = d[0] * r[1] - d[1] * r[0] # Used in formula for point of intersection

    # Check if lines are parallel
    if denominator == 0:
        return None

    numerator = d[1]*a[0] - d[0]*a[1] + d[0]*p[1] - d[1]*p[0] # Used in formula for point of intersection

    mu = numerator/denominator # Parameter to denote the location of the intersection on the line

    # Check if point of intersection lies on the line segment
    if not 0 < mu < line.length:
        return None

    intersection = add_vectors(a, multiply_vector(mu, r)) # Point of intersection

    # Check if photon moved in the correct direction
    t = subtract_vectors(intersection, p)
    if t[0]*d[0] >= 0 and t[1]*d[1] >= 0:
        return intersection

    return None


if __name__ == '__main__':
    pygame.init()

    # Draw a blank white screen
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill((255, 255, 255))

    # Initialising variables
    running = True # Should program continue
    model_light = False # Should lasers be simulated upon halting
    colours = ['red', 'blue', 'green'] # Possible laser colours
    place_laser = 1 # Are we placing new laser pointer
    drawing_line = 0 # Have we started drawing a new line
    line_start = [0, 0] # Where line is being drawn from
    lasers = [] # Array containing all laser pointer objects
    lines = boundary(screen_width, screen_height) # Array containing all line objects, including the window
    max_reflections = 10 # Max number of times a laser can reflect off of a line

    # Main loop
    while running:
        for event in pygame.event.get():

            # Mouse click represents drawing line or placing laser pointer
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Should we add a laser pointer or new line
                if place_laser:
                    lasers, added = add_laser(lasers, pos)
                    if added:
                        # If a new laser pointer is placed then draw it
                        pygame.draw.rect(screen, lasers[-1].colour, lasers[-1].rectangle)

                else:
                    # Has the line already been started
                    if drawing_line:
                        lines, added = add_line(lines, line_start, pos)
                        drawing_line = 0
                        if added:
                            # If a new line is placed then draw it
                            pygame.draw.line(screen, 'black', lines[-1].start, lines[-1].end)

                    # Start a new line
                    else:
                        line_start = pos
                        drawing_line = 1

            # Shift button toggles between placing a laser and drawing a line
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    place_laser = (place_laser + 1) % 2
                    drawing_line = 0
                if event.key == pygame.K_RETURN:
                    running = False
                    model_light = True

            # Closing the PyGame window terminates the program
            elif event.type == pygame.QUIT:
                running = False

        # Updates the display
        pygame.display.flip()

    # Draw the reflections of the lasers
    if model_light:
        for laser in lasers:
            points = [laser.photon.pos]  # Array of points of collision

            # Reflect the laser until maximum is reached
            while laser.reflections <= max_reflections:
                # Checks which line photon will collide with, and its direction vector
                collision, line = find_collision(laser.photon, lines)

                laser.reflections += 1
                points.append(collision)
                laser.photon.current_line = line

                # Photon now starts from collision point
                laser.photon.pos = collision

                # Photon changes direction
                laser.photon.reflect(line.vector)

            # Draw the ray tracing
            pygame.draw.lines(screen, laser.colour, False, points)

        pygame.display.flip()
        time.sleep(5)

    pygame.quit()