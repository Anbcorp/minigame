__author__ = 'benoit'

import math
import pygame

RED = (255, 0 , 0)
BLUE = pygame.Surface((32,32))
BLUE.fill((0,0,155,255))
GREEN = (0 , 255, 0)

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

DIRECTIONS = [ UP, DOWN, LEFT, RIGHT ]

def hsv2rgb(h,s,v, bitsize=8) :
    s /= 100
    v /= 100
    resolution = math.pow(2,bitsize) - 1

    C = v*s
    H = h/60

    X = C*(1-abs(H%2-1))

    if H < 1:
        (r,g,b) = (C,X,0)
    elif H >= 1 and H < 2:
        (r,g,b) = (X,C,0)
    elif H >= 2 and H < 3:
        (r,g,b) = (0,C,X)
    elif H >= 3 and H < 4:
        (r,g,b) = (0,X,C)
    elif H >= 4 and H < 5:
        (r,g,b) = (X,0,C)
    elif H >= 5 and H < 6:
        (r,g,b) = (C,0,X)
    else:
        (r,g,b) = (0,0,0)

    m = v - C
    return (
            int((r+m)*resolution), 
            int((g+m)*resolution), 
            int((b+m)*resolution),
            )

def apply_hue(value, hue) :
    """
    Return the mid-point on a color disc between value and hue

    apply blue (240) to red (0) should return purple (300)
    apply green (120) to blue (240) returns cyan (180) 
    apply blue to green returns also cyan
    """
    distance = value - hue
    if abs(distance) > 180 :
        distance =value+360-hue

    return hue + distance/2
