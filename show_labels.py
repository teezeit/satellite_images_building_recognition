# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:04:13 2016

@author: to
"""

import glob
import cv2
import sys

if len(sys.argv) < 2:
    print "need at least 1 argument as (str) defining the image directory and file extension [png/txt] e.g. './images/*png' ./labels/*txt"
    exit()


listdirectory = sys.argv[1:]

for directories in listdirectory:
    filenames = glob.glob(directories)


    for f in filenames:
        
                  
        if str(f[-3:]) == 'txt':


            newlabels = []
            lines = open(f,'r').read().split('\n')
           
            lines = lines[:-1]



            for N,l in enumerate(lines):
                _,_,_,_,c1x,c1y,c2x,c2y,_,_,_,_,_,_,_ = l.split()
                
                c1x = int(float(c1x))
                c1y = int(float(c1y))
                c2x = int(float(c2x))
                c2y = int(float(c2y))
 
                print c1x,'\t',c1y,'\t',c2x,'\t',c2y  

     
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
