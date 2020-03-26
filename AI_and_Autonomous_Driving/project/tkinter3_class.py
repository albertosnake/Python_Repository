# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 11:08:56 2020

@author: Utilisateur
"""
from tkinter import Label, Frame, Button, Tk, StringVar
#from tkinter import *
from PIL import ImageTk, Image

########## CLASS definicion de keyboard
from keyboard_class import keyboard_control


class mbackground():
    def __init__(self,root,mbg, dim):
        
        # selfs
        self.kb = False
        #self.kb = keyboard_control()
        
        # parameter definition
        l1,l2,h0 = dim[0],dim[1],dim[2]
        self.l1 = l1

        # frame definitions
        f1 = Frame(root,width=l1,height=h0,bg=mbg, highlightcolor="green")
        f2 = Frame(root,width=l2,height=h0,bg=mbg, highlightcolor="green")
        f3 = Frame(root,width=l1,height=h0,bg=mbg, highlightcolor="green")
        # place the frames
        f1.place(relx = 0, rely = 0)
        f2.place(x = l1,  y = 0)
        f3.place(x=l1+l2, y = 0)
        
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        
        # labels
        # --- Video
        lvideo = Label(f1)
        lvideo.place(x=0,y=120)
        self.mvideo = lvideo
        
        # --- Hand
        lhand = Label(f1)
        lhand.place(x=0,y=120+int(h0/3))
        self.mhand = lhand
        
        # ---- Nav
        x = 0
        y = 0
        w = l2
        h = int(h0/2)
        self.load_place(f2,"images\maps.jpg",w,h,x,y)
        # --- Status
        x = 0
        y = int(h0/2)
        w = l2
        h = int(h0/2)
        self.load_place(f2,"images\im3.jpg",w,h,x,y)
        #self.change_image(1, w, h, x, y)
        
        # --- Car status
        x = 0
        y = 0
        w = l1
        h = h
        self.load_place(f3,"images\im7.jpg",w,h,x,y)
        self.load_place(f3,"images\im9.png",w,h,x,int(h0/2))
        
        # --- Automation levels
        self.load_place(f1,"images\levels.png",w=l1,h=150,x=0,y=560)
        
        # --- Wellcome
        self.load_place(f1,"images\AICA.png",w=l1,h=100,x=0,y=8)
        
        w = 80
        tam = 24
        
        #labels
        mbg = "black"
        
        ln1 = Label(f1,text="Name :", bg="white",padx=tam,pady=10) # Name label
        ln2 = Label(f1, bg=mbg,padx=tam, fg="SpringGreen", pady=10) # Actual name
        ln3 = Label(f1,text="N_precis :", bg="white",padx=tam,pady=10) # Precision 
        ln4 = Label(f1,bg=mbg,padx=tam, fg="SpringGreen", pady=10) # Actual precission
        
        ln5 = Label(f1,text="Gest :", bg="white",padx=tam,pady=10) # Gest 
        ln6 = Label(f1,bg=mbg,padx=tam, fg="SpringGreen", pady=10) # Actual precission
        ln7 = Label(f1,text="G_precis :", bg="white",padx=tam,pady=10) # Gest 
        ln8 = Label(f1,bg=mbg,padx=tam, fg="SpringGreen", pady=10) # Actual precission
        
        # placement
        n = 50
        
        ln1.place(x=int(l1/2),y=120+int(h0/3)) 
        ln2.place(x=int(l1/2)+w,y=120+int(h0/3))
        ln3.place(x=int(l1/2),y=120+int(h0/3)+n)
        ln4.place(x=int(l1/2)+w,y=120+int(h0/3)+n)
        
        ln5.place(x=int(l1/2),y=120+int(h0/3)+2*n)
        ln6.place(x=int(l1/2)+w,y=120+int(h0/3)+2*n)
        ln7.place(x=int(l1/2),y=120+int(h0/3)+3*n)
        ln8.place(x=int(l1/2)+w,y=120+int(h0/3)+3*n)
        
        # calls
        self.name = ln2
        self.precname =  ln4
        self.gest = ln6
        self.precgest = ln8
        
        # ------------ Buttons
        self.mbutton = 0
        self.mbutton1 = 0
        
        #self.mbutton = Button(f1, text ="FW", command = lambda:self.kb.cmd1(3))        
        #self.mbutton.place(x=int(l1/2), y=120+int(h0/3)+5*n)
        
        #self.mbutton1 = Button(f1, text ="AUTO_P", command = self.kb.autopilot)        
        #self.mbutton1.place(x=int(l1/2), y=120+int(h0/3)+6*n)
        
        print('He cargado la clase : tkinter')
        
    def load_place(self,root,path,w,h,x,y):
        load = Image.open(path)
        load = load.resize((w, h), Image.ANTIALIAS) 
        render = ImageTk.PhotoImage(load, master = root)
        img = Label(root, image=render)
        img.image = render
        img.place(x=x, y=y)
        
    def from_rgb(self,rgb):
        return "#%02x%02x%02x" % rgb
    
    def change_image(self, autopilot,w,h,x,y):
        if autopilot:
            self.load_place(self.f2,"images\im3_green.jpg",w,h,x,y)
            self.load_place(self.f1,"images\levels5.png",w=self.l1,h=150,x=0,y=560)
        else:
            self.load_place(self.f2,"images\im3.jpg",w,h,x,y)
            self.load_place(self.f1,"images\levels3.png",w=self.l1,h=150,x=0,y=560)
            
    
#def do_test():
#    root = Tk() #tkinter class blank window
#    root.geometry('{}x{}'.format(1280, 720))
#    
#    
#    # definimos las dinmensiones
#    msize= 1280
#    
#    l1 = 340
#    l2 = msize - 2*l1
#    h0 = 720
#    
#    dims = [l1,l2,h0]
#    
#    # creamos la clase
#    b =  mbackground(root,"grey",dims)
#    b.name.configure(text = "0")
#    b.precname.configure(text = "0")
#    
#    root.mainloop()
    
#do_test()
