import os
import shutil

if not os.path.exists(os.path.join(os.getcwd(),'saved_model_weather')):
	# os.mkdir(os.path.join(os.getcwd(),'saved_model_weather'))
	shutil.copytree(os.path.join(os.getcwd(),'..','weather_model','saved_model'),os.path.join(os.getcwd(),'saved_model_weather'))


if not os.path.exists(os.path.join(os.getcwd(),'saved_model_segmenter')):
	os.mkdir(os.path.join(os.getcwd(),'saved_model_segmenter'))
	shutil.copyfile(os.path.join(os.getcwd(),'..','unet','model50.hdf5'),os.path.join(os.getcwd(),'saved_model_segmenter','model50.hdf5'))


if not os.path.exists(os.path.join(os.getcwd(),'saved_model_labeler')):
	# os.mkdir(os.path.join(os.getcwd(),'saved_model_labeler'))
	shutil.copytree(os.path.join(os.getcwd(),'..','labeler','saved_model'),os.path.join(os.getcwd(),'saved_model_labeler'))
