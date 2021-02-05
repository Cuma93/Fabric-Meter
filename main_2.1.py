import os
import time
import RPi.GPIO as GPIO
import yaml
from StepperLib import *
import cv2
import numpy as np
from tkinter import *
from tkinter import font as tkFont


# FUNZIONE PER LA LIBERAZIONE DELLA GPIO

def clean_gpio():
	GPIO.cleanup()


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
	# Posizione 0 ---> 4 motori distensione
	# Posizione 1 ---> motore tensionatore
	# Posizione 2 ---> motore allineamento
	# Posizione 3 ---> motore videocamera
	
	global dirP, stepperP, microP
	
	dirP = (31, 36, 40, 35)
	stepperP = (29, 37, 38, 33)
	microP = (10000, 50, 1000, 100)  # Tempo in microsecondi tra due step
	

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
	
	stepR(0)

# -------------------------------------------------------------------
# FUNZIONE SCRITTURA E SALVATAGGIO POSIZIONE SU FILE ESTERNO
# -------------------------------------------------------------------

def read_position (file_name):
	file = open(file_name, 'r')
	pos = file.read()
	position = pos
	file.close()
	
	return int(position)


def save_position(file_name, position):
	file = open(file_name, 'w+')
	file.write(str(position))
	file.close()


# ------------------------------------
# Funzione di controllo motori step
# ------------------------------------


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




# ----------------------------------
# FUNZIONI VISIONE
# ----------------------------------

def middleR(img, coordinates_x, coordinates_y, width, height):  # funzione che individua le coordinate del foro nella mezzeria con coordinata x maggiore e quello adiacente
    ### Identifichiamo il foro più a destra che sta in un intorno di y centrato nella mezzeria
    Y_max = int(height/2 - 20)
    Y_min = int(height/2 + 20)
    selected_y = []
    selected_x = []
    #print("La lista selected_x vale: " + str(selected_x))
    ## disegnamo il range +/- 50 pxl per verifica
    cv2.line(img,(0, Y_max) , (width, Y_max),(255, 0, 0) ,1)  # linea superiore
    cv2.line(img,(0, int(height/2)) , (width, int(height/2)),(255, 255, 0) ,1)  # linea di mezzeria
    cv2.line(img,(0, Y_min) , (width, Y_min),(255, 0, 0) ,1)  # linea inferiore
    for i, y in enumerate(coordinates_y):    
        if (y < Y_min and y > Y_max):   # cerca le y nella fascia centrale +/- 50 pixel 
            selected_y.append(y)   
            selected_x.append(coordinates_x[i])
    ## qui abbiamo ottenuto la lista delle y che stanno nella fascia e la lista delle x corrispondenti
    x_max = np.argmin(selected_x)  # restituisce l'indice dell'argomento massimo
    #print("selected x: " + str(selected_x))
    #print("x max: " + str(x_max))
    x_circle = selected_x[x_max] 
    y_circle = selected_y[x_max] 
    cv2.circle(img,(int(x_circle), int(y_circle)), 5, (0, 255, 0), 2)

    ### Identifichiamo tutti i fori che stanno in un intorno ridotto e centrato nella y del foro di controllo trovano precedentemente
    Y_range_max = int(y_circle - 35)
    Y_range_min = int(y_circle + 35)
    range_selected_y = []  # lista delle cordinate y interne al range 
    range_selected_x = []  # lista delle cordinate x corrispondenti alle y interne al range
    ## disegnamo il range +/- 50 pxl per verifica
    cv2.line(img,(0, Y_range_max) , (width, Y_range_max),(255, 0, 255) ,1)  # linea superiore
    cv2.line(img,(0, int(y_circle)) , (width, int(y_circle)),(255, 50, 255) ,1)  # linea di mezzeria
    cv2.line(img,(0, Y_range_min) , (width, Y_range_min),(255, 0, 255) ,1)  # linea inferiore
    for i, y in enumerate(coordinates_y):    
        if (y < Y_range_min and y > Y_range_max):   # cerca le y nella fascia centrale +/- 50 pixel 
            range_selected_y.append(y)   
            range_selected_x.append(coordinates_x[i])
    ## qui abbiamo ottenuto la lista delle y che stanno nella fascia e la lista delle x corrispondenti
    x_max_range = np.argmin(range_selected_x)  # restituisce l'indice dell'argomento massimo
    #print("selected x: " + str(range_selected_x))
    #print("x max range: " + str(x_max_range))
    y_max_range = range_selected_y[x_max_range]
    x_circle_range = range_selected_x[x_max_range]
    y_circle_range = range_selected_y[x_max_range] 
    #cv2.circle(img,(int(x_circle_range), int(y_circle_range)), 5, (0, 0, 0), 2)

    ### identifichiamo il foro adiacente a quello più a dx
    short_selected_x = range_selected_x.copy()  # creiamo una copia della lista
    short_selected_x.remove(x_circle_range)     # eliminiamo la coordinata x maggiore, cioè quella del foro più esterno
    short_selected_y = range_selected_y.copy()  # creiamo una copia della lista
    short_selected_y.remove(y_circle_range)     # eliminiamo la coordinata y corrispondente alla x maggiore, cioè quella del foro più esterno
    x_next = np.argmin(short_selected_x)  # restituisce l'indice dell'argomento massimo
    #print("range selected x: " + str(range_selected_x))
    #print("short selected x: " + str(short_selected_x))
    #print("range selected y: " + str(range_selected_y))
    #print("short selected y: " + str(short_selected_y))
    #print("x next: " + str(x_next))
    y_next = short_selected_y[x_next]  # cerchiamo la coordinata y corrispondente a x_next
    x_circle_next = short_selected_x[x_next]
    y_circle_next = short_selected_y[x_next] 
    cv2.circle(img,(int(x_circle_next), int(y_circle_next)), 5, (0, 100, 100), 2)
    
    
    '''second_short_selected_x = short_selected_x.copy()  # creiamo una copia della lista
    second_short_selected_x.remove(x_circle_next)     # eliminiamo la coordinata x maggiore, cioè quella delsecondo foro più esterno
    second_short_selected_y = short_selected_y.copy()  # creiamo una copia della lista
    second_short_selected_y.remove(y_circle_next)     # eliminiamo la coordinata y corrispondente alla x maggiore, cioè quella del secondo foro più esterno
    y_third = second_short_selected_y[x_third]  # cerchiamo la coordinata y corrispondente a x_next
    x_circle_third = second_short_selected_x[x_third]
    y_circle_third = second_short_selected_y[x_third] 
    cv2.circle(img,(int(x_circle_third), int(y_circle_third)), 5, (0, 100, 100), 2)'''

    return x_circle, y_circle, x_circle_next, y_circle_next



def alignment(img, x_last, y_last, x_next, y_next): # prende in ingresso l'immagine, le coordinate dell'ultimo foro e di quello adiacente.
	global alignment_commuter
    # intervallo di tolleranza
	check_position = 2
	if (alignment_commuter == True): # setta il range di controllo solo al primo richiamo della funzione (quindi al primo frame). 
		global Y_max, Y_min
		Y_max = int(y_last - 10)   
		Y_min = int(y_last + 10)
		alignment_commuter = False
	cv2.line(img,(0, Y_max) , (width, Y_max),(0, 255, 0) ,1)  # linea superiore
	cv2.line(img,(0, Y_min) , (width, Y_min),(0, 255, 0) ,1)  # linea inferiore
	if (y_next < Y_max):
		check_position = 1
	if (y_next > Y_min):
		check_position = -1
	if (y_next > Y_max and y_next < Y_min):
		check_position = 0
    
	return check_position



def detect_hole(frame_gray):  # Funzione che identifica i centri dei fori, li numera !!! variare il threshold da 100 (maglia fitta) a 150 (maglia più lasca)
    holes = hole_cascade.detectMultiScale(frame_gray, 1.1, 22) 
    frame_color = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2BGR)
    print (len(holes))  # Stampa il numero di fori identificati
    #print(holes)
    marker = 1
    x_holes = [] # lista delle cordinate X dei centri dei fori
    y_holes = [] # lista delle cordinate Y dei centri dei fori
    
    for (x, y, w, h) in holes:
        cv2.circle(frame_color,(int(x+w/2), int(y+h/2)), 2, (0, 0, 255), 2)  # disegna il centro dei fori
        # Numera i fori
        cv2.putText(frame_color, str(marker), (int(x+w/2), int(y+h/2)), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        marker = marker + 1          
        X = x+w/2   # coordinata x del centro del detecting
        Y = y+h/2   # coordinata y del centro del detecting
        x_holes.append(X)
        y_holes.append(Y)
        #print("Cordinata x: " + str(x))
        #print("Cordinata y: " + str(y))
    
    return len(holes), list(x_holes), list(y_holes), frame_color   # We return the image with the detector rectangles.


def detect_row (frame_gray, range, y_center, coordinates_x, coordinates_y): # funzione che controlla quanti fori sono presenti nella fascia di controllo
    holes = hole_cascade.detectMultiScale(frame_gray, 1.1, 22)
    frame_color = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2BGR)
    Y_max = int(y_center - range/2)
    Y_min = int(y_center + range/2)
    selected_y = []
    selected_x = []
    for i, y in enumerate(coordinates_y):    
        if (y < Y_min and y > Y_max):   # cerca le y nella fascia centrale +/- 50 pixel 
            selected_y.append(y)   
            selected_x.append(coordinates_x[i])
    if (len(selected_y) >= 5):
            check_value = 1 
    else:
        check_value = 0

    return check_value, len(selected_y)


def filtered (frame_gray, threshold_value):
	averaging = cv2.blur(frame_gray, (20, 20))
	median = cv2.medianBlur(averaging, 25)
	_, threshold = cv2.threshold(median, threshold_value, 255, cv2.THRESH_BINARY)  # per isolare i fori
		
	return threshold
# --------------------------------------------------------------------------------------------------------------------------------------------------------------


#______________________________________________________________________________________
#
# AVVIO CICLO MACCHINA
#______________________________________________________________________________________
trigger = False
Setting = False
global alignment_commuter
alignment_commuter = True

setting()
GPIO.cleanup()

#def stop_main():
#	break


def start_main():
	global hole_cascade
	global height, width
	
	
	
	# Reset motori
	stepR(0)
	stepR(3)
	stepR(2)
	stepR(4)
	stepR(6)
	
	# Azionamento motori
	#moveStep2(0,8,90)   # 90 x sfocato 100 per nitido
	#stepC(0, 2)
	#stepC(150, 0)
	#stepC(500, 3)
	#print("pos 3 vale: " + str(pos[3]))
	#save_position("position.txt", pos[2])
	#stepC(position_value, 0)
	#inizializza una lista vuota
	#GPIO.output(bobina_fissa, GPIO.LOW)'''
	
	# Caricamento classificatore
	hole_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Fabric-Meter/hole classifier 2.0/classifier/hole_cascade_2.0.xml')
	
	# Attivazione videocamera
	video_capture = cv2.VideoCapture(0)
	
	video_position_counter = pos[3]
	aligner_position_counter = pos[2]

	# Ciclo visione
	while (GPIO.input(proxy_videocamera) == True):
		ret, img = video_capture.read()
		if ret == True:
			img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			cv2.imshow("Natural Gray", img_gray)
			height, width = img_gray.shape[0:2]
			print("height, width: " + str(height) + " " + str(width))
			threshold_value = 140
			while True:
				img_filtred = filtered(img_gray, threshold_value)
				holes_number, X, Y, canvas = detect_hole(img_filtred)  # restituisce l'immagine, la lista delle coordinate x e la lista delle coordinate y
				if (holes_number <= 29 and threshold_value >= 120):
					threshold_value = threshold_value - 10
				else:
					break
			#print("Le coordinate X sono: " + str(X)) 
			x_last, y_last, x_next, y_next = middleR(canvas, X, Y, width, height)
			#print("siamo arrivati qui 6")
			#print("Dimensione frame:" + str(width) + "x" + str(height) + "pxl")
			#print("Le coordinate del'ultimo foro sono: " + str((x_last, y_last)))
			#print("Le coordinate del foro adiacente sono: " + str((x_next, y_next)))
			aligner = alignment(canvas, x_last, y_last, x_next, y_next)
			print(aligner)
			#print("siamo arrivati qui 7")
			#print("L'allineatore è: " + str(aligner))
			cv2.imshow("Sample", canvas)
			
			if aligner == -1:
				aligner_position_counter = aligner_position_counter - 3
				stepC(aligner_position_counter, 2)
				cv2.imshow("Sample", canvas)
				cv2.waitKey(1)
				
				
			if aligner == 1:
				aligner_position_counter = aligner_position_counter + 3
				stepC(aligner_position_counter, 2)
				cv2.imshow("Sample", canvas)
				cv2.waitKey(1)
				
			
			if aligner == 0:
				cv2.imshow("Sample", canvas)
				cv2.waitKey(1)
				video_position_counter = video_position_counter - 100
				print(video_position_counter)
				stepC(video_position_counter, 3)
				
			
			if aligner == 2:
				cv2.imshow("Sample", canvas)
				cv2.waitKey(1)
				print("ERROR")
			
			
		
		
			'''check_row, holes_in_row = detect_row(img_gray, 80, y_last, X, Y)
			if check_row == 1:
				print("Tutti i " + str(holes_in_row) + " fori sono nella fascia di allineamento.")
			else:
				print("Solo " + str(holes_in_row) + " fori sono nella fascia di allineamento")'''
			
			
		
			  
			if cv2.waitKey(1) & 0xFF == ord('q'): # If we type on the keyboard:
				#print("L'immagine è " + str(height) + "x" + str(width))  #stampa le dimensioni del frame
				break # We stop the loop.


	video_capture.release() # We turn the webcam off.
	cv2.destroyAllWindows() # We destroy all the windows inside which the images were displayed.


# --------------------------------------------------------------------------------------------------------------------------------
# GUI
# -------------------------------------------------------------------------------------------------------------------------------- 

start_loop = True
root = Tk()
root.title("Program")
root.geometry("800x1500+1100+0")
helv36 = tkFont.Font(family='Helvetica', size=70, weight=tkFont.BOLD)
setting_button = Button(root, text="Setting", font=helv36, padx=204, pady=50, command=setting, fg="white", bg="blue")
setting_button.pack()
start_button = Button(root, text="Start", font=helv36, padx=256, pady=50, command=start_main, fg="white", bg="green")
start_button.pack()
clean_button = Button(root, text="Clean GPIO", font=helv36, padx=105, pady=50, command=clean_gpio, fg="black", bg="white")
clean_button.pack()
close_button = Button(root, text="Close", font=helv36, padx=235, pady=50, command=root.destroy, fg="white", bg="red")
close_button.pack()

root.mainloop()

GPIO.cleanup()
