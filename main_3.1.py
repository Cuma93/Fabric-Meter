################################################################################################
####################################  IMPORTAZIONE LIBRERIE  ###################################
################################################################################################

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

# Librerie GUI
import tkinter as tk #.......................................GUI (principale)
from tkinter.constants import HORIZONTAL, SOLID #............estensione per widget GUI
from tkinter.ttk import Progressbar #........................barre avanzamento
from tkinter import font as tkFont #.........................fonts per GUI

################################################################################################
######################################  FUNZIONI MOTORI  #######################################
################################################################################################

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
            moveStep2(1,3,1)    # prende in ingresso: direzione (0/1), millisecondi (3 è il limite minimo di sicurezza), numero di step
          
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
            moveStep2(1,3,1)    # prende in ingresso: direzione (0/1), millisecondi (3 è il limite minimo di sicurezza), numero di step. '''
        
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
            moveStep2(1,3,1)    # prende in ingresso: direzione (0/1), millisecondi (3 è il limite minimo di sicurezza), numero di step
        
        pos[0]=0
        pos[1]=0
        pos[3]=0
        pos[4]=0


################################################################################################
#########################################  FUNZIONI  ###########################################
################################################################################################

# Funzione per la pulizia frame GUI. Serve ogni volta che si vuole cancellare/aggiornare un elemento della GUI (bottoni, messaggi etc...)
def clear(object):
    slaves = object.grid_slaves()
    for x in slaves:
        x.destroy()

# Funzione che identifica i centri dei fori, li numera.
def detect_hole(frame_gray):  
    holes = hole_cascade.detectMultiScale(frame_gray, 1.1, 22) 
    frame_color = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2BGR)
    #print (len(holes))  # Stampa il numero di fori identificati
    #print(holes)
    marker = 1
    marker2 = 1
    
    coordinates = []
    x_holes = [] # lista delle cordinate X dei centri dei fori
    y_holes = [] # lista delle cordinate Y dei centri dei fori
    for (x, y, w, h) in holes:  
        X = x+w/2   # coordinata x del centro del detecting
        Y = y+h/2   # coordinata y del centro del detecting
        x_holes.append(X)
        y_holes.append(Y)
        coordinates.append([X, Y])
    
    # Ordina le coordinate 
    sorted_coordinates = sorted(coordinates, key=lambda x: (x[0],x[0]))

    for (x, y) in sorted_coordinates:
        cv2.circle(frame_color,(int(x), int(y)), 2, (0, 0, 255), 2)  # disegna il centro dei fori
        cv2.putText(frame_color, str(marker2), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)    # Numera i fori
        marker2 = marker2 + 1
    
    # Seleziona i primi punti
    confidence = np.mean([x[1] for x in sorted_coordinates]) * 0.15
    starting_points = []
    starting_points_coord = []
    for point in enumerate(sorted_coordinates) :
        if len([el[1] for el in sorted_coordinates if (el[1] >= point[1][1] - confidence) & (el[1] <= point[1][1] + confidence) & (el[0] < point[1][0])]) > 0 :
            continue
        else :
            starting_points.append(point[0])     # vettore degli indici dei primi punti
            starting_points_coord.append(sorted_coordinates[point[0]])   # riempie il vettore con le coordinate dei primi punti
    
    # disegna il centro dei primi fori in blu
    for (x, y) in starting_points_coord:
        cv2.circle(frame_color,(int(x), int(y)), 2, (255, 0, 0), 2) 

    return coordinates, starting_points_coord, frame_color   # restiutisce le coordinate di tutti i punti e le coordinate dei primi punti a sx.


# Funzione che restituisce il miglior valore di threshold per ogni immagine
def best_filtering(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    averaging = cv2.blur(gray, (20, 20))
    median = cv2.medianBlur(averaging, 25)
    
    threshold_record = []
    for val in range(60, 170, 5):   # prova diversi valori di threshold. Itera sui valori di threshold predefiniti (scale)
        ret, threshold = cv2.threshold(median, val, 255, cv2.THRESH_BINARY)
        holes_coordinates, _, color = detect_hole(threshold)  # holes_number è il numero dei fori identificati
        threshold_record.append((val, len(holes_coordinates)))  # associa ad un valore di threshold, il corrispettivo numero di fori identificati

    _, val = np.argmax(threshold_record, axis=0)  # trova l'indice dell'elemento con indice 1 comparato con tutti gli elementi con indice 1                                                           quindi il numero di fori trovati più alto.
    best_threshold = threshold_record[val][0] # l'elemento con indice 0 più grande quindi il valore di threshold che corrisponde al numero                                                         più alto di fori trovato.
    ret, thresholded_img = cv2.threshold(median, best_threshold, 255, cv2.THRESH_BINARY)
    
    return thresholded_img, best_threshold  # "thresholded_img" è l'immagine a cui è stato applicato "best_threshold"


# Funzione per eliminare outilers usando la regressione lineare
# Prende in ingresso un array di coordinate dei punti su cui applicare la regressione
def regression(points_coordinates):
    
    coordinates_x = []
    coordinates_y = []
    for x, y in points_coordinates:
        coordinates_x.append(x)
        coordinates_y.append(y)

    x = np.array(coordinates_x)  # creiamo un array delle coordinate x della fascia di controllo 
    y = np.array(coordinates_y)  # creiamo un array delle coordinate y della fascia di controllo

    points_in_band = []  # numero di punti rilevati in ogni riga
    
    if len(coordinates_x) > 1: # se nella fascia sono presenti almeno 2 punti
        # Creazione della fascia di filtraggio
        lim_inf = np.median(y) - 2 * np.std(y)  # il parametro può variare (1 filtro stretto - 3 filtro largo)
        lim_sup = np.median(y) + 2 * np.std(y)
        
        filtred_x = []
        filtred_y = []
        for i, el in enumerate(y):
            if (el > lim_inf) and (el < lim_sup): 
                filtred_y.append(el)   
                filtred_x.append(x[i])
        
        points_in_band.append(len(filtred_x))
        res = stats.linregress(filtred_x, filtred_y)
        
        filtred_coordinates = []
        for i, x in enumerate(filtred_x):   # genera l'array dai due array delle coordinate x e y dei punti
            filtred_coordinates.append([x, filtred_y[i]])
    
    if len(coordinates_x) == 1: # se nella fascia è presente solo un punto
        filtred_x = coordinates_x
        filtred_y = coordinates_y
        filtred_coordinates = [filtred_x[0], filtred_y[0]]
        points_in_band.append(len(filtred_x))

    return points_in_band, filtred_coordinates


# Funzione che prende un immagine in ingresso, coordinate dei fori, coordinate del primo foro di ogni riga e restituisce quanti fori ci devono essere per ogni riga. 
def check_lines(holes_coordinates, first_holes_coordinates, img_color):
    sorted_first_coordinates = sorted(first_holes_coordinates, key=lambda x: (x[1],x[0]))  # ordina le coordinate secondo la y. 
    height, width = img_color.shape[0:2]
    
    # Trova i limiti delle fasce di controllo di ogni riga 
    band_limits = []
    for i, el in enumerate(sorted_first_coordinates):
        
        if (i == 0):
            lim_sup = 0
            lim_inf = (sorted_first_coordinates[1][1] - sorted_first_coordinates[0][1]) / 2 + sorted_first_coordinates[0][1]
            band_limits.append((lim_sup, lim_inf))
        
        if (i > 0) & (i < (len(sorted_first_coordinates) - 1)):
            lim_sup = band_limits[i - 1][1]
            lim_inf = (sorted_first_coordinates[i + 1][1] - sorted_first_coordinates[i][1]) / 2 + sorted_first_coordinates[i][1]
            band_limits.append((lim_sup, lim_inf))

        if (i == (len(sorted_first_coordinates) - 1)):
            lim_sup = band_limits[i - 1][1]
            lim_inf = height
            band_limits.append((lim_sup, lim_inf))

    total_coordinates = []  # array di coordinate dei punti nelle fascia di controllo della singola immagine (inutile)
    number_of_points = []   # array dei numeri di punti trovati in ogni 
    for i, (sup, inf) in enumerate(band_limits):
        cv2.line(img_color,(0, int(round(sup))) , (width, int(round(sup))),(0, 255, 0) ,1)  # limite superiore
        cv2.line(img_color,(0, int(round(inf))) , (width, int(round(inf))),(0, 255, 0) ,1)  # limite inferiore
        
        band_coordinates = []  # salva le coordinate dei punti nella fascia di controllo
        for (x, y) in holes_coordinates:
            if (y < inf) and (y > sup):
                band_coordinates.append([x, y])

        band_coordinates_sorted = sorted(band_coordinates, key=lambda x: (x[0],x[0]))  # ordina le coordinate nella fascia secondo le x
        points_in_band, filtred_coordinates = regression(band_coordinates_sorted)
        number_of_points = number_of_points + points_in_band       # aggiunge il numero di punti trovati su ogni riga
        total_coordinates.append(filtred_coordinates)

    return img_color, number_of_points, total_coordinates


# Calcola il valore più alto di un numero in una lista e la frequenza con cui è presente
def frequency(my_list):
    counter = Counter(my_list)
    max_key = max(counter.keys())
    max_value = counter[max_key]
    frequency = round((max_value / len(my_list)), 2)
    
    if (frequency <= 0.05):
        max_key = max(counter.keys()) - 1
        max_value = counter[max_key]
        frequency = round((max_value / len(my_list)), 2)

    #print("Il valore massimo " + str(max_key) + " ha una frequenza del " + str(frequency))
    return max_key, frequency   # restituisce il valore più alto e la frequenza percentuale


# Applica le deviazioni standard.
# Imput: 4-D array, numero di fori per riga
# Output: vettore distanze tra ogni coppia di fori contigui, mediana delle distanze e distanza minima rilevata.
def distance_x(array, max_points):
    
    distances = []
    for image in array:
        
        for line in image:
            
            if (len(line) == max_points):
                
                for i in range(0, max_points):
                    
                    if (i > 0):
                        dist = line[i][0] - line[i - 1][0]
                        distances.append(dist)
                        
    # Una deviazione standard rappresenta il 68/2 % dei valori attorno alla media
    # Due deviazioni standard rappresentano il 95/2 % dei valori attorno alla media
    # Tre deviazioni standard rappresentano il 99.7/2 % dei valori attorno alla media
    min_dist = np.mean(distances) - 3 * np.std(distances)  # è lo scostamento tra -3sigma e la media dei valori (tre deviazioni standard)
    max_dist = np.mean(distances) + 3 * np.std(distances)  # è lo scostamento tra +3sigma e la media dei valori (tre deviazioni standard)

    return distances, np.median(distances), min_dist


def recognition():

    global hole_cascade
    hole_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Fabric-Meter/hole classifier 2.0/classifier/hole_cascade_2.0.xml')
    
    # Salvataggio di 30 immagini su array per campionamento
    count = 0
    step_count = 1000
    images = [] #......................................................................Array dove vengono salvate le immagini  
    for i in range(0,30):   
        stepC(step_count, 3)
        step_count = step_count + 1000
        ret,frame = cap.read() #.......................................................Legge il frame della videocamera
        
        if ret == True:
            cv2.imshow('preview',frame) #..............................................Output immagine che deve essere salvata
            images.append(frame)  #....................................................Aggiunge le immagini all'array per la successiva elaborazione
            count = count + 1
            time.sleep(0.75)
            cv2.waitKey(1)
        
        
        else:
            print("WARNING! Non arriva il segnale dalla videocamera.")
    
    cv2.destroyWindow('preview') #.....................................................Chiude la vinestra di visualizzazione immagini
    
    
    total_coordinates = []
    detecting = []
    times = []
    total_points = []
    for i, img in enumerate(images):  # richiama la singola immagine salvata nel vettore per l'elaborazione
        start = time.time()
        img_gray, threshold_used = best_filtering(img)
        holes_coordinates, first_holes_coordinates, img_color = detect_hole(img_gray)
        detecting.append(len(holes_coordinates))
        print(threshold_used, len(holes_coordinates))
        image, points_per_band, coordinates = check_lines(holes_coordinates, first_holes_coordinates, img_color)  # restituisce quanti fori                                                                                                                                sono presenti in ogni fascia                                                                                                                           dell'immagine
        total_points =  total_points + points_per_band
        total_coordinates.append(coordinates)
        cv2.imshow("Original Image", img)
        cv2.imshow("AI comput", image)
        cv2.waitKey(1)
        # Progress bar. 
        # Questo pezzo di codice va inserito nel punto in cui si vuole aggiornare la progress bar.
        b = (i + 1) * 100 / len(images)  # valore da incrementare sulla barra ad ogni ciclo di immagine.
        progress_bar['value'] = b 
        objects_frame.update_idletasks()
    
    cv2.destroyAllWindows()
    
    total_points.sort()
    max_value, _ = frequency(total_points)
    _, _, min_distance = distance_x(total_coordinates, max_value)
    check_recognition = True
    
    return check_recognition, max_value, round(min_distance, 1)


################################################################################################
#####################################  FUNZIONI FISICHE  #######################################
################################################################################################
def pi_setup():
    GPIO.setmode(GPIO.BOARD)   # Assegna ai pin la numerazione convenzionale. Usare "GPIO.setmode(GPIO.BCM)" per la numerazione hardware.
    GPIO.setwarnings(False)
    
    global dir_distensori, pull_distensori, dir_tensionatore, pull_tensionatore, dir_allineamento, pull_allineamento, dir_videocamera, pull_videocamera
    global bobina_mobile, bobina_fissa, bobina_distensione
    global proxy_tensionatore, proxy_allineamento, proxy_distensori, proxy_focus, proxy_videocamera, laser

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
        
    global dirP, stepperP, microP
        
    dirP = (dir_distensori, dir_tensionatore, dir_allineamento, dir_videocamera) #.................................pin DIR motori step
    stepperP = (pull_distensori, pull_tensionatore, pull_allineamento, pull_videocamera) #.........................pin PULL motori step
    microP = (10000, 50, 1000, 100) #..............................................................................tempo in microsecondi tra due passi dei motori
        
    # Posizione iniziale motori in step
    global inizio_distensione, inizio_tensionamento, inizio_allinemanento, inizio_videocamera, inizio_focus 
        
    inizio_distensione = 0
    inizio_tensionamento = 0
    inizio_allinemanento = read_position("position.txt") #.........................................................legge la posizione precedentemente salvata su file
    inizio_videocamera = 0
    inizio_focus = 0

    global pos
    pos = [inizio_distensione, inizio_tensionamento, inizio_allinemanento , inizio_videocamera, inizio_focus] #....contatore passi
        
    return True
    

# Esegue le seguenti operazioni:
# - salva in memoria globale i parametri n boccole e forza di tiro
# - controlla la GPIO. Se è piena la svuota. Se è vuota la carica
# - restituisce un True
def setting():
    global set_holes, set_force, check_setting
    set_holes = holes_number.get()
    set_force = forza_tiraggio.get()
    clear(buttons_frame)
    tk.Button(buttons_frame, text="START", command=start, padx=98).grid(row=0, column=0)
    
    pi_setup() # Armamento bobine
    

    clear(message_frame)
    tk.Label(message_frame, text="RESET MOTORI IN ESECUZIONE...").grid(row=0, column=0)
    stepR(7) # reset di tutti i motori
    moveStep2(0,8,90)
    
    clear(message_frame)
    tk.Label(message_frame, text="SISTEMA PRONTO." + "\n\n" + "PREMERE START PER AVVIARE").grid(row=0, column=0)
    
    check_setting = True

################################################################################################
##########################################  MAIN  ##############################################
################################################################################################

# Esegue le seguenti operazioni:
# - esegue caratterizzazione e restituisce: max_points, min_dist e True
# - esegue allineamento e restituisce: True
# - esegue conteggio e aggancia
# - esegue tiraggio restituisce: parametro
# - sgancio e rimozione
def start():
    if (check_setting == True):
        clear(objects_frame)
        clear(buttons_frame)
        
        global progress_bar
        progress_bar = Progressbar(objects_frame, orient="horizontal", mode="determinate", maximum=100, value=0)
        progress_bar.grid(row=0, column=1)
        
        global cap
        cap = cv2.VideoCapture(0) # We turn the webcam on.
        
        clear(message_frame)
        tk.Label(message_frame, text="RICONOSCIMENTO IN CORSO...").grid(row=0, column=0)
        stepC(150, 0) # Distensione
        check_recognition, holes, min_dist = recognition()
        print("Il numero di fori per linea:  " + str(holes))
        print("La distanza minima tra i fori è: "  + str(min_dist))
        clear(message_frame)
        tk.Label(message_frame, text="RICONOSCIMENTO COMPLETATO").grid(row=0, column=0)
        progress_bar['value'] = 0
        
        '''for i in range(0, 100, 1):
            progress_bar['value'] = i
            objects_frame.update_idletasks() 
            time.sleep(0.01)'''
        
        '''clear(message_frame)
        tk.Label(message_frame, text="ALLINEAMENTO IN CORSO...").grid(row=0, column=0)'''
        GPIO.cleanup()
    

################################################################################################
###########################################  GUI  ##############################################
################################################################################################

# Setup dell'interfaccia
root = tk.Tk()  
root.title("Menu system")
root.geometry("800x1500+1100+0")
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
tk.Scale(objects_frame, label="NUMERO ASOLE", from_=0, to=200, bg="white", activebackground="green", troughcolor="white", width=50, length=300, relief=SOLID, tickinterval=50, orient=HORIZONTAL, variable=holes_number).grid(row=0, column=0) # slider
tk.Scale(objects_frame, label="FORZA TENSIONAMENTO (kg)", from_=0, to=200, bg="white", activebackground="green", troughcolor="white", width=50, length=300, relief=SOLID, tickinterval=50, orient=HORIZONTAL, variable=forza_tiraggio).grid(row=1, column=0) # slider
tk.Button(objects_frame, text="CONFERMA PARAMETRI", command=setting, padx=98).grid(row=2, column=0) # pulsante conferma
 
tk.mainloop()












