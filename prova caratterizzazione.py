import os
import time
import glob
import numpy as np
from collections import Counter
import cv2
from tkinter import * 
from tkinter.ttk import *
from scipy import stats
import matplotlib.pyplot as plt


# FUNCTIONS

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
def regression(points_coordinates):
    
    coordinates_x = []
    coordinates_y = []
    for x, y in points_coordinates:
        coordinates_x.append(x)
        coordinates_y.append(y)

    x = np.array(coordinates_x)  # creiamo un array delle coordinate x della fascia di controllo 
    y = np.array(coordinates_y)  # creiamo un array delle coordinate y della fascia di controllo
    #print(x)
    #print(y)
    #plt.plot(x, y, 'o', label='original data')
    #plt.show()
    points_in_band = []  # numero di punti rilevati in ogni riga
    
    if len(coordinates_x) > 1: # se nella fascia sono presenti almeno 2 punti
        # Creazione della fascia di filtraggio
        lim_inf = np.median(y) - 2 * np.std(y)  # il parametro può variare (1 filtro stretto - 3 filtro largo)
        lim_sup = np.median(y) + 2 * np.std(y)
        #print("Lim inf =" + str(lim_inf))
        #print("Lim sup =" + str(lim_sup))
        
        filtred_x = []
        filtred_y = []
        for i, el in enumerate(y):
            if (el > lim_inf) and (el < lim_sup): 
                filtred_y.append(el)   
                filtred_x.append(x[i])
        
        points_in_band.append(len(filtred_x))
        #idx = [y.tolist().index(el) for el in y if (el > lim_inf) & (el < lim_sup)]
        #filtred_y = np.array([el for el in y if (el > lim_inf) & (el < lim_sup)])     # modo compatto di creare un array con elementi selezionati
        
        #print("filtred x: " + str(filtred_x))
        #print("filtred y: " + str(filtred_y))
        res = stats.linregress(filtred_x, filtred_y)
        #print(res.slope)
        #print(res.intercept)
        
        filtred_coordinates = []

        for i, x in enumerate(filtred_x):   # genera l'array dai due array delle coordinate x e y dei punti
            filtred_coordinates.append([x, filtred_y[i]])

        '''plt.plot(filtred_x, filtred_y, 'o', label='original data')
        plt.plot(filtred_x, res.intercept + res.slope*np.array(filtred_x), 'r', label='fitted line')  # crea la linea di regressione
        plt.legend()
        plt.show()'''
    
    if len(coordinates_x) == 1: # se nella fascia è presente solo un punto
        filtred_x = coordinates_x
        filtred_y = coordinates_y
        filtred_coordinates = [filtred_x[0], filtred_y[0]]
        points_in_band.append(len(filtred_x))

    return points_in_band, filtred_coordinates


# Funzione che prende un immagine in ingresso, coordinate dei fori, coordinate del primo foro di ogni riga e restituisce quanti fori ci devono essere per ogni riga. 

def check_lines(holes_coordinates, first_holes_coordinates, img_color):
    sorted_first_coordinates = sorted(first_holes_coordinates, key=lambda x: (x[1],x[0]))  # ordina le coordinate secondo la y.
    #print(sorted_first_coordinates)  
    height, width = img_color.shape[0:2]
    
    # Trova i limiti delle fasce di controllo di ogni riga 
    band_limits = []
    for i, el in enumerate(sorted_first_coordinates):
        
        if (i == 0):
            lim_sup = 0
            lim_inf = (sorted_first_coordinates[1][1] - sorted_first_coordinates[0][1]) / 2 + sorted_first_coordinates[0][1]
            band_limits.append((lim_sup, lim_inf))
            #print("Lim sup: " + str(lim_sup))
            #print("Punto centrale: " + str(sorted_first_coordinates[0][1]))
            #print("Lim inf: " + str(lim_inf))
        
        if (i > 0) & (i < (len(sorted_first_coordinates) - 1)):
            lim_sup = band_limits[i - 1][1]
            lim_inf = (sorted_first_coordinates[i + 1][1] - sorted_first_coordinates[i][1]) / 2 + sorted_first_coordinates[i][1]
            band_limits.append((lim_sup, lim_inf))
            #print("Lim sup: " + str(lim_sup))
            #print("Punto centrale: " + str(sorted_first_coordinates[i][1]))
            #print("Lim inf: " + str(lim_inf))
        
        if (i == (len(sorted_first_coordinates) - 1)):
            lim_sup = band_limits[i - 1][1]
            lim_inf = height
            band_limits.append((lim_sup, lim_inf))
            #print("Lim sup: " + str(lim_sup))
            #print("Punto centrale: " + str(sorted_first_coordinates[i][1]))
            #print("Lim inf: " + str(lim_inf))
    
    total_coordinates = []  # array di coordinate dei punti nelle fascia di controllo della singola immagine (inutile)
    number_of_points = []   # array dei numeri di punti trovati in ogni 
    for i, (sup, inf) in enumerate(band_limits):
        cv2.line(img_color,(0, round(sup)) , (width, round(sup)),(0, 255, 0) ,1)  # limite superiore
        cv2.line(img_color,(0, round(inf)) , (width, round(inf)),(0, 255, 0) ,1)  # limite inferiore
        
        band_coordinates = []  # salva le coordinate dei punti nella fascia di controllo
        for (x, y) in holes_coordinates:
            if (y < inf) and (y > sup):
                band_coordinates.append([x, y])

        band_coordinates_sorted = sorted(band_coordinates, key=lambda x: (x[0],x[0]))  # ordina le coordinate nella fascia secondo le x
        #print("Le cordinate nella " + str(i) + "esima riga sono: " + str(band_coordinates_sorted))
        points_in_band, filtred_coordinates = regression(band_coordinates_sorted)
        number_of_points = number_of_points + points_in_band       # aggiunge il numero di punti trovati su ogni riga
        total_coordinates.append(filtred_coordinates)
        #print("Le coordinate della fascia sono : " + str(filtred_coordinates))
        #save_file("array.txt", filtred_coordinates)
    
    #print("La lista dei punti trovati: " + str(number_of_points))
    #save_file("array.txt", "\n")
    return img_color, number_of_points, total_coordinates


# Funzione per il salvataggio (append) su file.
def save_file(file_name, elements):
	file = open(file_name, 'a+')
	file.write(str(elements) + '\n')
	file.close()

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

# # Dato un vettore 3-Dimensionale di coordinate cartesiane, estrarre la distanza dalle coordinate x contigue.
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



############################################
################# MAIN #####################
############################################

def recognition(): 
    global hole_cascade
    hole_cascade = cv2.CascadeClassifier('C:\\Users\\nk84\\OneDrive\\Documents\\Fabric-Meter\\hole classifier 2.0\\classifier\\hole_cascade_2.0.xml') 
    
    for folder in range(1,2):   # itera il processo su più di una cartella di immagini (qualora fossero presenti)
        input_folder = "C:\\Users\\nk84\\Desktop\\capture_test inclinazione\\green\\capture_test_" + str(folder) + "\\"
        output_folder = 'C:\\Users\\nk84\Desktop\\capture_test inclinazione\\filtrate_2\\'

        # Calcola il numero di immagini già numerate in ordine crescente nella cartella di destinazione
        path = glob.glob(output_folder + "*.jpg")  #cartella di destinazione
        cv2_img1 = []  # inizializza una lista vuota
        
        # carica le immagini in un array per la successiva elaborazione
        for img in path:
            n = cv2.imread(img)
            cv2_img1.append(n)
        
        #print("La cartella conteneva "+ str(len(cv2_img1)) + " immagini.")

        # Aggiunge le nuove immagini alla cartella numerate in ordine crescente partendo dall'ultimo numero precedente
        path1 = glob.glob(input_folder + "*.jpg") # cartella di partenza
        name =  len(cv2_img1)
        
        images = []
        for i in path1:   # itera sulla singola immagine e le salva in un vettore
            n = cv2.imread(i)
            name = name + 1
            images.append(n)
        
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
            #print("n fori: " + str(len(holes_coordinates)))
            total_coordinates.append(coordinates)
            cv2.imshow("try", image)
            cv2.waitKey(1)
            end = time.time()
            time_passed = end - start
            times.append(time_passed)
            # Progress bar. 
            # Questo pezzo di codice va inserito nel punto in cui si vuole aggiornare la progress bar.
            b = (i + 1) * 100 / len(images)  # valore da incrementare sulla barra ad ogni ciclo di immagine.
            progress['value'] = b 
            root.update_idletasks() 
            
    #median_detection = np.median(detecting) # fa la media di tutti i valori dei fori individuati (serve per capire l'effetto della variazione di                                                 sensibilità del thresholding)
    #print("Media dei fori individati: " + str(median_detection))
    #median_time = np.median(time_passed) # fa la media dei tempi di ciclo
    #print("Tempo medio per elaborazione: " + str(median_time))
    total_points.sort()
    print("Array delle coordinate: " + str(total_coordinates))
    #print("Il numero totale di fori per ogni riga: " + str(total_points))
    max_value, _ = frequency(total_points)
    print(max_value)
    _, _, min_distance = distance_x(total_coordinates, max_value)
    print(min_distance)

    cv2.destroyAllWindows()



############################################
################## GUI #####################
############################################

# creating tkinter window 
root = Tk() 

# Progress bar widget 
progress = Progressbar(root, orient = HORIZONTAL, 
			length = 200, mode = 'determinate') 

progress.pack(pady = 10) 

# This button will initialize 
# the progress bar 
Button(root, text = 'Start', command = main_with_bar).pack(pady = 10) 

# infinite loop 
mainloop() 