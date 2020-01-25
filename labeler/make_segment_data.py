import numpy as np
import cv2
import keras
from keras.models import load_model
import matplotlib.pyplot as plt 
import os
import shutil

def segColor(img):
    maskList = [(255,255,255),(0,0,0),(0,255,255),(255,0,255),(255,255,0),(0,0,255),(0,255,0),(255,0,0),(50,100,150),(100,150,50),(150,50,100),(127,127,127)]
    h = img.shape[0]
    w = img.shape[1]
    final = np.zeros((h,w,3),dtype = 'uint8')
    mask = cv2.inRange(img,0,0)
    for i in range(12):
        final[:,:,0] += (((cv2.inRange(img,i,i))/255)*(maskList[i][0])).astype('uint8')
        final[:,:,1] += (((cv2.inRange(img,i,i))/255)*(maskList[i][1])).astype('uint8')
        final[:,:,2] += (((cv2.inRange(img,i,i))/255)*(maskList[i][2])).astype('uint8')
    return final

count=0
import os
if not os.path.exists(os.path.join(os.getcwd(),'model50.hdf5')):
    shutil.copyfile(os.path.join(os.getcwd(),'..','unet','model50.hdf5'),os.path.join(os.getcwd(),'model50.hdf5'))
model=load_model('model50.hdf5')



classes=['busy','semi-busy','clear']

for class_ in classes:
    if not os.path.exists(os.path.join(os.getcwd(),'data_images',class_)):
        os.makedirs(os.path.join(os.getcwd(),'data_images',class_))

for class_ in classes:
    for x in os.listdir(os.path.join(os.getcwd(),'data',class_)):
        addr=os.path.join(os.getcwd(),'data',class_,x)
        a=cv2.resize(cv2.imread(addr),(256,256))
        a=np.reshape(a,(1,)+a.shape)
        seg=model.predict(a)
        seg=seg[0]
        seg=np.argmax(seg,axis=2)
        seg=np.array(seg)
        cv2.imwrite(os.path.join(os.getcwd(),'data_images',class_,x),seg)
        count=count+1
        print(count)
    print('done for class -- {}'.format(class_))

