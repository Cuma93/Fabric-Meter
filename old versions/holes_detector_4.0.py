from setting import *



#______________________________________________________________________________________
#
# AVVIO CICLO MACCHINA
#______________________________________________________________________________________



#inizializza una lista vuota
numbers = []

hole_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Fabric-Meter/hole classifier 2.0/classifier/hole_cascade_2.0.xml') # caricamento del classificatore per fori ad immafine filtrata
edge_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Fabric-Meter/edge classifier/classifier/cascade.xml') # caricamento del classificatore per i bordi


def detect(gray, frame):  #open cv prende in ingresso solo l'immagine in bianco e nero e non un video  !!!!! Sistemare questione fori
    
    holes = hole_cascade.detectMultiScale(gray, 1.3, 5)
    print (len(holes))
    marker = 1
    
    for (x,y,w,h) in holes:
        holesCy=int(y+h/2)  #prende come riferimento la metà dell'altezza in Y del quadrato detection
        lineCy=height-300   #identifica una linea non visibile ad altezza height-300. 
        
        if(holesCy)<=lineCy+6 and (holesCy)>=lineCy-6:  #se la metà dell'altezza del quadrato detection si trova in un intorno (della linea identificata ) compreso tra +6 e -6
            numbers.append(1)                           #somma +1 al contatore
        
        cv2.line(frame,(500, 0),(500, height),(0, 0, 255) ,2)  #traccia la linea per il contatore. Le parentesi sono le cordinate. Il centro è nell angolo alto a sx incremento è basso dx.  
        #cv2.putText(frame, str(len(numbers)),(300, 30), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        #cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 255, 0), 2)
        cv2.circle(frame,(int(x+w/2), int(y+h/2)), 2, (0, 0, 255), 2)  # disegna il centro dei fori
        cv2.putText(frame, str(marker), (int(x+w/2),int(y+h/2)), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        marker = marker + 1          
        print("Cordinata x: " + str(x+w/2))
        print("Cordinata y: " + str(y+h/2))
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


#stepR(0)
#GPIO.output(bobina_distensione, GPIO.LOW)

'''time.sleep(15)
moveStep2(0,8,90)   # 90 x sfocato 100 per nitido
'''

video_capture = cv2.VideoCapture(0) # We turn the webcam on.
#time.sleep(10)
#stepC(150, 0)


while True: # We repeat infinitely (until break):
    ret, frame = video_capture.read() # We get the last frame.
    if ret == True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = frame.shape[0:2]    
       
        # applicazione filtri
        averaging = cv2.blur(gray, (20, 20))
        averaging2 = cv2.blur(gray, (50, 20))
        median = cv2.medianBlur(averaging, 25)
        median2 = cv2.medianBlur(averaging2, 25)
        ret,threshold_strong = cv2.threshold(median2, 30, 255, cv2.THRESH_BINARY)  # per unire i fori
        ret,threshold_light = cv2.threshold(median, 100, 255, cv2.THRESH_BINARY)  # per isolare i fori
        
        # We do some colour transformations.
        grey_strong = detect(threshold_strong, threshold_strong) 
        grey_light = detect(threshold_light, threshold_light)
        color_strong = cv2.cvtColor(grey_strong, cv2.COLOR_GRAY2BGR)
        color_light = cv2.cvtColor(grey_light, cv2.COLOR_GRAY2BGR)
        
        # Elementi sull'immagine fori uniti
        cv2.line(color_strong,(500, 0),(500, height),(0,0,255),2)  #traccia la linea verticale per il contatore. Le parentesi sono le cordinate. Il centro è nell angolo alto a sx incremento è basso dx.  
        cv2.putText(color_strong, "HOLES COUNTER: ", (15,30), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        cv2.circle(color_strong,(int(width/2), int(height/2)), 10, (0,255,0), 2)
     
        # Elementi sull'immagine fori uniti
        
        
        # Visualizzazione a monitor
        cv2.imshow('Strong', color_strong) # We display the outputs.
        cv2.imshow('Light', color_light)
        cv2.imshow('Original', frame)
        
        # Interruzione ciclo
    if cv2.waitKey(1) & 0xFF == ord('q'): # If we type on the keyboard:
        #print("L'immagine è " + str(height) + "x" + str(width))  #stampa le dimensioni del frame
        break # We stop the loop.
    


video_capture.release() # We turn the webcam off.
cv2.destroyAllWindows() # We destroy all the windows inside which the images were displayed.

#GPIO.cleanup()