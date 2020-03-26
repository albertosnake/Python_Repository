# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 08:21:33 2020

@author: Utilisateur
"""

class Vehicle_state():
    def __init__(self):
        self.autopilot = False
        
    def aply_control(self, vehicle):
        if self.autopilot == False:
            vehicle.set_autopilot(False)
        else:
            vehicle.set_autopilot(True)

def initialize(): 
    from queue import Queue
    global q
    global veh_st     
    q = Queue()
    veh_st = Vehicle_state()
