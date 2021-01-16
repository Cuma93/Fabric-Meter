import os
import time
import RPi.GPIO as GPIO
import yaml
from StepperLib import *
import cv2
import numpy as np

# Funzione di controllo motori step

def stepC (stepfinal, puntatoreposizione):    # (numero di step destinazione, numero identificativo motore) 
    dirPin = dirP[puntatoreposizione]
    stepperPin = stepperP[puntatoreposizione]
    micro = microP[puntatoreposizione]
    dir=0

    if(stepfinal>pos[puntatoreposizione]):
        GPIO.output(dirPin, GPIO.HIGH)
        dir=1
    else:
        GPIO.output(dirPin, GPIO.LOW)
        dir=0
    
    while (stepfinal != pos[puntatoreposizione]):
        GPIO.output(stepperPin, GPIO.HIGH)
        time.sleep(micro/1000000)
        GPIO.output(stepperPin, GPIO.LOW)
        time.sleep(micro/1000000)
        
        if(dir==1):
            pos[puntatoreposizione] = pos[puntatoreposizione] + 1
        else:
            pos[puntatoreposizione] = pos[puntatoreposizione] - 1
            
            
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Funzione RESET motori

def stepR (steptypeR):                # Steptype è il metodo di reset. Eventualmente si può fare un reset diverso facendo andare a zero i motori in modo diverso. 
    GPIO.output(dirP[0], GPIO.LOW)
    GPIO.output(dirP[1], GPIO.LOW)
    GPIO.output(dirP[2], GPIO.LOW)
    GPIO.output(dirP[3], GPIO.LOW)
    
    # Posizione 0 ---> 4 motori estensione
    # Posizione 1 ---> motore tensionatore
    # Posizione 2 ---> motore allineamento
    # Posizione 3 ---> motore videocamera
    
    microR = (1000, 100, 100, 100)  # Setta la velocità di reset
    
    if (steptypeR == 5):  # Reset motori uno per volta
        while (GPIO.input(proxy_distensori) == True):
            GPIO.output(stepperP[0], GPIO.HIGH)
            time.sleep(micro[0]/1000000)
            GPIO.output(stepperP[0], GPIO.LOW)
            time.sleep(micro[0]/1000000)
        while (GPIO.input(proxy_tensionatore) == True):
            GPIO.output(stepperP[1], GPIO.HIGH)
            time.sleep(microR[1]/1000000)
            GPIO.output(stepperP[1], GPIO.LOW)
            time.sleep(microR[1]/1000000)
        while (GPIO.input(proxy_allineamento) == True):
            GPIO.output(stepperP[2], GPIO.HIGH)
            time.sleep(microR[2]/1000000)
            GPIO.output(stepperP[2], GPIO.LOW)
            time.sleep(microR[2]/1000000)
        while (GPIO.input(proxy_videocamera) == True):
            GPIO.output(stepperP[3], GPIO.HIGH)
            time.sleep(micro3/1000000)
            GPIO.output(stepperP[3], GPIO.LOW)
            time.sleep(micro3/1000000)
        while (GPIO.input(proxy_focus) == True):
            moveStep2(1,3,1)    # prende in ingresso: direzione (0/1), millisecondi (3 è il limite minimo di sicurezza), numero di step. '''
        
    pos[0]=0
    pos[1]=0
    pos[2]=0
    pos[3]=0
    pos[4]=0
    
    #print("Il sistema è pronto.")
    
    
    if (steptypeR == 0):    # Reset motori distensione
        while (GPIO.input(proxy_distensori) == True):
            GPIO.output(stepperP[0], GPIO.HIGH)
            time.sleep(micro0/1000000)
            GPIO.output(stepperP[0], GPIO.LOW)
            time.sleep(micro0/1000000)
        
    pos[0]=0
    
    #print("Il sistema è pronto.")
    
    
    if (steptypeR == 1):    # Reset motore tensionatore
        while (GPIO.input(proxy_tensionatore) == True):
            GPIO.output(stepperP[1], GPIO.HIGH)
            time.sleep(micro1/1000000)
            GPIO.output(stepperP[1], GPIO.LOW)
            time.sleep(micro1/1000000)
       
    pos[1]=0

    #print("Il sistema è pronto.")
    
    
    if (steptypeR == 2):    # Reset motore allineamento
        while (GPIO.input(proxy_allineamento) == True):
            GPIO.output(stepperP[2], GPIO.HIGH)
            time.sleep(microR[2]/1000000)
            GPIO.output(stepperP[2], GPIO.LOW)
            time.sleep(microR[2]/1000000)
        
    pos[2]=0
    
    #print("Il sistema è pronto.")
    
    
    if (steptypeR == 3):    # Reset motore avanzamento videocamera
        while (GPIO.input(proxy_videocamera) == True):
            GPIO.output(stepperP[3], GPIO.HIGH)
            time.sleep(micro3/1000000)
            GPIO.output(stepperP[3], GPIO.LOW)
            time.sleep(micro3/1000000)
        
    pos[3]=0
    
    #print("Il sistema è pronto.")


    if (steptypeR == 4):    # Reset motore focus videocamera
        while (GPIO.input(proxy_focus) == True):
            moveStep2(1,3,1)    # prende in ingresso: direzione (0/1), millisecondi (3 è il limite minimo di sicurezza), numero di step
          
    pos[4]=0
    
    #print("Il sistema è pronto.")
    