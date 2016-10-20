#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script copies a random subset of images and labels in startfolder to a targetfolder
using the KITTI folder structure

run this script
python create_random_subsets.py 'STARTfOLDER' 'TARGETFOLDER' AMOUNT_IMAGES PERCENT_TRAIN
e.g.:
python create_random_subsets.py './processed_labeled' './sample1' 10 0.8

this is how the original images need to be stored:

STARTFOLDERNAME/
|--images/
|    |___000001.png
|--labels
|    |___000001.txt

STARTFOLDER determines where the original images are stored
TARGETFOLDER determines where the subset should be copied
AMOUNT_IMAGES determines how many images should be used
PERCENT_TRAIN determines how much percent of the used images should be training


'''

import sys
import os
import random
import shutil

if len(sys.argv) != 5:
    print 'something went wrong- not 4 arguments'
    print "e.g.: python create_random_subsets.py './processed_labeled' './sample1' 10 0.8"
    sys.exit()
#READIN the arguments into a list
argin = sys.argv

#and store them
startfoldername = argin[1] #e.g. data
targetfoldername= argin[2] #e.g. sample1
amount_images   = argin[3] #e.g. 100
percent_train   = argin[4] #e.g. 0.8

#check that the startfolder exists
if not os.path.exists(startfoldername):
    print 'something went wrong- startfolder doesnt seem to exist'
    
#create target folders if they don't exist yet
if not os.path.exists(targetfoldername):
    os.makedirs(targetfoldername+'/train/images/')
    os.makedirs(targetfoldername+'/train/labels/')
    os.makedirs(targetfoldername+'/val/images/')
    os.makedirs(targetfoldername+'/val/labels/')    


#read in all filenames
filenames = os.listdir(startfoldername + '/labels/')

Nfilenames = []
#print 'len filenames before = ',len(filenames)

#Read in all labels and only keeep those with amount_buildings in [1,30]
for f in filenames:
    lines = open(startfoldername + '/labels/' + f,'r').read().split('\n')
            
    lines = lines[:-1]

    if len(lines)>5:# and len(lines)<25:
        sizes =[]
        for l in lines:
            _,_,_,_,c1x,c1y,c2x,c2y,_,_,_,_,_,_,_ = l.split()

            #sizes.append([float(c2x)-float(c1x),float(c2y)-float(c1y)])
        #if all( i[0] >=13 or i[1]>=13 for i in sizes):
        Nfilenames.append(f)
    '''
    #len_lin = len(lines)

    if len_lin == 0:
        filenames.remove(f)
        
    elif len_lin == 1:         
        object_det,_,_,_,c1x,c1y,c2x,c2y,_,_,_,_,_,_,_ = lines[0].split()
        if str(object_det) == 'dontcare':
            filenames.remove(f)
            
    elif len_lin > 6:
        print len_lin
        filenames.remove(f)
    '''       
print 'left images = ',len(Nfilenames)

#create a random subset of filenames
rand_smpl_filenames = [Nfilenames[i] for i in random.sample(xrange(len(Nfilenames)),int(amount_images))]

#create indexlist
indexlist = {rand_smpl_filenames[i][:-3]:str(i).zfill(4) for i in xrange(len(rand_smpl_filenames))}

#calculate the index at which the data is split
splitindex = int(float(percent_train) *len(rand_smpl_filenames))


#define the training and validation images and labels
train_lab = rand_smpl_filenames[:splitindex]
val_lab   = rand_smpl_filenames[splitindex:]
train_img = [name[:-3]+'png' for name in train_lab]
val_img   = [name[:-3]+'png' for name in val_lab]



#then copy them to the new directories
for im in train_img:
    shutil.copyfile(startfoldername+'/images/'+im, targetfoldername+'/train/images/'+indexlist[im[:-3]]+'.png')
for im in val_img:
    shutil.copyfile(startfoldername+'/images/'+im, targetfoldername+'/val/images/'+indexlist[im[:-3]]+'.png')
for label in train_lab:
    shutil.copyfile(startfoldername+'/labels/'+label, targetfoldername+'/train/labels/'+indexlist[label[:-3]]+'.txt')
for label in val_lab:
    shutil.copyfile(startfoldername+'/labels/'+label, targetfoldername+'/val/labels/'+indexlist[label[:-3]]+'.txt')




