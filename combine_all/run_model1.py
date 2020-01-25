import inference1 as inference
import cv2
import matplotlib.pyplot as plt
import numpy as np
from beautify import do_red,do_yellow,do_green



class infer_all:
	def __init__(self):
		self.segmenter_=inference.infer_segment()
		self.labeler_=inference.infer()
		self.weather_=inference.infer_weather()	

	def segment_predictor(self,img):
		a=self.segmenter_.predict(img)
		b=self.segmenter_.segColor(a)
		return a,b

	def weather_predictor(self,img):
		return self.weather_.predict(img)

	def label_predictor(self,img):
		a,b=self.segment_predictor(img)
		return b,self.labeler_.predict(a)

	def predict(self,img_rgb):
		img_bgr=cv2.cvtColor(img_rgb,cv2.COLOR_BGR2RGB)
		wt=self.weather_predictor(img_bgr)
		si,tp=self.label_predictor(img_rgb)
		img_rgb=cv2.resize(img_rgb,(256,256))
		if tp=='busy':
			tp=do_red(img_rgb)
		elif tp=='semi-busy':
			tp=do_yellow(img_rgb)
		else:
			tp=do_green(img_rgb)


		# wt=cv2.resize(cv2.imread(os.path.join(os.getcwd(),'pics',wt)),(256,256))

		return si,tp,wt

# inf_=infer_all()
# si,tp,wt=inf_.predict(cv2.imread('1.png'))

# cv2.imwrite('a.png',si)
# cv2.imwrite('b.png',tp)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

