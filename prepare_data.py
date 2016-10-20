# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 18:26:44 2016

@author: to
"""
import numpy as np
import json
import cv2 #using opencv 3
import glob            #to search for textfiles in folder
import time
import pickle

workingpath   = './processed_labeled/images/'
outputprefix_labels    = './processed_labeled/labels/3band_'
outputprefix_images   = './processed_labeled/images/3band_'
featurefile   = './AOI_1_Rio_polygons_solution_3band.geojson'
prefix_images = workingpath +'3band_'# + ID + .png
postfix_images= '.png'
map_featureNR = './mapping.p'


#013022232200_Public_img7018
cutoff_identifier = len('013022232200_Public_img')



start_time = time.time()

#GET ALL IMAGES
#list of filenames in this directory.
filenames = glob.glob(workingpath + '*' + postfix_images)
#filenames.sort()

#READ IN FEATURE LIST
with open(featurefile) as data_file:
    data = json.load(data_file) 
    
#store featurelist
features = [f for f in data['features']]


#map filelist to featurelist 

file_to_feature = []
'''
for nrstr,im_str in enumerate(filenames): 
    if nrstr%100==0:print nrstr
    featurelistNR = []
    for nr,f in enumerate(features):
        #remove '3band_' beginning and '.tif' ending
        im_str_id = im_str[len(prefix_images):-len(postfix_images)]
        
        #and find the features associated with the current image [with a valid (!=-1) buildingid]
        if f['properties']['ImageId'] == unicode(im_str_id):
            featurelistNR.append(nr)
            
    file_to_feature.append(featurelistNR)

fileObject = open(map_featureNR,'wb')
pickle.dump(file_to_feature,fileObject)   
fileObject.close()
end_time = time.time()
exit()
#took 2613 seconds

'''
fileObject = open(map_featureNR,'r')
file_to_feature = pickle.load(fileObject)





#loop over all images
for im_str_nr, im_str in enumerate(filenames):
    
    #if im_str_nr%100==0 and im_str_nr>1: break


    #READ IN IMAGE
    im = cv2.imread(im_str)

    #check if too many black pixels:
    #convert 2 grayscale
    bw = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    #count pixels, color & black pixels
    amount_pixel = np.prod(np.shape(bw))
    amount_colorpixel = cv2.countNonZero(bw)
    amount_blackpixel = amount_pixel - amount_colorpixel

    #if too many blackpixels, then we don't want to use the image
    if amount_blackpixel >  1000:
        continue
    
    #COOL, now write the label description in KITTI format
    '''
    1    type         Describes the type of object: 'Car', 'Van', 'Truck',
                     'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram',
                     'Misc' or 'DontCare'
    1    truncated    Float from 0 (non-truncated) to 1 (truncated), where
                      truncated refers to the object leaving image boundaries
    1    occluded     Integer (0,1,2,3) indicating occlusion state:
                      0 = fully visible, 1 = partly occluded
                      2 = largely occluded, 3 = unknown
    1    alpha        Observation angle of object, ranging [-pi..pi]
    4    bbox         2D bounding box of object in the image (0-based index):
                      contains left, top, right, bottom pixel coordinates
    3    dimensions   3D object dimensions: height, width, length (in meters)
    3    location     3D object location x,y,z in camera coordinates (in meters)
    1    rotation_y   Rotation ry around Y-axis in camera coordinates [-pi..pi]
    1    score        Only for results: Float, indicating confidence in
                      detection, needed for p/r curves, higher is better.
                      
    Example:
    Cyclist 0.00 3 -1.65 676.60 163.95 688.98 193.93 1.86 0.60 2.02 4.59 1.32 45.84 -1.55
    DontCare -1 -1 -10 503.89 169.71 590.61 190.13 -1 -1 -1 -1000 -1000 -1000 -10
    '''
    #This is where the labels will be stored
    labels = []

    #remove '3band_' beginning and '.tif' ending
    im_str_id = im_str[len(prefix_images):-len(postfix_images)]

    label_ids = file_to_feature[im_str_nr]
    
    print 'im_str_id: ', im_str_id, ' \t amount of buildings: ', len(label_ids)

    #loop throught the features associated with label_ids
    for id_i in label_ids:
        #get the feature from the feature list
        f = features[id_i]
        #and find the features associated with the current image [with a valid (!=-1) buildingid]
        if not f['properties']['ImageId'] == unicode(im_str_id):
            print 'something went wrong'
            print 'im_str_id: ', im_str_id, ' ImageID (featurelist): ', f['properties']['ImageId']
        
        if f['properties']['BuildingId'] != -1:
            #get the list of 3d polygon coordinates
            coordinates_3d =  np.squeeze(f['geometry']['coordinates'])
            #get list of 2d polygon coordinates
            coordinates = np.squeeze(np.array([[c[0],c[1]] for c in coordinates_3d],np.float32))
            #print coordinates
            #print coordinates[:,0]
            #print coordinates[:,1]
            #find the associated bounding box coordinates vertex1: [c1x,c1y], vertex2: [c2x,c2y]
            if coordinates.any():
                c1x   = max(np.min(coordinates[:,0])-3.0, 0)
                c1y   = max(np.min(coordinates[:,1])-3.0, 0.0)
                c2x   = min(np.max(coordinates[:,0])+3.0, 406.0)
                c2y   = min(np.max(coordinates[:,1])+3.0, 438.0)
                #print c1x,c2y,c2x,c2y
                if (c1x == c2x) or (c1y == c2y):
                    continue
                
            else:
                continue
            
            #This is what the label looks like in KITTI format                
            label_i = 'building 0.0 0 0.0 {:.2f} {:.2f} {:.2f} {:.2f} 0.0 0.0 0.0 0.0 0.0 0.0 0.0\n'.format(c1x,c1y,c2x,c2y)
            #else:
            #    #This is what the label looks like in KITTI format                
            #    label_i = 'dontcare 0.0 0 0.0 0.0 0.0 1.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0\n'

            #print label_i
            labels.append(label_i)
    
    #remove last \n
    if labels:
        labels[-1]=labels[-1][:-1]
    
    #print labels     
    #Write the feature labels into a file [same name required as input image]             
    outputfile = outputprefix_labels + im_str_id + '.txt'

    #if this is the first building, write to a new file, otherwise append
    labelfile = open(outputfile,'w')
 
    #write the label
    labelfile.writelines(labels)
    #close the document
    labelfile.close()
        
    #write the png image asscociated
    #outputim = outputprefix_images + im_str_id + '.png'
    #cv2.imwrite(outputim,im)
end_time = time.time()

print 'time: ', (end_time-start_time)      
            
