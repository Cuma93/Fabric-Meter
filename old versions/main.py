from setting import *

def middleR(img, coordinates_x, coordinates_y, width, height):  # funzione che individua le coordinate del foro nella mezzeria con coordinata x maggiore e quello adiacente
    ### Identifichiamo il foro più a destra che sta in un intorno di y centrato nella mezzeria
    Y_max = int(height/2 - 50)
    Y_min = int(height/2 + 50)
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

    return x_circle, y_circle, x_circle_next, y_circle_next



def alignment(img, x_last, y_last, x_next, y_next): # prende in ingresso l'immagine, le coordinate dell'ultimo foro e di quello adiacente.
    # intervallo di tolleranza
    check_position = 2
    Y_max = int(y_last - 4)   
    Y_min = int(y_last + 4) 
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
        print("Cordinata x: " + str(x))
        print("Cordinata y: " + str(y))
        #roi = frame_color[y:y+h, x:x+w] # We get the region of interest in the image.
    
    return list(x_holes), list(y_holes), frame_color   # We return the image with the detector rectangles.


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


def filtered (frame_gray):
	averaging = cv2.blur(frame_gray, (20, 20))
	median = cv2.medianBlur(averaging, 25)
	_, threshold = cv2.threshold(median, 140, 255, cv2.THRESH_BINARY)  # per isolare i fori
		
	return threshold
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# FUNZIONE SALVATAGGIO E SCRITTURA SU FILE ESTERNO


	


#______________________________________________________________________________________
#
# AVVIO CICLO MACCHINA
#______________________________________________________________________________________


#stepR(3)
#stepR(2)

stepC(328, 2)
#save_position("position.txt", pos[2])
#stepC(position_value, 0)
#inizializza una lista vuota
#GPIO.output(bobina_fissa, GPIO.LOW)
#moveStep2(0,8,90)   # 90 x sfocato 100 per nitido


numbers = [] 
hole_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Fabric-Meter/hole classifier 2.0/classifier/hole_cascade_2.0.xml')



video_capture = cv2.VideoCapture(0)

while True:
	start = time.time()
	_, img = video_capture.read()
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#height, width = img_gray.shape[0:2]
	cv2.imshow("Try", img_gray)
	'''img_filtred = filtered(img_gray)
	X, Y, canvas = detect_hole(img_filtred)  # restituisce l'immagine, la lista delle coordinate x e la lista delle coordinate y
	print("Le coordinate X sono: " + str(X)) 
	x_last, y_last, x_next, y_next = middleR(canvas, X, Y, width, height)
	print("siamo arrivati qui 6")
	print("Dimensione frame:" + str(width) + "x" + str(height) + "pxl")
	print("Le coordinate del'ultimo foro sono: " + str((x_last, y_last)))
	print("Le coordinate del foro adiacente sono: " + str((x_next, y_next)))
	aligner = alignment(canvas, x_last, y_last, x_next, y_next)
	print("siamo arrivati qui 7")
	print("L'allineatore è: " + str(aligner))
	if aligner == -1:
		print("Muovi il motore 'allineamento' di un passo nella direzione corretta")
	if aligner == 1:
		print("Muovi il motore 'allineamento' di un passo nella direzione corretta")
	check_row, holes_in_row = detect_row(img_gray, 80, y_last, X, Y)
	if check_row == 1:
		print("Tutti i " + str(holes_in_row) + " fori sono nella fascia di allineamento.")
	else:
		print("Solo " + str(holes_in_row) + " fori sono nella fascia di allineamento")

	cv2.imshow("Sample", canvas)'''
	
	end = time.time()
	print("tempo " + str(end - start))
	if cv2.waitKey(1) & 0xFF == ord('q'): # If we type on the keyboard:
        #print("L'immagine è " + str(height) + "x" + str(width))  #stampa le dimensioni del frame
		break # We stop the loop.


video_capture.release() # We turn the webcam off.
cv2.destroyAllWindows() # We destroy all the windows inside which the images were displayed.


GPIO.cleanup()