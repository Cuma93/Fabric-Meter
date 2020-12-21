from setting import *
from matplotlib import pyplot as plt

GPIO.output(bobina_distensione, GPIO.LOW)

cap = cv2.VideoCapture(0) # We turn the webcam on.
while True:
    ret,frame = cap.read()
    #cv2.imshow('preview',frame) # We display the outputs.
    height, width, _ = frame.shape
    canvas1 = cv2.line(frame,(round(width/2), 0),(round(width/2), height),(0,255,0),1)  # linea verticale
    canvas2 = cv2.line(canvas1,(0, round(height/2)),(width, round(height/2)),(0,255,0),1)   # linea orizzonatale
    blur1 = cv2.GaussianBlur(frame,(5,5),0)
    cv2.imshow('blur1',canvas2) # We display the outputs.
    blur2 = cv2.GaussianBlur(frame,(5,5),10)
    #cv2.imshow('blur2',blur2) # We display the outputs.
    #cv2.imshow('original',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): # If we type on the keyboard:
        #print("L'immagine è " + str(height) + "x" + str(width))  #stampa le dimensioni del frame
        break # We stop the loop.
cap.release() # We turn the webcam off.
cv2.destroyAllWindows() # We destroy all the windows inside which the images were displayed.a

GPIO.cleanup()