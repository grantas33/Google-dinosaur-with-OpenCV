# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 12:04:38 2017

@author: Vartotojas
"""

import cv2
import numpy as np
from grabscreen import grab_screen
import glob
import pyautogui
import time

dino = cv2.imread('dino.jpg', 0)
w_dino, h_dino = dino.shape[::-1]

files = glob.glob ('cacti/*.jpg')   
cacti = []       
for file in files:
    temp=cv2.imread(file, 0)  
    cacti.append(temp)
 
start_time = time.time() 
frame_time = time.time()
obstacle_height = 0
last_state_crouched = False
should_crouch = False

while(True):
    leftest = 1000            
    jump_dist = 170  +  (time.time() - start_time) *1.82   
    pts = []
    scr = grab_screen(region=(75,250, 750, 450))
   # scr = cv2.cvtColor(scr, cv2.COLOR_BGR2RGB)
    scr_gray = cv2.cvtColor(scr, cv2.COLOR_BGR2GRAY)    
    
    res_dino = cv2.matchTemplate(scr_gray, dino, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc_dino = np.where(res_dino >= threshold)
    
    for pt in zip(*loc_dino[::-1]):
      #  cv2.rectangle(scr, pt, (pt[0] + w_dino, pt[1] + h_dino + 9), (50,205,50), 1)
        dinoX = pt[0] + w_dino
        dinoH = pt[1]
    for cactus in cacti: 
        res = cv2.matchTemplate(scr_gray, cactus, cv2.TM_CCOEFF_NORMED)
        w, h = cactus.shape[::-1]
        loc = np.where(res >= 0.8)
        for pt in zip(*loc[::-1]):
            if(pt in pts):
                continue
          #  cv2.rectangle(scr, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
            pts.append(pt)
            if(leftest > pt[0] + w):
                leftest = pt[0] + w
                obstacle_height = h
                if(h < 20 and pt[1] + 10 < dinoH):
                    should_crouch = True
                elif(should_crouch == True):
                    should_crouch = False
                    pyautogui.keyUp('down')
    
    if(leftest - dinoX < jump_dist - obstacle_height and should_crouch == False):       
        cv2.putText(scr, 'Jump!', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                     2, cv2.LINE_AA) 
        if(dinoH > 110): 
            pyautogui.press('space')
    elif(should_crouch == True):
        pyautogui.keyDown('down')  
        cv2.putText(scr, 'Crouch!', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (30, 255, 10),
                     2, cv2.LINE_AA) 
  
    print(1/(time.time() - frame_time))    
    frame_time = time.time()
        
    cv2.imshow('screen', scr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    