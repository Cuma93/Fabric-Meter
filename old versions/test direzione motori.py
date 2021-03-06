import os
import time
import RPi.GPIO as GPIO
import yaml
from StepperLib import *
import cv2



GPIO.setmode(GPIO.BOARD)   # Assegna ai pin la numerazione convenzionale. Usare "GPIO.setmode(GPIO.BCM)" per la numerazione hardware.

# Assegnazione pin motori
dir_distensori = 31
pull_distensori = 29
dir_tensionatore = 36
pull_tensionatore = 37
dir_allineamento = 40
pull_allineamento = 38
dir_videocamera = 35
pull_videocamera = 33

# Assegnazione pin bobine
bobina_mobile = 12
bobina_fissa = 11
bobina_distensione = 10

# Assegnazione pin sensore
proxy_tensionatore = 21
proxy_allineamento = 18
proxy_distensori = 19
proxy_focus = 13
proxy_videocamera = 15
laser = 16


# Setup GPIO input/output
setup2() # Setup del mini step (vedi libreria StepperLib.py)
GPIO.setup(31, GPIO.OUT, initial=0)
GPIO.setup(29, GPIO.OUT, initial=0)
GPIO.setup(36, GPIO.OUT, initial=0)
GPIO.setup(37, GPIO.OUT, initial=0)
GPIO.setup(40, GPIO.OUT, initial=0)
GPIO.setup(38, GPIO.OUT, initial=0)
GPIO.setup(35, GPIO.OUT, initial=0)
GPIO.setup(33, GPIO.OUT, initial=0)

GPIO.setup(24, GPIO.OUT, initial=1 )
GPIO.setup(bobina_mobile, GPIO.OUT, initial=1)
GPIO.setup(bobina_fissa, GPIO.OUT, initial=1)
GPIO.setup(bobina_distensione, GPIO.OUT, initial=0)

GPIO.setup(proxy_tensionatore, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(proxy_allineamento, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(proxy_distensori, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(proxy_focus, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(proxy_videocamera, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(laser, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# DEFINIZIONE MOTORI
# Posizione 0 ---> 4 motori estensione
# Posizione 1 ---> motore tensionatore
# Posizione 2 ---> motore allineamento
# Posizione 3 ---> motore videocamera

dirP = (31, 36, 40, 35)
stepperP = (29, 37, 38, 33)
microP = (10000, 50, 5000, 200)  # Tempo in microsecondi tra due step

# Posizione iniziale motore in step
inizio_distensione = 0
inizio_tensionamento = 10000
inizio_allinemanento = 325
inizio_videocamera = 0
inizio_focus = 0

pos = [inizio_distensione, inizio_tensionamento, inizio_allinemanento , inizio_videocamera, inizio_focus]   #contatore passi

#______________________________________________________________________________________
#
# DEFINIZIONE FUNZIONI
#______________________________________________________________________________________

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
    micro0 = microR[0]
    micro1 = microR[1]
    micro2 = microR[2]
    micro3 = microR[3]

    if (steptypeR == 0):    # Reset motori uno per volta
     
        '''while (GPIO.input(proxy_distensori) == True):
          GPIO.output(stepperP[0], GPIO.HIGH)
          time.sleep(micro0/1000000)
          GPIO.output(stepperP[0], GPIO.LOW)
          time.sleep(micro0/1000000)
        while (GPIO.input(proxy_tensionatore) == True):
          GPIO.output(stepperP[1], GPIO.HIGH)
          time.sleep(micro1/1000000)
          GPIO.output(stepperP[1], GPIO.LOW)
          time.sleep(micro1/1000000)
        while (GPIO.input(proxy_allineamento) == True):
          GPIO.output(stepperP[2], GPIO.HIGH)
          time.sleep(microR[2]/1000000)
          GPIO.output(stepperP[2], GPIO.LOW)
          time.sleep(microR[2]/1000000)'''
        while (GPIO.input(proxy_videocamera) == True):
          GPIO.output(stepperP[3], GPIO.HIGH)
          time.sleep(micro3/1000000)
          GPIO.output(stepperP[3], GPIO.LOW)
          time.sleep(micro3/1000000)
        '''while (GPIO.input(proxy_focus) == True):
          moveStep2(1,3,1)'''    # prende in ingresso: direzione (0/1), millisecondi (3 è il limite minimo di sicurezza), numero di step.
        
    pos[0]=0
    pos[1]=0
    pos[2]=0
    pos[3]=0
    pos[4]=0
    
    #print("Il sistema è pronto.")
#______________________________________________________________________________________
#
# AVVIO CICLO MACCHINA
#______________________________________________________________________________________


stepR(0)
#GPIO.output(bobina_mobile, GPIO.LOW)
#GPIO.output(bobina_distensione, GPIO.LOW)
#time.sleep(1)
#stepC(500, 0)


#stepC(420, 0)

#GPIO.output(bobina_fissa, GPIO.LOW)
#moveStep2(0,8,20)
#count = 20
#while (GPIO.input(proxy_focus) == True):
#    moveStep2(0,8,1)
#    count = count + 1
#print("Il focus ha una corsa di: " + str(count) + ' steps.') 


#GPIO.output(dirP[2], GPIO.HIGH)
#while (GPIO.input(proxy_allineamento) == True):
 #   GPIO.output(stepperP[2], GPIO.HIGH)
  #  time.sleep(5000/1000000)
  #  GPIO.output(stepperP[2], GPIO.LOW)
  #  time.sleep(5000/1000000)
  #  pos[2] = pos[2] + 1



GPIO.cleanup()
