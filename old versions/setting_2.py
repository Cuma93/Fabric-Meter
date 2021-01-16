import os
import time
import RPi.GPIO as GPIO
import yaml
from StepperLib import *
import cv2
import numpy as np




def read_position (file_name):
	file = open("file_name", 'r')
	pos = file.read()
	position = pos
	file.close()
	
	return int(position)


def save_position(file_name, position):
	file = open("file_name", 'w+')
	file.write(str(position))
	file.close()





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
	
    if(puntatoreposizione == 2):
        save_position("position.txt", pos[2])
    
            
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Funzione RESET motori

def stepR (steptypeR):                # Steptype è il metodo di reset. Eventualmente si può fare un reset diverso facendo andare a zero i motori in modo diverso. 
	
	GPIO.output(dirP[0], GPIO.LOW)
	GPIO.output(dirP[1], GPIO.LOW)
	#GPIO.output(dirP[2], GPIO.LOW)
	GPIO.output(dirP[3], GPIO.LOW)
    
    # Posizione 0 ---> 4 motori estensione
    # Posizione 1 ---> motore tensionatore
    # Posizione 2 ---> motore allineamento
    # Posizione 3 ---> motore videocamera
    
	microR = (1000, 100, 100, 100)  # Setta la velocità di reset
    
	if (steptypeR == 5):  # Reset motori uno per volta
		while (GPIO.input(proxy_distensori) == True):
			GPIO.output(stepperP[0], GPIO.HIGH)
			time.sleep(microR[0]/1000000)
			GPIO.output(stepperP[0], GPIO.LOW)
			time.sleep(microR[0]/1000000)
		while (GPIO.input(proxy_tensionatore) == True):
			GPIO.output(stepperP[1], GPIO.HIGH)
			time.sleep(microR[1]/1000000)
			GPIO.output(stepperP[1], GPIO.LOW)
			time.sleep(microR[1]/1000000)
		stepC(328, 2)
		while (GPIO.input(proxy_videocamera) == True):
			GPIO.output(stepperP[3], GPIO.HIGH)
			time.sleep(microR[3]/1000000)
			GPIO.output(stepperP[3], GPIO.LOW)
			time.sleep(microR[3]/1000000)
		while (GPIO.input(proxy_focus) == True):
			moveStep2(1,3,1)    # prende in ingresso: direzione (0/1), millisecondi (3 è il limite minimo di sicurezza), numero di step. '''
        
		pos[0]=0
		pos[1]=0
		pos[3]=0
		pos[4]=0
    
    #print("Il sistema è pronto.")
    
    
	if (steptypeR == 0):    # Reset motori distensione
		while (GPIO.input(proxy_distensori) == True):
			GPIO.output(stepperP[0], GPIO.HIGH)
			time.sleep(microR[0]/1000000)
			GPIO.output(stepperP[0], GPIO.LOW)
			time.sleep(microR[0]/1000000)
        
		pos[0]=0
    
    #print("Il sistema è pronto.")
    
    
	if (steptypeR == 1):    # Reset motore tensionatore
		while (GPIO.input(proxy_tensionatore) == True):
			GPIO.output(stepperP[1], GPIO.HIGH)
			time.sleep(microR[1]/1000000)
			GPIO.output(stepperP[1], GPIO.LOW)
			time.sleep(microR[1]/1000000)
       
		pos[1]=0

    #print("Il sistema è pronto.")
    
    
	if (steptypeR == 2):    # Reset motore allineamento
		stepC(328,2)
    
    #print("Il sistema è pronto.")
    
    
	if (steptypeR == 3):    # Reset motore avanzamento videocamera
		while (GPIO.input(proxy_videocamera) == True):
			GPIO.output(stepperP[3], GPIO.HIGH)
			time.sleep(microR[3]/1000000)
			GPIO.output(stepperP[3], GPIO.LOW)
			time.sleep(microR[3]/1000000)
        
		pos[3]=0
    
    #print("Il sistema è pronto.")


	if (steptypeR == 4):    # Reset motore focus videocamera
		while (GPIO.input(proxy_focus) == True):
			moveStep2(1,3,1)    # prende in ingresso: direzione (0/1), millisecondi (3 è il limite minimo di sicurezza), numero di step
          
		pos[4]=0
    
    #print("Il sistema è pronto.")
		
	if (steptypeR == 6):    # Reset combinato videocamera e bobina mobile
		while (GPIO.input(proxy_videocamera) == True or GPIO.input(proxy_tensionatore) == True):
			
			if (GPIO.input(proxy_videocamera) == True and GPIO.input(proxy_tensionatore) == True):
				while (GPIO.input(proxy_videocamera) == True and GPIO.input(proxy_tensionatore) == True):
					GPIO.output(stepperP[3], GPIO.HIGH)
					GPIO.output(stepperP[1], GPIO.HIGH)
					time.sleep(50/1000000)
					GPIO.output(stepperP[3], GPIO.LOW)
					GPIO.output(stepperP[1], GPIO.LOW)
					time.sleep(50/1000000)
						
			if (GPIO.input(proxy_videocamera) == True and GPIO.input(proxy_tensionatore) == False):
				while (GPIO.input(proxy_videocamera) == True and GPIO.input(proxy_tensionatore) == False):
					GPIO.output(stepperP[3], GPIO.HIGH)
					time.sleep(microR[3]/1000000)
					GPIO.output(stepperP[3], GPIO.LOW)
					time.sleep(microR[3]/1000000)
					
			if (GPIO.input(proxy_videocamera) == False and GPIO.input(proxy_tensionatore) == True):
				while (GPIO.input(proxy_videocamera) == False and GPIO.input(proxy_tensionatore) == True):
					GPIO.output(stepperP[1], GPIO.HIGH)
					time.sleep(microR[1]/1000000)
					GPIO.output(stepperP[1], GPIO.LOW)
					time.sleep(microR[1]/1000000)
					
			
		pos[1]=0
		pos[3]=0
# ----------------------------------------------------------------------------------------------------------------------------------------------------

# FUNZIONE PER IL SETUP INIZIALE

def setting():
	
	
	GPIO.setmode(GPIO.BOARD)   # Assegna ai pin la numerazione convenzionale. Usare "GPIO.setmode(GPIO.BCM)" per la numerazione hardware.

	global dir_distensori, pull_distensori, dir_tensionatore, pull_tensionatore, dir_allineamento, pull_allineamento, dir_videocamera, pull_videocamera
	global bobina_mobile, bobina_fissa, bobina_distensione
	global proxy_tensionatore, proxy_allineamento, proxy_distensori, proxy_focus, proxy_videocamera, laser

	#------------------------
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
	GPIO.setup(dir_distensori, GPIO.OUT, initial=0)
	GPIO.setup(pull_distensori, GPIO.OUT, initial=0)
	GPIO.setup(dir_tensionatore, GPIO.OUT, initial=0)
	GPIO.setup(pull_tensionatore, GPIO.OUT, initial=0)
	GPIO.setup(dir_allineamento, GPIO.OUT, initial=0)
	GPIO.setup(pull_allineamento, GPIO.OUT, initial=0)
	GPIO.setup(dir_videocamera, GPIO.OUT, initial=0)
	GPIO.setup(pull_videocamera, GPIO.OUT, initial=0)

	#GPIO.setup(24, GPIO.OUT, initial=1)
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
	
	global dirP, stepperP, microP
	
	dirP = (31, 36, 40, 35)
	stepperP = (29, 37, 38, 33)
	microP = (10000, 50, 200, 100)  # Tempo in microsecondi tra due step
	

	# Posizione iniziale motore in step
	global inizio_distensione, inizio_tensionamento, inizio_allinemanento, inizio_videocamera, inizio_focus 
	
	inizio_distensione = 0
	inizio_tensionamento = 0
	inizio_allinemanento = read_position("position.txt")
	inizio_videocamera = 0
	inizio_focus = 0

	global pos
	pos = [inizio_distensione, inizio_tensionamento, inizio_allinemanento , inizio_videocamera, inizio_focus]   #contatore passi
	
	global Setting
	Setting = True
	

	



