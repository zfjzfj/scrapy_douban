# -*- coding:utf-8 -*-
import cv

def Reduce(image,m,n):
    H = int(image.height*m)
    W = int(image.width*n)
    size = (W,H)
    iReduce = cv.CreateImage(size,image.depth,image.nChannels)
    for i in range(H):
	for j in range(W):
	    x = int(i/m)
            y = int(j/n)
            iReduce[i,j] = image[x,y]
    return iReduce

image = cv.LoadImage('lena.jpg',1)
iReduce1 = Reduce(image,0.5,0.5)
iReduce2 = Reduce(image,0.8,0.8)
cv.SaveImage("1.jpg",iReduce1)
cv.SaveImage("2.jpg",iReduce2)
