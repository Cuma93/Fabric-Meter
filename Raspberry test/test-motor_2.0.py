import RPi.GPIO as GPIO  #library for I/O
import time              #library for delays
import yaml
from StepperLib import *

def loop():
    while True:
        moveStep1(1,3,512)
        time.sleep(0.5)
        moveStep2(0,3,512)
        time.sleep(0.5)
        

def destroy():
    GPIO.cleanup()  #release GPIOs used chennels

if __name__ == '__main__':
    setup1()
    setup2()
    #setup3()
    #setup4()
    #setup5()
    #setup6()
    #setup7()
    print("Program is starting...")
    try:
        loop()
    except KeyboardInterrupt:
        destroy() 