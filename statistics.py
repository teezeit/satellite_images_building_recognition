# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 18:26:44 2016

@author: to
"""


from matplotlib import pyplot as plt
import glob


labdir1 = './sample2000_1280/train/labels/*.txt'
labdir2 = './sample2000_1280/val/labels/*txt'

filenames = glob.glob(labdir1) + glob.glob(labdir2)




coordinates = []
number_of_buildings = []
heights  = []
widths  = []
size    = []

for f in filenames:
    
    data = []
    
    lines = open(f,'r').read().split('\n')
    lines = lines[:-1]
    number_of_buildings.append(len(lines))
    for l in lines:
        _,_,_,_,c1x,c1y,c2x,c2y,_,_,_,_,_,_,_ = l.split()            
        data.append([float(c1x),float(c1y),float(c2x),float(c2y)])
        coordinates.append([float(c1x),float(c1y),float(c2x),float(c2y)])    
        heights.append(int(abs(float(c2y)-float(c1y))))
        widths.append(int(abs(float(c2x)-float(c1x))))
        size.append(heights[-1]*widths[-1])
   

fig =plt.figure(figsize=(25,20),dpi=160)
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(224)
ax4 = fig.add_subplot(223)




n,bins,pathces = ax1.hist(number_of_buildings,50, facecolor='green', alpha=0.75)
n,bins,pathces = ax2.hist(widths, 50, facecolor='green', alpha=0.75)
n,bins,pathces = ax3.hist(heights, 50, facecolor='green', alpha=0.75)
n,bins,pathces = ax4.hist(size, 100,facecolor='green', alpha=0.75)

#ax1.set_xlim([0,40])
ax2.set_xlim([0,250])
ax3.set_xlim([0,250])
ax4.set_xlim([0,50000])

ax1.set_xlabel('number of buildings in image')
ax1.set_ylabel('amount')
ax2.set_xlabel('widths of building [px]')
ax2.set_ylabel('amount')
ax3.set_xlabel('heights of buidling [px]')
ax3.set_ylabel('amount')
ax4.set_xlabel('size of building [px]')
ax4.set_ylabel('amount')
plt.rc('font',size=30)
fig.tight_layout()
fig.savefig('./statistics.png')

