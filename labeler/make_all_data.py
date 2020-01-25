import os

import shutil

addr_busy=os.path.join(os.getcwd(),'data_images','busy')
addr_clear=os.path.join(os.getcwd(),'data_images','clear')
addr_semibusy=os.path.join(os.getcwd(),'data_images','semi-busy')

train_data_busy=os.listdir(addr_busy)[:(int)(.9*len(os.listdir(addr_busy)))]
val_data_busy=os.listdir(addr_busy)[(int)(.9*len(os.listdir(addr_busy))):]

train_data_clear=os.listdir(addr_clear)[:(int)(.9*len(os.listdir(addr_clear)))]
val_data_clear=os.listdir(addr_clear)[(int)(.9*len(os.listdir(addr_clear))):]

train_data_semibusy=os.listdir(addr_semibusy)[:(int)(.9*len(os.listdir(addr_semibusy)))]
val_data_semibusy=os.listdir(addr_semibusy)[(int)(.9*len(os.listdir(addr_semibusy))):]


print('making directories')
if not os.path.exists(os.path.join(os.getcwd(),'all_data')):
	os.mkdir(os.path.join(os.getcwd(),'all_data'))

if not os.path.exists(os.path.join(os.getcwd(),'all_data','train')):
	os.mkdir(os.path.join(os.getcwd(),'all_data','train'))

if not os.path.exists(os.path.join(os.getcwd(),'all_data','val')):
	os.mkdir(os.path.join(os.getcwd(),'all_data','val'))

new_train_busy=os.path.join(os.getcwd(),'all_data','train','busy')
if not os.path.exists(new_train_busy):
	os.mkdir(new_train_busy)

new_train_clear=os.path.join(os.getcwd(),'all_data','train','clear')
if not os.path.exists(new_train_clear):
	os.mkdir(new_train_clear)

new_train_semibusy=os.path.join(os.getcwd(),'all_data','train','semi-busy')
if not os.path.exists(new_train_semibusy):
	os.mkdir(new_train_semibusy)

new_val_busy=os.path.join(os.getcwd(),'all_data','val','busy')
if not os.path.exists(new_val_busy):
	os.mkdir(new_val_busy)

new_val_clear=os.path.join(os.getcwd(),'all_data','val','clear')
if not os.path.exists(new_val_clear):
	os.mkdir(new_val_clear)

new_val_semibusy=os.path.join(os.getcwd(),'all_data','val','semi-busy')
if not os.path.exists(new_val_semibusy):
	os.mkdir(new_val_semibusy)

print('folders made')
for x in train_data_busy:
	shutil.copyfile(os.path.join(addr_busy,x),os.path.join(new_train_busy,x))
print('train_data_busy done')
for x in train_data_clear:
	shutil.copyfile(os.path.join(addr_clear,x),os.path.join(new_train_clear,x))
print('train_data_clear done')
for x in train_data_semibusy:
	shutil.copyfile(os.path.join(addr_semibusy,x),os.path.join(new_train_semibusy,x))
print('train_data_semibusy done')

for x in val_data_busy:
	shutil.copyfile(os.path.join(addr_busy,x),os.path.join(new_val_busy,x))
print('val_data_busy done')

for x in val_data_clear:
	shutil.copyfile(os.path.join(addr_clear,x),os.path.join(new_val_clear,x))
print('val_data_clear done')

for x in val_data_semibusy:
	shutil.copyfile(os.path.join(addr_semibusy,x),os.path.join(new_val_semibusy,x))
print('val_data_semibusy done')