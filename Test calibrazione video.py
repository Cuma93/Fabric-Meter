# Librerie generiche
import os #..................................................navigazione cartelle
import yaml  #...............................................caricamento files di configurazione
import RPi.GPIO as GPIO  #...................................abilitazione GPIO Raspberry
from StepperLib import * #...................................attuazione del mini motore step 
import cv2  #............................................... grafica e computer vision
import numpy as np  #........................................operazioni su array
from scipy import stats #....................................oprazioni matematiche complesse su array
from collections import Counter #............................operazioni di riordino su array
import time #................................................delays
import matplotlib.pyplot as plt #............................plottare grafici e funzioni
import threading

# Librerie GUI
import tkinter as tk #.......................................GUI (principale)
from tkinter.constants import HORIZONTAL, SOLID #............estensione per widget GUI
from tkinter.ttk import Progressbar #........................barre avanzamento
from tkinter import font as tkFont #.........................fonts per GUI

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

#GPIO.setup(24, GPIO.OUT, initial=1)
GPIO.setup(bobina_mobile, GPIO.OUT, initial=1)
GPIO.setup(bobina_fissa, GPIO.OUT, initial=1)
GPIO.setup(bobina_distensione, GPIO.OUT, initial=1)

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
microP = (10000, 50, 500, 80)  # Tempo in microsecondi tra due step

# Posizione iniziale motore in step
inizio_distensione = 0
inizio_tensionamento = 0
inizio_allinemanento = 0
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
    
    microR = (1000, 100, 500, 70)  # Setta la velocità di reset
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
        while (GPIO.input(proxy_focus) == True):
          moveStep2(0,3,1)    # prende in ingresso: direzione (0/1), millisecondi (3 è il limite minimo di sicurezza), numero di step. 
        
    pos[0]=0
    pos[1]=0
    #pos[2]=0
    pos[3]=0
    pos[4]=0
    
    if (steptypeR == 1): 
        while (GPIO.input(proxy_tensionatore) == True):
          GPIO.output(stepperP[1], GPIO.HIGH)
          time.sleep(micro1/1000000)
          GPIO.output(stepperP[1], GPIO.LOW)
          time.sleep(micro1/1000000)
        
        pos[1]=0
    
    if (steptypeR == 3): 
        while (GPIO.input(proxy_videocamera) == True):
          GPIO.output(stepperP[3], GPIO.HIGH)
          time.sleep(micro3/1000000)
          GPIO.output(stepperP[3], GPIO.LOW)
          time.sleep(micro3/1000000)
        
        pos[3]=0
    
    if (steptypeR == 4): 
        while (GPIO.input(proxy_focus) == True):
          moveStep2(0,3,1)    # prende in ingresso: direzione (0/1), millisecondi (3 è il limite minimo di sicurezza), numero di step. 
    
        pos[4]=0
#______________________________________________________________________________________
#
# AVVIO CICLO MACCHINA
#______________________________________________________________________________________
global cap, switch, count
cap = cv2.VideoCapture(1) # We turn the webcam on.
switch = True
count = 0

def video():
    def video_on():
        
        while(switch == True):
            _,frame = cap.read()
            cv2.imshow('preview',frame) # We display the outputs.
            cv2.waitKey(1)
            
            if (switch == False):
                break
        
    #cap.release() # We turn the webcam off.
    #cv2.destroyAllWindows()
    
    thread = threading.Thread(target = video_on)
    thread.start()


def switch_on():
    global switch
    switch = True
    video()
    
def switch_off():
    global switch
    switch = False
    video()
    
def start():
    global count
    stepC(1000, 3)
    #stepC(80000, 1)
    '''for i in range(0, 225):
        count = count + 335  
        stepC(count, 3)
        time.sleep(0.5)'''
            
    #cap.release() # We turn the webcam off.
    #cv2.destroyAllWindows() # We destroy all the windows inside which the images were displayed.a

    #GPIO.cleanup()

def reset():
    stepR(1)
    stepR(3)
    stepR(4)
    time.sleep(0.5)
    moveStep2(1,3,440)
    
def kill():
    global switch
    switch = False
    time.sleep(0.3)
    cap.release() # We turn the webcam off.
    cv2.destroyAllWindows()
    root.destroy()
    GPIO.cleanup()

def video_rel():
    global switch
    for i in range(0, 101):
        ret,frame = cap.read()
        reset()
        time.sleep(0.5)
        if ret == True:
            cv2.imwrite('/home/pi/Desktop/Test affidabilità videocamera/' + str(i+1) + '.jpg', frame)
            
        if ret == False:
            print("ERRORE VIDEO")
        
        

    
# Setup dell'interfaccia
root = tk.Tk()  
root.title("Menu system")
root.geometry("800x1500+1100+0")
helv36 = tkFont.Font(family='Helvetica', size=30)
holes_number = tk.IntVar()
forza_tiraggio = tk.DoubleVar()
 
# Creazione dei frames (caselle apposte sul root)
objects_frame = tk.Frame(root)
objects_frame.grid(row=0, column=0)
buttons_frame = tk.Frame(root)
buttons_frame.grid(row=1, column=0)
message_frame = tk.Frame(root)
message_frame.grid(row=2, column=0)

# Pulsanti nella schermata iniziale
tk.Button(objects_frame, text="VIDEO ON", command=switch_on, font=helv36, padx=98).grid(row=0, column=0) # pulsante conferma
tk.Button(objects_frame, text="VIDEO OFF", command=switch_off, font=helv36, padx=110).grid(row=1, column=0) # pulsante conferma
tk.Button(objects_frame, text="RESET", command=reset,  font=helv36, padx=155).grid(row=2, column=0) # pulsante conferma
tk.Button(objects_frame, text="AVVIA TEST", command=start, font=helv36, padx=141).grid(row=3, column=0)
tk.Button(objects_frame, text="TEST AFFIDABILITÀ VIDEO", command=video_rel, font=helv36, padx=141).grid(row=4, column=0)
tk.Button(objects_frame, text="CLOSE", command=kill, font=helv36, padx=98).grid(row=5, column=0)

tk.mainloop()


















