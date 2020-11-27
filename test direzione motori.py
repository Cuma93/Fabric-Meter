import os
import time
import RPi.GPIO as GPIO


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

# Setup GPIO input/output
GPIO.setup(31, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

GPIO.setup(bobina_mobile, GPIO.OUT)
GPIO.setup(bobina_fissa, GPIO.OUT)
GPIO.setup(bobina_distensione, GPIO.OUT)

# DEFINIZIONE MOTORI
# Posizione 0 ---> 4 motori estensione
# Posizione 1 ---> motore tensionatore
# Posizione 2 ---> motore allineamento
# Posizione 3 ---> motore videocamera

dirP = (31, 36, 40, 35)
stepperP = (29, 37, 38, 33)
microP = (200, 200, 5000, 200)  # Tempo in microsecondi tra due step

# Posizione iniziale motore in step
inizio_estensione = 0
inizio_tensionamento = 0
inizio_allinemanento = 0
inizio_videocamera = 0

pos = [inizio_estensione, inizio_tensionamento, inizio_allinemanento , inizio_videocamera]   #contatore passi

#______________________________________________________________________________________
#
# DEFINIZIONE FUNZIONI
#______________________________________________________________________________________

# Funzione di controllo motori step

def stepC (stepfinal, puntatoreposizione):
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
#
# AVVIO CICLO MACCHINA
#______________________________________________________________________________________

#stepC(100, 0)
#setup2()
#moveStep2(0,3,500)  #il motore impiega 512 step/giro

#stepC(0, 0)
#stepC(100, 2)
GPIO.output(bobina_mobile, GPIO.LOW)
GPIO.output(bobina_fissa, GPIO.LOW)
for i in range (0, 10):
    GPIO.output(bobina_distensione, GPIO.HIGH)
    time.sleep(1/10)
    GPIO.output(bobina_distensione, GPIO.LOW)
    time.sleep(1/10)
    print("ha fatto" + str(i+1) + "cicli")
GPIO.cleanup()
