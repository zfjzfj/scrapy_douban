# -*- coding:utf-8 -*-
import cv
import math
import numpy as np
def XRotate(image,angle):
    size = (image.width,image.height)
    iXRotate = cv.CreateImage(size,image.depth,image.nChannels)
    h = image.height
    w = image.width
    anglePi = angle*math.pi/180.0
    cosA = np.cos(anglePi)
    sinA = np.sin(anglePi)
    for i in range(h):
        for j in range(w):
            x = int(cosA*i-sinA*j-0.5*w*cosA+0.5*h*sinA+0.5*w)
            y = int(sinA*i+cosA*j-0.5*w*sinA-0.5*h*cosA+0.5*h)
	    print (x,y)
            if x>-1 and x<image.height and y>-1 and y<image.width:
                iXRotate[x,y] = image[i,j]
    return iXRotate


image = cv.LoadImage('lena.jpg',1)
iSRotate = XRotate(image,20)
cv.SaveImage("np.jpg",iSRotate)

