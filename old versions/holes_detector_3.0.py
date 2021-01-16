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

dirP = (31, 36, 40, 35)
stepperP = (29, 37, 38, 33)
microP = (10000, 50, 5000, 500)  # Tempo in microsecondi tra due step

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
    
    microR = (1000, 100, 100, 100)  # Setta la velocità di reset
    micro0 = microR[0]
    micro1 = microR[1]
    micro2 = microR[2]
    micro3 = microR[3]

    if (steptypeR == 0):    # Reset motori uno per volta
     
        while (GPIO.input(proxy_distensori) == True):
          GPIO.output(stepperP[0], GPIO.HIGH)
          time.sleep(micro0/1000000)
          GPIO.output(stepperP[0], GPIO.LOW)
          time.sleep(micro0/1000000)
        '''while (GPIO.input(proxy_tensionatore) == True):
          GPIO.output(stepperP[1], GPIO.HIGH)
          time.sleep(micro1/1000000)
          GPIO.output(stepperP[1], GPIO.LOW)
          time.sleep(micro1/1000000)
        #while (GPIO.input(proxy_allineamento) == True):
         # GPIO.output(stepperP[2], GPIO.HIGH)
         # time.sleep(microR[2]/1000000)
         # GPIO.output(stepperP[2], GPIO.LOW)
         # time.sleep(microR[2]/1000000)
        while (GPIO.input(proxy_videocamera) == True):
          GPIO.output(stepperP[3], GPIO.HIGH)
          time.sleep(micro3/1000000)
          GPIO.output(stepperP[3], GPIO.LOW)
          time.sleep(micro3/1000000)'''
        while (GPIO.input(proxy_focus) == True):
          moveStep2(1,3,1)    # prende in ingresso: direzione (0/1), millisecondi (3 è il limite minimo di sicurezza), numero di step. 
        
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



#inizializza una lista vuota
numbers = []

hole_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Fabric-Meter/hole classifier 2.0/classifier/hole_cascade_2.0.xml') # caricamento del classificatore per fori ad immafine filtrata
edge_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Fabric-Meter/edge classifier/classifier/cascade.xml') # caricamento del classificatore per i bordi


def detect(gray, frame):  #open cv prende in ingresso solo l'immagine in bianco e nero e non un video
    holes = hole_cascade.detectMultiScale(gray, 1.3, 5)
    print (len(holes))
   
    
    for (x,y,w,h) in holes:
        holesCy=int(y+h/2)  #prende come riferimento la metà dell'altezza in Y del quadrato detection
        lineCy=height-300   #identifica una linea non visibile ad altezza height-300. 
        
        if(holesCy)<=lineCy+6 and (holesCy)>=lineCy-6:  #se la metà dell'altezza del quadrato detection si trova in un intorno (della linea identificata ) compreso tra +6 e -6
            numbers.append(1)                           #somma +1 al contatore
        
        
        
        cv2.line(frame,(500, 0),(500, height),(0, 0, 255) ,2)  #traccia la linea per il contatore. Le parentesi sono le cordinate. Il centro è nell angolo alto a sx incremento è basso dx.  
        #cv2.putText(frame, str(len(numbers)),(300, 30), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        #cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 255, 0), 2)
        cv2.circle(frame,(int(x+w/2), int(y+h/2)), 2, (0, 0, 255), 2)  # disegna il centro dei fori
        print("Cordinata y: " + str(y+h/2))
        print("Cordinata x: " + str(x+w/2))
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        holesCx=int(x+w/2)  #prende come riferimento la metà della larghezza in X del quadrato detection
        lineSpikeCy=int(height/2)  #identifica una linea non visibile messa in corrispondenza dell'asse y del cerchio
        lineSpikeCx=int(width/2)   #identifica una linea non visibile messa in corrispondenza dell'asse x del cerchio
        
        if(holesCy)<=lineSpikeCy+7 and (holesCy)>=lineSpikeCy-7:
            if(holesCx)<=lineSpikeCx+7 and (holesCx)>=lineSpikeCx-7:
                print("FIRE!")
                
    return frame
        
    #for (ex, ey, ew, eh) in edges: 
         #cv2.rectangle(roi_color,(ex, ey),(ex+ew, ey+eh), (0, 255, 0), 2) # We paint a rectangle around the eyes, but inside the referential of the face.

def detect1(gray, frame): # Funzione che identifica i bordi
    edges = edge_cascade.detectMultiScale(gray, 1.1, 22) # We apply the detectMultiScale method to locate one or several edges in the image.
    for (x, y, w, h) in edges: 
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) # We paint a rectangle around edges.
        roi_gray = gray[y:y+h, x:x+w] # We get the region of interest in the black and white image.
        roi_color = frame[y:y+h, x:x+w] # We get the region of interest in the colored image.
    return frame # We return the image with the detector rectangles.


def unsharp_mask(image, amount, kernel_size=(5, 5), sigma=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened
    
#GPIO.output(bobina_distensione, GPIO.LOW)
#stepR(0)
#time.sleep(0.5)
#moveStep2(0,8,90)   # 90 x sfocato 100 per nitido
#stepC(5000, 3)

video_capture = cv2.VideoCapture(0) # We turn the webcam on.
            
while True: # We repeat infinitely (until break):
    _, frame = video_capture.read() # We get the last frame.
    height, width = frame.shape[0:2]   
          
   
    # applicazione filtri
    #median_3 = cv2.medianBlur(frame, 27)
    #unsharp_4 = unsharp_mask(median_3, 13)
    # cambio di colore pixel
    #image = unsharp_4.copy()!!!!
    image = frame.copy()
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV) 
    #grey_lo=np.array([1,1,1])
    #grey_hi=np.array([254,254,254])
    #mask=cv2.inRange(hsv,grey_lo,grey_hi)
    #image[mask>0]=(0,0,0)
    # applicazione filtri singoli
    #bilateral_6 = cv2.bilateralFilter(image, 9, 350, 350)
    median_7 = cv2.medianBlur(image, 15)
    #unsharp_8 = unsharp_mask(median_7, 2)
    
    gray = cv2.cvtColor(median_7, cv2.COLOR_BGR2GRAY) # We do some colour transformations.
    canvas = detect(gray, median_7) # We get the output of our detect function.
    #cv2.line(unsharp_8,(500, 0),(500, height),(0,0,255),2)  #traccia la linea verticale per il contatore. Le parentesi sono le cordinate. Il centro è nell angolo alto a sx incremento è basso dx.  
    #cv2.putText(unsharp_8, "HOLES COUNTER: ", (15,30), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    #cv2.circle(unsharp_8,(int(width/2), int(height/2)), 10, (0,255,0), 2)
 
    cv2.imshow('Filter', canvas) # We display the outputs.
    cv2.imshow('Original', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): # If we type on the keyboard:
        #print("L'immagine è " + str(height) + "x" + str(width))  #stampa le dimensioni del frame
        break # We stop the loop.
    


video_capture.release() # We turn the webcam off.
cv2.destroyAllWindows() # We destroy all the windows inside which the images were displayed.

#GPIO.cleanup()