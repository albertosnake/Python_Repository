# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 19:55:39 2020

@author: Utilisateur
"""

class datacar() :
    def __init__(self):   
        self.autopilot = 1
        self.speed = 30
    
 
 
from queue import Queue 
from threading import Thread, Event
import time

# A thread that produces data 
def producer(out_q): 
    while True: 
       # Produce some data 
       data = datacar()
       time.sleep(3)
       out_q.put(data) 
       time.sleep(2)
       out_q.put(data) 
       time.sleep(2)
       break
                               
# A thread that consumes data 
def consumer(in_q):
    
    while True: 
        if not q.empty():           
            data = in_q.get_nowait()
            
            autopilot = data.autopilot
            speed = data.speed
            time.sleep(1)
            print(data)

           #set_vehicle()  

class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
                               
# Create the shared queue and launch both threads 
q = Queue() 

  
    
t1 = StoppableThread(target = consumer, args =(q, )) # CARLA
t2 = StoppableThread(target = producer, args =(q, ))  # AICA
t1.setDaemon(True)
t2.setDaemon(True)

t1.start() 
t2.start()


#t1.join() 
#t2.join() 



