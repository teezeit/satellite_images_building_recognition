import cv2
import sys
import glob
import random


if len(sys.argv)<2:
    print "at least 1 argument. e.g. python show_boxes.py './sample1/' 10"
    print " first argument defines directory with images/labels, second argument says how many examples to try"


elif len(sys.argv)==2:
    directory = sys.argv[1]
    amount = 10
elif len(sys.argv)==3:
    directory = sys.argv[1]
    amount = sys.argv[2]
else:
    print "too many arguments"

imagedirectory = directory+'images/*png'

list_im = glob.glob(imagedirectory)


number = len(list_im)

#random_imgs = [str(i).zfill(4) for i in random.sample(xrange(number),int(amount))]
random_imgs = [i for i in random.sample(list_im,int(amount))]
random_names = [i[-8:-4] for i in random_imgs]

for i in random_names:

    im  = cv2.imread(directory+'images/'+i+'.png')

    lines = open(directory+'labels/'+i+'.txt','r').read().split('\n')
    lines = lines[:-1]


    for l in lines:
        _,_,_,_,c1x,c1y,c2x,c2y,_,_,_,_,_,_,_ = l.split()

        c1x = int(float(c1x))
        c1y = int(float(c1y))
        c2x = int(float(c2x))
        c2y = int(float(c2y))

        cv2.rectangle(im,(c1x,c1y),(c2x,c2y),(255,0,0))

    #im = cv2.resize(im,(512,512))
    cv2.imshow('img',im)
    cv2.waitKey(0)
