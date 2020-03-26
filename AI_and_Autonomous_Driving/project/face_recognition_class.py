# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 15:25:59 2020

@author: Utilisateur
"""
import sys
sys.path.append('tensorflow-101/model')


from inception_resnet_v1 import *
from PIL import Image
import numpy as np
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras.applications.imagenet_utils import preprocess_input
#import matplotlib.pyplot as plt
import cv2  
from sklearn.externals import joblib
import logging

#facenet_weights = 'model_alb/facenet_weights.h5'
#classif_path = 'model_alb/haarcascade_frontalface_default.xml'
#path_clasify_face = 'model_alb/alb_model_getnames.h5'
#scaler_filename = "model_alb/scaler_face.save"

class facial_reconigtion():
    def __init__(self,facenet_weights, classif_path, path_clasify_face,scaler_filename):
        self.model_facenet = self.carga_modelo(facenet_weights)
        self.names = ['alberto', 'ben_afflek', 'elton_john', 'jerry_seinfeld', 'madonna', 'mindy_kaling']
        self.mface_classifier = cv2.CascadeClassifier(classif_path)   # Extract the pre-trained face detector from an xml file  
        self.model_clasify_face = load_model('model_alb/alb_model_getnames.h5')
        self.scaler =  joblib.load(scaler_filename) 
        logging.info('He cargado la clase : facial')
    
    def carga_modelo(self,facenet_weights):
        ####### CARGA DE MODELO REC FACIAL
        model = InceptionResNetV1()
        model.load_weights(facenet_weights)    
        return model
    
    ###### Preprocesado
    def preprocess_image2(self,img):
        #img = load_img(img, target_size=(160, 160)) #cargamos la imagen en ese tamano
        img = Image.fromarray(img)
        img = img_to_array(img) #convertimos a avector
        img = np.expand_dims(img, axis=0) #metemos dentro de un vector
        img = preprocess_input(img) #preprocesado
        return img
    
    #### predecir embeddings y escalado
    def predict_image(self,im, scaler):
        #produce 128-dimensional representation
        img1_representation = self.model_facenet.predict(self.preprocess_image2(im))[0,:]
        img_out = scaler.transform([img1_representation]) # scaler
        #arr2 = np.expand_dims(arr, axis=0) # sin escaler
        return img_out
    
    ## Auxiliary functions
    def read_image(self,path):
        """ Method to read an image from file to matrix """
        image = cv2.imread(path)
        #image = load_img(path)        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    
    
    def get_faces(self,im):
        """
        It returns an array with the detected faces in an image
        Every face is defined as OpenCV does: top-left x, top-left y, width and height.
        """
        image_copy = np.copy(im)    # To avoid overwriting
        gray = cv2.cvtColor(image_copy, cv2.COLOR_RGB2GRAY) # The filter works with grayscale images
        face_classifier = self.mface_classifier
        faces = face_classifier.detectMultiScale(gray, 1.2, 5) # Detect the faces in image
        return faces
    
        
    def crop_face(self,image,faces):
        fx = 1
        fy = 1
        fyy = 1
        
        f = faces[0]
        x1,y1,x2,y2 = f[0],f[1],f[2],f[3]
        im_crop = image[int(fy*y1):int(fyy*(y1+y2)),int(fx*x1):x1+x2]
        return im_crop
    
    def detect_crop(self,image):
        ## leemos y ponemos la cara
        faces = self.get_faces(image)
        # la recortamos
        if len(faces):
            im = self.crop_face(image,faces)
        else:
            im = image
        im = cv2.resize(im, (160, 160)) 
        return [im, faces]
    
    #### dibujar cara
    def mdrawface(self, face,img,mypred,name_class):
        # -- Dibujamos cara y clase
        x,y,w,h = face[0]
        cv2.rectangle(img, (x,y), (x+w,y+h), (200, 200, 200), 3) #draw rectangle to main image
        precision = str(np.round(max(mypred[0])*100,2))
        #cv2.putText(img, name_class,(30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1)
        #cv2.putText(img, precision,(220,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1)
        return precision
    
    def predice_clase(self, im_face):
        # --- calculamos los embedings
        arr = self.predict_image(im_face,self.scaler)  # 
        # --- predecimos la clase
        mypred = self.model_clasify_face.predict(arr)
        # elegimos la clase
        nclass = np.argmax(mypred)
        return nclass,mypred

#facial_reconigtor = facial_reconigtion(facenet_weights, classif_path, path_clasify_face)
