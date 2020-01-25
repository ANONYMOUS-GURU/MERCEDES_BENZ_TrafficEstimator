import tensorflow as tf
import os
import numpy as np 
import time
import carla

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_integer('epoch', 50, "training epoch")
# tf.app.flags.DEFINE_float('test_size',0.1,'test size')
# tf.app.flags.DEFINE_float('val_size',0.1,'val size')
# tf.app.flags.DEFINE_boolean('train',True,'training')
tf.app.flags.DEFINE_float('learning_rate_',0.001,'learning rate')
# tf.app.flags.DEFINE_float('keep_prob',0.8,'keep prob')
tf.app.flags.DEFINE_string('save_name','saved_model','folder of saving')
tf.app.flags.DEFINE_integer('validation_interval',None,'validation_interval')


def train():
	# take input data from take_input
	img_size_1=256
	img_size_2=256
	img_channel=1
	label_cnt=3
	kp=0.9
	# let's have the input placeholders
	X,y,learning_rate,dropout_keep_prob,training=carla.placeholders(img_size_1,img_size_2,img_channel,label_cnt)   ####
	logits,out_probs=carla.network(X,dropout_keep_prob=dropout_keep_prob,label_cnt=label_cnt,training=training)   ####
	loss=carla.loss(logits,y)
	optimizer=carla.optimizer(loss,learning_rate)
	accuracy=carla.accuracy(logits,y)

	init=tf.global_variables_initializer()
	sess=tf.Session(config=tf.ConfigProto(allow_soft_placement=True,log_device_placement=False))
	sess.run(init)

	merged=tf.summary.merge_all()
	writer_train_addr='./summary/train'
	writer_val_addr='./summary/val'
	train_writer=tf.summary.FileWriter(writer_train_addr,sess.graph)
	val_writer=tf.summary.FileWriter(writer_val_addr)

	saver=tf.train.Saver()
	saver_addr=os.path.join(os.getcwd(),FLAGS.save_name,'var.ckpt')
	if not os.path.exists(os.path.join(os.getcwd(),FLAGS.save_name)):
		os.mkdir(FLAGS.save_name)

	elif len(os.listdir(os.path.join(os.getcwd(),FLAGS.save_name)))>0:
		saver.restore(sess,saver_addr)
		print('*'*50)
		print('Restoring saved_model')
		print('*'*50)

	lr=FLAGS.learning_rate_
	epochs=FLAGS.epoch
	summary_writer_index_train=0
	summary_writer_index_val=0
	for epoch in range(epochs):
		if (epoch+1) % 5 == 0 and epoch > 0:
			lr /= 2
		i=0
		epoch_loss=0
		epoch_accuracy=0
		train_imgs,_=carla.get_data()

		data_loader_train=carla.data_loader(train_imgs)

		train_num=len(train_imgs)
		batch_size=8
		num_batches=int(np.floor(train_num/batch_size))
		val_interval=(int)(num_batches/2) if FLAGS.validation_interval==None else FLAGS.validation_interval
		for batch in range(num_batches):
			train_x,train_y=next(data_loader_train)
			if i%20==0:
				summary,_,batch_loss,accuracy_batch_tr=sess.run([merged,optimizer,loss,accuracy],feed_dict={X:train_x,y:train_y,learning_rate:lr,dropout_keep_prob:kp,training:True})    #########
				train_writer.add_summary(summary, summary_writer_index_train)
				summary_writer_index_train+=1
				print('>> training loss computed :: {} on {} images out of {}  with learning_rate {}  epoch-> {}  batch number-> {}'.format(batch_loss,train_x.shape[0],train_num,lr,epoch,i+1))
			else:
				_,batch_loss,accuracy_batch_tr=sess.run([optimizer,loss,accuracy],feed_dict={X:train_x,y:train_y,learning_rate:lr,dropout_keep_prob:kp,training:True})      ##########

			epoch_loss+=batch_loss
			epoch_accuracy+=accuracy_batch_tr

			if i%val_interval==0 and i>0:
				_,val_imgs=carla.get_data()
				loss_val=0
				acc_val=0
				val_batch_size=16
				data_loader_val=carla.data_loader(val_imgs)
				num_batches_val=(int)(np.ceil(len(val_imgs)/val_batch_size))
				for k in range(num_batches_val):
					val_x,val_y=next(data_loader_val)
					accuracy_batch,batch_loss,summary=sess.run([accuracy,loss,merged],feed_dict={X:val_x,y:val_y,dropout_keep_prob:1.0,training:False})        ########
					val_writer.add_summary(summary,summary_writer_index_val)
					loss_val+=batch_loss
					acc_val+=accuracy_batch
					summary_writer_index_val+=1

				print('>> validation loss computed :: {} and validation accuracy :: {} on {} images'.format(loss_val/num_batches_val,acc_val/num_batches_val,len(val_imgs)))
			i=i+1
		print('>> epoch loss computed :: {} and epoch training accuracy {}  on epoch_num-> {}'.format(epoch_loss/num_batches,epoch_accuracy/num_batches,epoch))
		saver.save(sess, saver_addr)
	train_writer.close()
	val_writer.close()

	sess.close()

def main(_):
	train()

if __name__=='__main__':
	tf.app.run()


















