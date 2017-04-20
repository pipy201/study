# -*- coding: utf-8 -*-

'''
My system is windows7 - anaconda3 , ubuntu16.04 anaconda2.
To run this script , you need to use keras 2.0 tensorflow backend.
You need to modify your system to run this script, Considering suitable environment of your system. 
Refer to below 'Setting part' for detail.
If this script doesn't run properly, check your system one more time.
ex) pip list
    pip install tensorflow
    pip install keras
http://gusrb.tistory.com
'''

import multiprocessing, os, time
from keras.preprocessing.image import ImageDataGenerator
#from tensorflow.contrib.keras.python.keras.preprocessing.image import ImageDataGenerator

''' Setting part '''
INPUT_DIR = 'C:/tmp3/'# your image data directory/
OUTPUT_DIR = 'C:/Temp/'  # output images data directory/
IMAGE_FORMAT = 'jpeg'  # output image format (jpeg, png)
FILE_NAME = 'pre'  # output image file name pre***.jpeg
IMAGE_SIZE = (299, 299)  # output image size
END_POINT = 100  # When batch size = 1, the number of new total image
P_NUM = multiprocessing.cpu_count() # number of core
# Set image modify
# See keras api documentation
# https://keras.io/preprocessing/image/
train_data = ImageDataGenerator(
    samplewise_center=False,
    featurewise_std_normalization=False,
    samplewise_std_normalization=False,
    zca_whitening=False,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    channel_shift_range=0.1,
    fill_mode='nearest',
    horizontal_flip=False,
    vertical_flip=False,
    rescale=None,
    preprocessing_function=None)

''' Script execution part '''
labels = os.listdir(INPUT_DIR)
labels_cnt = len(labels)

def check_start():
    no_image = []
    if not (labels):
        print('\nError : Input directory is empty.')
        print(INPUT_DIR)
        exit()
    else:
        for name in labels:
            if (len(os.walk(INPUT_DIR + name).__next__()[2]) == 0):
                no_image.append(name)
    if (no_image):
        print('\nError : There are no images in the directory.')
        for name in no_image:
            print('- ' + name)
        exit()

def ready_dir():
    # looking for labels
    print('\nLooking for folder name ...')
    for folder_name in labels:
        print(folder_name)
        os.mkdir(OUTPUT_DIR + folder_name)
    print('... Completed ...\n')

def gen(folder_name):
    i = 0
    batch_cnt = len(os.walk(INPUT_DIR + folder_name).__next__()[2])
    print('- ' + folder_name + ' start ...')
    try:
        for name in train_data.flow_from_directory(
                directory=INPUT_DIR,
                target_size=IMAGE_SIZE,
                batch_size=batch_cnt,
                save_to_dir=OUTPUT_DIR + folder_name,
                save_format=IMAGE_FORMAT,
                save_prefix=folder_name,
                classes=[folder_name]):
            i += 1
            if i > END_POINT:
                print('-- '+folder_name + ' end ...')
                break
    except Exception as e:
        print('\nError : Image generate error !')
        print(e)

def gen_run():
    if P_NUM > labels_cnt:
        core = labels_cnt
    else:
        core = P_NUM

    try:
        p = multiprocessing.Pool(core)
        p.map_async(gen, labels).get()
    except Exception as e:
        print('\nError : Process execution error !')
        print(e)

def check_end():
    new_labels = os.listdir(OUTPUT_DIR)
    if (labels == new_labels):
        print('\nAll images generated !')
    else:
        error_dir = list(set(labels) - set(new_labels))
        print('\nError : Some images were not generated. Please check the Input/Output directory.')
        for dir in error_dir:
            print(dir)

if __name__ == '__main__':
    start_time = time.time()
    check_start()
    ready_dir()
    gen_run()
    check_end()
    running_time = time.time()-start_time
    print('RUNNING TIME : %.2f sec'%running_time)
    print('SPEED : %.2f label/sec'%(running_time / labels_cnt))
