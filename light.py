from __future__ import division
from neopixel import *
import math
import time, colorsys
import numpy as np
import random
import skywriter
import signal

LED_PIN        = 18     # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # Just leave it at this, normally works!
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255      # from 0 to 255, keep it low, you don't want to be blinded
LED_INVERT     = False # True to invert the signal (when using NPN transistor level shift)
Width          = 20      # How ever many pixels wide your grid is
Height         = 13       # How ever many pixels wide your grid is
LED_COUNT      = 259      # Total number of LEDs

ws2812 = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
ws2812.begin()
_rotation = 0

#Large LED Matrix 
map = [
  [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
  [39,38,37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20],
  [40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59],
  [79,78,77,76,75,74,73,72,71,70,69,68,67,66,65,64,63,62,61,60],
  [80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99],
  [119,118,117,116,115,114,113,112,111,110,109,108,107,106,105,104,103,102,101,100],
  [120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139],
  [159,158,157,156,155,154,153,152,151,150,149,148,147,146,145,144,143,142,141,140],
  [160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179],
  [199,198,197,196,195,194,193,192,191,190,189,188,187,186,185,184,183,182,181,180],
  [200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219],
  [239,238,237,236,235,234,233,232,231,230,229,228,227,226,225,224,223,222,221,220],
  [240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259]
]

def xy_to_strip(x, y, strip_len):
    return x * strip_len + y
 
def rotation(r = 0):
    global _rotation
    if r in [0,90,180,270]:
        _rotation = r
        return True
    else:
        raise ValueError('Rotation must be 0, 90, 180 or 270 degrees')
        return

def get_index_from_xy(x, y):
  
 #Convert an x, y value to an index on the display
 
    if x > 14 or x < 0:
        raise ValueError('X position must be between 0 and 7')
        return
    if y > 19 or y < 0:
        raise ValueError('Y position must be between 0 and 7')
        return

    y = 19-y

    if _rotation == 90:
        x, y = 19, 19-x
    if _rotation == 180:
        x, y = 19-x,19-y
    if _rotation == 270:
        x, y = 19-y,x
 
    return map[x][y]
	
def set_pixel(x, y, r, g, b):
    index = get_index_from_xy(x, y)
    if index != None:
        ws2812.setPixelColorRGB(index, r, g, b)

def make_gaussian(fwhm, x0, y0):
    x = np.arange(0, 20, 1, float)
    y = x[:, np.newaxis]
    fwhm = fwhm
    gauss = np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)
    return gauss

h = 0
@skywriter.move()
def spot(x, y, z):
    global h
    x0 = x * 19
    y0 = y * 13
    if z == 0:
        z = 0.01
    fwhm = 1/z
    gauss = make_gaussian(fwhm, x0, y0)
    for j in range(19):
        for i in range(13):
            s = 0.8
            v = gauss[i,j]
            rgb = colorsys.hsv_to_rgb(h/10000, s, v)
            r = int(rgb[0]*255.0)
            g = int(rgb[1]*255.0)
            b = int(rgb[2]*255.0)
            set_pixel(i, j, r, g, b)
    ws2812.show()
    time.sleep(0.0005)
    h += 1
    if h % 10 == 0:
        if h > 10000:
            print("h > 1000")
            h = 0

while True:
    input("Press Enter to pause")
    ws2812.setBrightness(0)
    ws2812.show()
    input("Press Enter to continue")
    ws2812.setBrightness(LED_BRIGHTNESS)
    ws2812.show()
