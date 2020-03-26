# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 07:41:23 2020

@author: Utilisateur
"""
from keras.models import load_model
import cv2  
import numpy as np
import sys

sys.path.append('tensorflow-101/model')

#hand_model_path = 'model_alb/model_def_def.h5'
bg = None

class gesture_recognition():
    def __init__(self, hand_model_path):
        self.model_clasify_hand = load_model('model_alb/model_def_def.h5')
        self.categories = ['C', 'F', 'L', 'P', 'O', 'PE']
        self.M = 256
        self.N = 256
        self.B = 3
        print('He cargado la clase : gestos')
    
    def clasify_hand(self, image):
        img = cv2.resize(image, (self.M, self.N)) # Reduce image size so training can be faster
        img = np.stack((img,)*3, axis=-1)
    
        X = np.array(img, dtype="uint8")
        X = X / 255.0
        X = X.reshape(1, self.N, self.M, self.B) # Needed to reshape so CNN knows it's different images
    
        mypred = self.model_clasify_hand.predict([X])
        nclass = np.argmax(mypred)
    
        s = self.categories[nclass]
        p = max(mypred[0])
    
        return(s,p)
        
        # Function - To find the running average over the background
    def run_avg(self,image, accumWeight):
        global bg
    
        if bg is None:
            bg = image.copy().astype("float")
            return
    
        cv2.accumulateWeighted(image, bg, accumWeight)
        
    # Function - To segment the region of hand in the image
    def segment(self,image, threshold=30):
    
        global bg
    
        diff = cv2.absdiff(bg.astype("uint8"), image)
        thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
        cnts = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cnts = cnts[0]
        if len(cnts) == 0:
            return
        else:
            segmented = max(cnts, key=cv2.contourArea)
            return (thresholded, segmented)
    
    def calcu_hand(self,segmented):
        c = segmented
        
        # determine the most extreme points along the contour
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])
        
        # EXTREAMOS PARA RECORTAR
        v = np.zeros((4,2))
        v[0],v[1],v[2],v[3] = extLeft,extRight,extTop,extBot
        
        # mnimos y maximos
        xmin = int(min(v[:,0])*0.8)
        xmax = int(max(v[:,0])*1.1)
        ymin = int(min(v[:,1])*0.6)
        ymax = int(max(v[:,1])*1.1)
        
        return xmin,xmax,ymin,ymax