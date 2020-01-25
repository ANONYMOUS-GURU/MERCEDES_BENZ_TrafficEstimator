import cv2
import numpy as np 
import os

path1=os.path.join(os.getcwd(),'data','train','image')
path2=os.path.join(os.getcwd(),'data','train','mask')

path3=os.path.join(os.getcwd(),'data','test','image')
path4=os.path.join(os.getcwd(),'data','test','mask')

paths=[path1,path2,path3,path4]

for path in paths:
	for x in os.listdir(path):
		a=cv2.imread(os.path.join(path,x))
		a=a[:500,:,:]
		cv2.imwrite(os.path.join(path,x),a)