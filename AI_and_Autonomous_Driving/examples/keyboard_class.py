# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 20:51:48 2020

@author: Utilisateur
"""

from pynput.keyboard import Key, Controller
import time

class keyboard_control():
    def __init__(self):
        self.keyboard = Controller()
        
    def press_alttab(self):
        time.sleep(1)
        self.keyboard.press(Key.alt)
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
        time.sleep(1)
        self.keyboard.release(Key.alt)
    
    def press_up(self,t):
        timeout = time.time() + t
        while time.time() < timeout:
            time.sleep(0.2)
            self.keyboard.press(Key.up)
        self.keyboard.release(Key.up)

    def cmd1(self,t):
        self.press_alttab()
        self.press_up(t)
        
    def autopilot(self):
        self.press_alttab()
        time.sleep(0.5)
        self.keyboard.press('p')
        time.sleep(0.1)
        self.keyboard.release('p')
        
    def autopilot2(self):
        time.sleep(0.5)
        self.keyboard.press('p')
        time.sleep(0.1)
        self.keyboard.release('p')

#https://pythonhosted.org/pynput/keyboard.html#pynput.keyboard.Key