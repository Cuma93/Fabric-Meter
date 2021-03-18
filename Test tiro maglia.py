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

# Legge la posizione da file
def read_position (file_name):
    file = open(file_name, 'r')
    pos = file.read()
    position = pos
    file.close()
    
    return int(position)


# Salva la posizione su file
def save_position(file_name, position):
    file = open(file_name, 'w+')
    file.write(str(position))
    file.close()



GPIO.setmode(GPIO.BOARD)   # Assegna ai pin la numerazione convenzionale. Usare "GPIO.setmode(GPIO.BCM)" per la numerazione hardware.

### Assegnazione pin
# Pin motori
dir_distensori = 31
pull_distensori = 29
dir_tensionatore = 36
pull_tensionatore = 37
dir_allineamento = 40
pull_allineamento = 38
dir_videocamera = 35
pull_videocamera = 33

# Pin bobine
bobina_mobile = 12
bobina_fissa = 11
bobina_distensione = 10
    
# Pin sensori
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
microP = (10000, 50, 1000, 100)  # Tempo in microsecondi tra due step

# Posizione iniziale motore in step
inizio_distensione = 0
inizio_tensionamento = 0
inizio_allinemanento = read_position("position.txt") #.........................................................legge la posizione precedentemente salvata su file
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

    if (puntatoreposizione == 2):  # condizioni solo per il motore allineamento
        if (stepfinal >= 0 and stepfinal <= 680):
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
            
        else:    # se stepfinal < 0 steps o stepfinal > 680 steps
            print("WARNING! L'allineamento ha raggiunto il finecorsa.")
        
    else:     # condizioni per tutti gli altri motori
        
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
    GPIO.output(dirP[3], GPIO.LOW)
    
    # Posizione 0 ---> 4 motori estensione
    # Posizione 1 ---> motore tensionatore
    # Posizione 2 ---> motore allineamento
    # Posizione 3 ---> motore videocamera
    
    microR = (1000, 100, 100, 100)  # Setta la velocità di reset
    
    #--------------------------------------------------------------------------------------------------------------------------------------------
    # Reset motori distensione
    if (steptypeR == 0):    
        while (GPIO.input(proxy_distensori) == True):
            GPIO.output(stepperP[0], GPIO.HIGH)
            time.sleep(microR[0]/1000000)
            GPIO.output(stepperP[0], GPIO.LOW)
            time.sleep(microR[0]/1000000)
        
        pos[0]=0

    #--------------------------------------------------------------------------------------------------------------------------------------------
    # Reset motore tensionatore
    if (steptypeR == 1):    
        while (GPIO.input(proxy_tensionatore) == True):
            GPIO.output(stepperP[1], GPIO.HIGH)
            time.sleep(microR[1]/1000000)
            GPIO.output(stepperP[1], GPIO.LOW)
            time.sleep(microR[1]/1000000)
       
        pos[1]=0
        
    #--------------------------------------------------------------------------------------------------------------------------------------------
    # Reset motore allineamento
    if (steptypeR == 2):    
        stepC(328,2)

    #--------------------------------------------------------------------------------------------------------------------------------------------
    # Reset motore avanzamento videocamera
    if (steptypeR == 3):    
        while (GPIO.input(proxy_videocamera) == True):
            GPIO.output(stepperP[3], GPIO.HIGH)
            time.sleep(microR[3]/1000000)
            GPIO.output(stepperP[3], GPIO.LOW)
            time.sleep(microR[3]/1000000)
        
        pos[3]=0
    
    #--------------------------------------------------------------------------------------------------------------------------------------------
    # Reset motore focus videocamera
    if (steptypeR == 4):    
        while (GPIO.input(proxy_focus) == True):
            moveStep2(0,3,1)    # prende in ingresso: direzione (0/1), millisecondi (3 è il limite minimo di sicurezza), numero di step
          
        pos[4]=0
    
    #--------------------------------------------------------------------------------------------------------------------------------------------
    # Reset tutti motori singolarmente
    if (steptypeR == 5):  
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
            moveStep2(0,3,1)    # prende in ingresso: direzione (0/1), millisecondi (3 è il limite minimo di sicurezza), numero di step. '''
        
        pos[0]=0
        pos[1]=0
        pos[3]=0
        pos[4]=0
    
    #--------------------------------------------------------------------------------------------------------------------------------------------
    # Reset combinato videocamera e bobina mobile
    if (steptypeR == 6):    
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
    
    #--------------------------------------------------------------------------------------------------------------------------------------------
    # Reset combinato: videocamera e bobina mobile.
    # Reset singolo: distensione, focus, allineamento.
    if (steptypeR == 7):
        # Reset distensori con allineamento forzato
        if (GPIO.input(proxy_distensori) == True):
            while (GPIO.input(proxy_distensori) == True):
                GPIO.output(stepperP[0], GPIO.HIGH)
                time.sleep(microR[0]/1000000)
                GPIO.output(stepperP[0], GPIO.LOW)
                time.sleep(microR[0]/1000000)
            
            pos[0]=60
                
            stepC(0, 0)


        #---------------------------------------------------------------------------------------------
        # Reset combinato tensionatore e videocamera
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
        
        #-----------------------------------------------------------------------------------------------------------------------------
        # Reset allineamento
        stepC(328,2)
        
        #------------------------------------------------------------------------------------------------------------------------------
        #Reset focus
        while (GPIO.input(proxy_focus) == True):
            moveStep2(0,3,1)    # prende in ingresso: direzione (0/1), millisecondi (3 è il limite minimo di sicurezza), numero di step
        
        pos[0]=0
        pos[1]=0
        pos[3]=0
        pos[4]=0
#______________________________________________________________________________________
#
# AVVIO CICLO MACCHINA
#______________________________________________________________________________________
global cap, switch, count
cap = cv2.VideoCapture(0) # We turn the webcam on.
switch = True
count = 0

def video():
    def video_on():
        
        while(switch == True):
            _,frame = cap.read()
            height, width = frame.shape[0:2]
            cv2.line(frame,(0, round(height/2)) , (width, round(height/2)),(0, 255, 0) ,1)  # linea mezzeria
            cv2.line(frame,(0, round(height/2 +30)) , (width, round(height/2 +30)),(0, 255, 0) ,1)
            cv2.line(frame,(0, round(height/2 -30)) , (width, round(height/2 -30)),(0, 255, 0) ,1)
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

def distensione():
	stepC(198, 0) # Distensione

def tensionamento():
    contatore_tensionamento = pos[1]
    contatore_tensionamento = contatore_tensionamento + 1000
    stepC(contatore_tensionamento,1)
    print(pos[1])

def reset():
    #GPIO.output(bobina_fissa, GPIO.LOW)
    stepR(1)
    stepR(0)
    #stepR(4)
    #time.sleep(0.5)
    #moveStep2(1,3,445)

def alza_bobine_tens():
	GPIO.output(bobina_mobile, GPIO.LOW)
	GPIO.output(bobina_fissa, GPIO.LOW)

def reset_distensione():
    stepR(0)

def reset_bobine_centrali():
	GPIO.output(bobina_mobile, GPIO.HIGH)
	GPIO.output(bobina_fissa, GPIO.HIGH)

def assestamento_distensione():
	posizione = pos[0]
	for i in range(0,4):
		posizione = posizione - 15
		stepC(posizione, 0)
		time.sleep(0.1)
		posizione = posizione + 15
		stepC(posizione, 0)
		time.sleep(0.1)


def assestamento_tensionamento():
	posizione = pos[1]
	for i in range(0,4):
		posizione = posizione - 500
		stepC(posizione, 1)
		time.sleep(0.1)
		posizione = posizione + 500
		stepC(posizione, 1)
		time.sleep(0.1)
	
	
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
tk.Button(objects_frame, text="ASSESTAMENTO TENSIONAMENTO", command=assestamento_tensionamento, font=helv36, padx=110).grid(row=2, column=0)
tk.Button(objects_frame, text="ASSESTAMENTO DISTENSIONE", command=assestamento_distensione, font=helv36, padx=110).grid(row=3, column=0)
tk.Button(objects_frame, text="DISTENSIONE", command=distensione, font=helv36, padx=141).grid(row=4, column=0)
tk.Button(objects_frame, text="TENSIONAMENTO", command=tensionamento, font=helv36, padx=141).grid(row=5, column=0)
tk.Button(objects_frame, text="ALZA BOBINE CENTRALI", command=alza_bobine_tens, font=helv36, padx=141).grid(row=6, column=0)
tk.Button(objects_frame, text="ABBASSA BOBINE CENTRALI", command=reset_bobine_centrali, font=helv36, padx=141).grid(row=7, column=0)
tk.Button(objects_frame, text="RESET", command=reset, font=helv36, padx=98).grid(row=8, column=0)
tk.Button(objects_frame, text="CLOSE", command=kill, font=helv36, padx=98).grid(row=9, column=0)

tk.mainloop()























