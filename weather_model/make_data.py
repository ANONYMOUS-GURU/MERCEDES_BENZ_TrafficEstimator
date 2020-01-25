import os

import shutil

addr_rainy=os.path.join(os.getcwd(),'data_images','rainy')
addr_cloudy=os.path.join(os.getcwd(),'data_images','cloudy')
addr_sunny=os.path.join(os.getcwd(),'data_images','sunny')

train_data_rainy=os.listdir(addr_rainy)[:(int)(.9*len(os.listdir(addr_rainy)))]
val_data_rainy=os.listdir(addr_rainy)[(int)(.9*len(os.listdir(addr_rainy))):]

train_data_cloudy=os.listdir(addr_cloudy)[:(int)(.9*len(os.listdir(addr_cloudy)))]
val_data_cloudy=os.listdir(addr_cloudy)[(int)(.9*len(os.listdir(addr_cloudy))):]

train_data_sunny=os.listdir(addr_sunny)[:(int)(.9*len(os.listdir(addr_sunny)))]
val_data_sunny=os.listdir(addr_sunny)[(int)(.9*len(os.listdir(addr_sunny))):]

print('making directories')

new_train_rainy=os.path.join(os.getcwd(),'all_data','train','rainy')
if not os.path.exists(new_train_rainy):
	os.makedirs(new_train_rainy)

new_train_cloudy=os.path.join(os.getcwd(),'all_data','train','cloudy')
if not os.path.exists(new_train_cloudy):
	os.makedirs(new_train_cloudy)

new_train_sunny=os.path.join(os.getcwd(),'all_data','train','sunny')
if not os.path.exists(new_train_sunny):
	os.makedirs(new_train_sunny)

new_val_rainy=os.path.join(os.getcwd(),'all_data','val','rainy')
if not os.path.exists(new_val_rainy):
	os.makedirs(new_val_rainy)

new_val_cloudy=os.path.join(os.getcwd(),'all_data','val','cloudy')
if not os.path.exists(new_val_cloudy):
	os.makedirs(new_val_cloudy)

new_val_sunny=os.path.join(os.getcwd(),'all_data','val','sunny')
if not os.path.exists(new_val_sunny):
	os.makedirs(new_val_sunny)

print('folders made')

for x in train_data_rainy:
	shutil.copyfile(os.path.join(addr_rainy,x),os.path.join(new_train_rainy,x))
print('train_data_rainy done')
for x in train_data_cloudy:
	shutil.copyfile(os.path.join(addr_cloudy,x),os.path.join(new_train_cloudy,x))
print('train_data_cloudy done')
for x in train_data_sunny:
	shutil.copyfile(os.path.join(addr_sunny,x),os.path.join(new_train_sunny,x))
print('train_data_sunny done')


for x in val_data_rainy:
	shutil.copyfile(os.path.join(addr_rainy,x),os.path.join(new_val_rainy,x))
print('val_data_rainy done')

for x in val_data_cloudy:
	shutil.copyfile(os.path.join(addr_cloudy,x),os.path.join(new_val_cloudy,x))
print('val_data_cloudy done')

for x in val_data_sunny:
	shutil.copyfile(os.path.join(addr_sunny,x),os.path.join(new_val_sunny,x))
print('val_data_sunny done')
