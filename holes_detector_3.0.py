from setting import *

#inizializza una lista vuota
numbers = []

hole_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Fabric-Meter/hole classifier 2.0/classifier/hole_cascade_2.0.xml') # caricamento del classificatore per fori ad immafine filtrata
edge_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Fabric-Meter/edge classifier/classifier/cascade.xml') # caricamento del classificatore per i bordi


def detect(gray, frame):  #open cv prende in ingresso solo l'immagine in bianco e nero e non un video
    holes = hole_cascade.detectMultiScale(gray, 1.3, 5)
   
    
    for (x,y,w,h) in holes:
        holesCy=int(y+h/2)  #prende come riferimento la metà dell'altezza in Y del quadrato detection
        lineCy=height-300   #identifica una linea non visibile ad altezza height-300. 
        
        if(holesCy)<=lineCy+6 and (holesCy)>=lineCy-6:  #se la metà dell'altezza del quadrato detection si trova in un intorno (della linea identificata ) compreso tra +6 e -6
            numbers.append(1)                           #somma +1 al contatore
        
        
        
        cv2.line(frame,(500, 0),(500, height),(0,0,255),2)  #traccia la linea per il contatore. Le parentesi sono le cordinate. Il centro è nell angolo alto a sx incremento è basso dx.  
        #cv2.putText(frame, str(len(numbers)),(300, 30), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 255, 0), 2)
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
    
GPIO.output(bobina_distensione, GPIO.LOW)
video_capture = cv2.VideoCapture(0) # We turn the webcam on.
            
while True: # We repeat infinitely (until break):
    _, frame = video_capture.read() # We get the last frame.
    height, width = frame.shape[0:2]   
    
    cv2.line(frame,(500, 0),(500, height),(0,0,255),2)  #traccia la linea verticale per il contatore. Le parentesi sono le cordinate. Il centro è nell angolo alto a sx incremento è basso dx.  
    cv2.putText(frame, "HOLES COUNTER: ", (15,30), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    cv2.circle(frame,(int(width/2), int(height/2)), 10, (0,255,0), 2)
    
    # applicazione filtri
    median_1 = cv2.medianBlur(frame, 9)
    median_2 = cv2.medianBlur(median_1, 9)
    median_3 = cv2.medianBlur(median_2, 9)
    unsharp_4 = unsharp_mask(median_3, 13)
    # cambio di colore pixel
    image = unsharp_4.copy()
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV) 
    grey_lo=np.array([50,50,50])
    grey_hi=np.array([254,254,254])
    mask=cv2.inRange(hsv,grey_lo,grey_hi)
    image[mask>0]=(255,255,255)
    # applicazione filtri singoli
    bilateral_6 = cv2.bilateralFilter(image, 9, 350, 350)
    median_7 = cv2.medianBlur(bilateral_6, 9)
    unsharp_8 = unsharp_mask(median_7, 2)
    
    gray = cv2.cvtColor(unsharp_8, cv2.COLOR_BGR2GRAY) # We do some colour transformations.
    canvas = detect(gray, unsharp_8) # We get the output of our detect function.
 
    cv2.imshow('Filter', canvas) # We display the outputs.
    cv2.imshow('Original', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): # If we type on the keyboard:
        #print("L'immagine è " + str(height) + "x" + str(width))  #stampa le dimensioni del frame
        break # We stop the loop.
    


video_capture.release() # We turn the webcam off.
cv2.destroyAllWindows() # We destroy all the windows inside which the images were displayed.a

