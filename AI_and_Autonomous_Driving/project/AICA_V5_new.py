#!/usr/bin/env python
# coding: utf-8

######## CARGA DE DATOS
#get_ipython().system('git clone https://github.com/serengil/tensorflow-101.git')

############################ librerias
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import load_img, save_img, img_to_array
from keras.applications.imagenet_utils import preprocess_input
import cv2  
import sys
import logging
###librerias gestos
from gesture_recognition_class import gesture_recognition 
### librerias definicion del background
from tkinter3_class import mbackground
from tkinter import Tk
from PIL import ImageTk, Image
### librerias cara
from face_recognition_class import facial_reconigtion
############################ 

import globals

class AICA_class():
    def __init__(self): 
        global bg
        #global q
        
        sys.path.append('tensorflow-101/model')
        
        self.queue = globals.q
        
    	############## CLASS definicion del background
    	# definimos las dinmensiones
        msize= 1280
        l1 = 340
        l2 = msize - 2*l1
        h0 = 720
        self.l1,self.l2,self.h0 = l1,l2,h0
        
        dims = [l1,l2,h0]
    
        self.root = Tk() #tkinter class blank window
        self.root.geometry('{}x{}'.format(msize, h0))
        self.b =  mbackground(self.root,"grey",dims) # creamos la clase

    	############## CLASS cara ###########
        facenet_weights = 'model_alb/facenet_weights.h5'
        classif_path = 'model_alb/haarcascade_frontalface_default.xml'
        path_clasify_face = 'model_alb/alb_model_getnames.h5'
        scaler_filename = "model_alb/scaler_face.save"
    
        self.fr = facial_reconigtion(facenet_weights, classif_path, path_clasify_face, scaler_filename) # creamos la clase
    
    	############## CLASS gestos ###########
        bg = None
    
    	# weight inicial    
        self.accumWeight = 0.5
    	# definimos roi
        self.top, self.right, self.bottom, self.left = 90, 350, 410, 600
        hand_model_path = 'model_alb/model_def_def.h5'
        self.gr = gesture_recognition(hand_model_path) # creamos la clase
        
            
    def run_app(self):
        def video_stream():
            global aica
            global contador
            global num_frames
                
            # leemos de webcam
            ret, img = aica.cap.read()
        
            ################# CARA #######################
            # detectamos y recortamos la cara
            im_face,face = aica.fr.detect_crop(img)
            if len(face):
        
                nclass,mypred = aica.fr.predice_clase(im_face)
                
                contador[nclass] = contador[nclass] + 1
        
                if max(contador) > 30:
                    contador = np.zeros(len(aica.fr.names))
        
                name_class = aica.fr.names[np.argmax(contador)]
                #name_class = names[nclass]
                
                # -- Dibujamos cara y clase
                prec = aica.fr.mdrawface(face,img,mypred,name_class)
                aica.b.name.configure(text=name_class)
                aica.b.precname.configure(text=prec)
                
                
        
            ################# GESTOS #######################    
            # detectamos mano
            #clone = img.copy()
            (height, width) = img.shape[:2]
            roi = img[aica.top:aica.bottom, aica.right:aica.left]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)
            num_frames += 1      
            if num_frames < 30:
                aica.gr.run_avg(gray, aica.accumWeight)
        
                if num_frames == 1:
                    logging.info(">>> Please wait! calibrating...")
                    cv2.putText(img,"CALIB NOK",(30,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,0,0), 1)
                elif num_frames == 29:
                    logging.info(">>> Calibration successfull...")
                    cv2.putText(img,"CALIB OK",(30,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,200,0), 1)
        
            else: ## si hemos calibrado
        
                hand = aica.gr.segment(gray)
        
                if hand is not None:
        
                    (thresholded, segmented) = hand
                    # show the thresholded image
        
                    # calculate points
                    xmin,xmax,ymin,ymax = aica.gr.calcu_hand(segmented)
                    cv2.rectangle(thresholded, (xmin,ymin), (xmax,ymax), (255, 255,255), 3)
                    # draw the segmented hand
                    cv2.rectangle(img, (aica.right + xmin, aica.top + ymin), (xmax + aica.right, aica.top + ymax), (255,0,0), 2)            
                    # Predecimos la mano
                    clase, prob = aica.gr.clasify_hand(thresholded)
                    
                    # autopilot ON
                    if clase == 'C' and prob > 0.8: 
                        globals.veh_st.autopilot = 1
                        globals.q.put(globals.veh_st)
                        aica.b.change_image(1, aica.l2, int(aica.h0/2), 0, int(aica.h0/2))
                    
                    # autopilot OFF
                    if clase == 'L' and prob > 0.7:
                        globals.veh_st.autopilot = 0
                        globals.q.put(globals.veh_st)
                        aica.b.change_image(0, aica.l2, int(aica.h0/2), 0, int(aica.h0/2))
                        #aica.b.kb.autopilot2()
                    #cv2.putText(img, clase,(30,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1)
                    
                    ## dibujamos en el panel
                    cv2image = cv2.resize(thresholded, (int(aica.l1/2), int(aica.h0/3))) 
                    imgh = Image.fromarray(cv2image)
                    imgtkh = ImageTk.PhotoImage(image=imgh)
                    aica.b.mhand.imgtk = imgtkh
                    aica.b.mhand.configure(image=imgtkh)
                    
                    aica.b.gest.configure(text = clase) 
                    aica.b.precgest.configure(text = str(prob)) 
                    
        
            cv2.rectangle(img, (aica.left, aica.top), (aica.right, aica.bottom), (0,255,0), 1)
            
            # cargamos imagen final
            cv2image = cv2.resize(img, (aica.l1, int(aica.h0/3))) 
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            
                
            # asignamos imagen a cara
            aica.b.mvideo.imgtk = imgtk
            aica.b.mvideo.configure(image=imgtk)
            
            # actualizamos el video
            aica.b.mvideo.after(2, video_stream) # delay
        ###################################################################
        self.cap = cv2.VideoCapture(0) #webcam

        # Try to get the first frame
        if self.cap.isOpened(): 
        	rval = True
        else:
        	rval = False
        
        global contador
        global num_frames
        
        contador = np.zeros(len(self.fr.names))
        num_frames = 0
        
        ####### LOOP
        video_stream()
        self.root.mainloop()
        
        #kill open cv things		
        self.cap.release()
        cv2.destroyAllWindows()
        ######################

def AICA_init_and_work():
    global aica
    aica = AICA_class()
    aica.run_app()

