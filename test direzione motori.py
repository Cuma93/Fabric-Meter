import os
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)   # Assegna ai pin la numerazione convenzionale. Usare "GPIO.setmode(GPIO.BCM)" per la numerazione hardware.

dir_distensori = 31
pull_distensori = 29
dir_tensionatore = 36
pull_tensionatore = 37
dir_allineamento = 40
pull_allineamento = 38
dir_videocamera = 35
pull_videocamera = 33

GPIO.setup(31, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

# DEFINIZIONE MOTORI
# Posizione 0 ---> 4 motori estensione
# Posizione 1 ---> motore tensionatore
# Posizione 2 ---> motore allineamento
# Posizione 3 ---> motore videocamera

dirP = (31, 36, 40, 35)
stepperP = (29, 37, 38, 33)
microP = (200, 200, 200, 200)  #

pos = [0, 0, 0, 0]   #contatore passi

#______________________________________________________________________________________
#
# DEFINIZIONE FUNZIONI
#______________________________________________________________________________________

# Funzione di controllo motori step

def stepC (stepfinal, puntatoreposizione):
    dirPin = dirP(puntatoreposizione)
    stepperPin = stepperP(puntatoreposizione)
    micro = microP(puntatoreposizione)
    dir=0

    if(stepfinal>pos[puntatoreposizione]:
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

#------------------------------------------------------------------------------------

# Funzione RESET motori

def stepR (steptypeR):    # Steptype è il metodo di reset. Eventualmente si può fare un reset diverso facendo andare a zero i motori in modo diverso. 
    GPIO.output(dirP[0], GPIO.LOW)
    GPIO.output(dirP[1], GPIO.LOW)
    GPIO.output(dirP[2], GPIO.LOW)
    GPIO.output(dirP[3], GPIO.LOW)
        
    while (GPIO.input(ProxyEstensore, GPIO.HIGH) = True:
          GPIO.output(stepperP(0), GPIO.HIGH)
          time.sleep(micro/1000000)
          GPIO.output(stepperP(0), GPIO.LOW)
          time.sleep(micro/1000000)
    while (GPIO.input(ProxyAllineamento, GPIO.HIGH) = True:
          GPIO.output(stepperP(1), GPIO.HIGH)
          time.sleep(micro/1000000)
          GPIO.output(stepperP(1), GPIO.LOW)
          time.sleep(micro/1000000)
    
    pos[0]=0
    pos[1]=100

#______________________________________________________________________________________

# AVVIO CICLO MACCHINA
#______________________________________________________________________________________

stepC(100, 0)
