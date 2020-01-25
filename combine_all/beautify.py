import numpy as np
import cv2
import random
import glob
import math

def verify_alpha_channel(frame):
    try:
        frame.shape[3] # looking for the alpha channel
    except IndexError:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    return frame

def apply_color_overlay(frame, intensity=0.5, blue=0, green=0, red=0):
    frame = verify_alpha_channel(frame)
    frame_h, frame_w, frame_c = frame.shape
    sepia_bgra = (blue, green, red, 1)
    overlay = np.full((frame_h, frame_w, 4), sepia_bgra, dtype='uint8')
    cv2.addWeighted(overlay, intensity, frame, 1.0, 0, frame)
    return frame

def do_red(img):
    return apply_color_overlay(img, intensity=.5, red=220, green=0)

def do_green(img):
    return apply_color_overlay(img, intensity=.5, red=0, green=220)

def do_yellow(img):
    return apply_color_overlay(img, intensity=.5, red=220, green=220)

# img=cv2.imread('a.png')
# a=apply_color_overlay(img, intensity=.5, red=0, green=220)
# b=apply_color_overlay(img, intensity=.65, red=200, green=200)
# c=apply_color_overlay(img, intensity=.5, red=200, blue=0,green=0)

# cv2.imshow('a',a)
# cv2.imshow('b',b)
# cv2.imshow('c',c)
# cv2.imshow('img',img)

# cv2.waitKey(0)
# cv2.destroyAllWindows()