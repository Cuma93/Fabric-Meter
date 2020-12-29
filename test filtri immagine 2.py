from setting import *
from matplotlib import pyplot as plt

#GPIO.output(bobina_distensione, GPIO.LOW)

hole_cascade = cv2.CascadeClassifier('/home/pi/Desktop/Fabric-Meter/hole classifier 2.0/classifier/hole_cascade_2.0.xml') # caricamento del classificatore per fori ad immafine filtrata

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

def detect(gray, frame):  #open cv prende in ingresso solo l'immagine in bianco e nero e non un video
    holes = hole_cascade.detectMultiScale(gray, 1.3, 5)
    print (len(holes))
   
    
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
                
                
image = cv2.imread("/home/pi/Desktop/campionamento/capture_test_1/capture_test_2.jpg")

height, width = image.shape[0:2]   
    
cv2.line(image,(500, 0),(500, height),(0,0,255),2)  #traccia la linea verticale per il contatore. Le parentesi sono le cordinate. Il centro è nell angolo alto a sx incremento è basso dx.  
cv2.putText(image, "HOLES COUNTER: ", (15,30), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
cv2.circle(image,(int(width/2), int(height/2)), 10, (0,255,0), 2)
    
# applicazione filtri
median_3 = cv2.medianBlur(image, 27)
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
 
#cv2.imshow('Filter', canvas) # We display the outputs.
cv2.imshow('Original', unsharp_8)

cv2.waitKey(5000)
cv2.destroyAllWindows()

GPIO.cleanup()