import numpy as np
import cv2
import keras
from keras.models import load_model
import matplotlib.pyplot as plt 
from PIL import Image

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

model=load_model('model50.hdf5')

img=np.asarray(Image.open('gta.jpg'))[:,:,:3]
img=cv2.resize(img,(256,256))

if np.max(img)>1:
	img=img/255

img=np.reshape(img,(1,)+img.shape)
out=model.predict(img)

print(out.shape)

out=out[0]
out=np.argmax(out,axis=2)

out=np.array(out)
print(out.shape)
print(out)

# out=toRGB(out)
# out=np.reshape(out,out.shape+(1,))
# print(out.shape)

# cv2.imshow('a',np.reshape(out,out.shape+(1,)))
# cv2.waitKey(0)
# cv2.destroAllWindows()

plt.imshow(out)
plt.show()

cv2.imshow('a',cv2.resize(segColor(out),(512,512)))
cv2.waitKey(0)
cv2.destroyAllWindows()

