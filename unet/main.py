from model import *
from data import *

import warnings
warnings.filterwarnings("default", category=DeprecationWarning)
from keras.callbacks import TensorBoard
from time import time
#os.environ["CUDA_VISIBLE_DEVICES"] = "0"


data_gen_args = dict(horizontal_flip=True)
batch_size=8
myGene = trainGenerator(batch_size,os.path.join(os.getcwd(),'data','train'),'image','mask',data_gen_args,save_to_dir = 'saved_pics')

model = unet()
model_checkpoint = ModelCheckpoint('unet_membrane.hdf5', monitor='loss',verbose=1, save_best_only=True)
tensorboard=TensorBoard(log_dir='logs')
print(model.summary())

model.fit_generator(myGene,steps_per_epoch=4500/batch_size,epochs=8,callbacks=[model_checkpoint,tensorboard])

testGene = testGenerator(os.path.join(os.getcwd(),'data','test','image'))
results = model.predict_generator(testGene,30,verbose=1)
saveResult(os.path.join(os.getcwd(),'data','test'),results)