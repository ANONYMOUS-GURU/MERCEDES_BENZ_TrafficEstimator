import cv2
import tensorflow as tf
import numpy as np
import os
from keras.models import load_model
import keras

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

class infer:
	def __init__(self):
		self.graph=tf.Graph()
		self.sess=tf.Session(graph=self.graph)

		with self.graph.as_default():
			new_saver = tf.train.import_meta_graph(os.path.join(os.getcwd(),'saved_model_labeler','var.ckpt.meta'))
			new_saver.restore(self.sess,os.path.join(os.getcwd(),'saved_model_labeler','var.ckpt'))
			ops=self.sess.graph.get_operations()

			self.sess_input=self.sess.graph.get_tensor_by_name('input/image:0')
			self.sess_out=self.sess.graph.get_tensor_by_name('fc2layer/BiasAdd:0')
			self.sess_keep_prob=self.sess.graph.get_tensor_by_name('hparams/keep_prob:0')
			self.sess_training=self.sess.graph.get_tensor_by_name('hparams/is_train:0') 
			self.probs=self.sess.graph.get_tensor_by_name('softmaxlayer/softmax_op:0')

	def predict(self,img):
		img=cv2.resize(img,(256,256))
		img=np.reshape(img,[1,img.shape[0],img.shape[1],1])
		out_logits,out_probs=self.sess.run([self.sess_out,self.probs],feed_dict={self.sess_input:img,self.sess_keep_prob:1.0,self.sess_training:False})
		a={0:'busy',1:'clear',2:'semi-busy'}
		return a[np.argmax(np.reshape(out_probs,[3]))]

	def close(self):
		self.sess.close()


class infer_weather:
	def __init__(self):
		self.graph=tf.Graph()
		self.sess=tf.Session(graph=self.graph)

		with self.graph.as_default():
			new_saver = tf.train.import_meta_graph(os.path.join(os.getcwd(),'saved_model_weather','var.ckpt.meta'))
			new_saver.restore(self.sess,os.path.join(os.getcwd(),'saved_model_weather','var.ckpt'))
			print('graph restored')
			ops=self.sess.graph.get_operations()

			self.sess_input=self.sess.graph.get_tensor_by_name('input/image:0')
			self.sess_out=self.sess.graph.get_tensor_by_name('fc2layer/BiasAdd:0')
			self.sess_keep_prob=self.sess.graph.get_tensor_by_name('hparams/keep_prob:0')
			self.sess_training=self.sess.graph.get_tensor_by_name('hparams/is_train:0') 
			self.probs=self.sess.graph.get_tensor_by_name('softmaxlayer/softmax_op:0')

	def predict(self,img):
		img=cv2.resize(img,(256,256))
		img=np.reshape(img,[1,img.shape[0],img.shape[1],3])
		out_logits,out_probs=self.sess.run([self.sess_out,self.probs],feed_dict={self.sess_input:img,self.sess_keep_prob:1.0,self.sess_training:False})
		a={0:'rainy',1:'cloudy',2:'sunny'}
		return a[np.argmax(np.reshape(out_probs,[3]))]

	def close(self):
		self.sess.close()

class infer_segment:
	def __init__(self):
		self.graph=tf.Graph()
		with self.graph.as_default():
			self.sess=tf.Session(graph=self.graph)
			with self.sess.as_default():
				self.model=load_model(os.path.join(os.getcwd(),'saved_model_segmenter','model50.hdf5'))

	def segColor(self,img):
		if len(img.shape)==3:
			img=img[:,:,2]
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

	def predict(self,img):
		img=cv2.resize(img,(256,256))
		if np.max(img)>1:
			img=img/255
		img=np.reshape(img,(1,)+img.shape)
		with self.graph.as_default():
			with self.sess.as_default():
				out=self.model.predict(img)
		out=out[0]
		out=np.argmax(out,axis=2)
		out=np.array(out)
		return out

	def close(self):
		del self.model


