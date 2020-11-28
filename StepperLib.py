import RPi.GPIO as GPIO  #library for Raspberry I/O
import time              #library for delays
import yaml
CCWStep = (0x01,0x02,0x04,0x08)
CWStep = (0x08,0x04,0x02,0x01)

with open('cfgMotorPins.yml') as cfg :    #importa il file di configurazione. Vedi cfgMotorPins.yml per la definizione dei pin motore.
    config = yaml.load(cfg, Loader=yaml.FullLoader)  #carica la configurazione

#motorPinsFocus = config['motorPinsFocus'] #assegna alla variabile motorPins1 la lista di valori
motorPins2 = config['motorPins2'] #assegna alla variabile motorPins2 la lista di valori
#motorPins3 = config['motorPins3'] #assegna alla variabile motorPins3 la lista di valori
#motorPins4 = config['motorPins4'] #assegna alla variabile motorPins4 la lista di valori
#motorPins5 = config['motorPins5'] #assegna alla variabile motorPins5 la lista di valori
#motorPins6 = config['motorPins6'] #assegna alla variabile motorPins6 la lista di valori
#motorPins7 = config['motorPins7'] #assegna alla variabile motorPins7 la lista di valori




#abilita i pin per il motore
#def setup1():   
    #print ('Program is starting...')
    #GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    #for pin in motorPinsFocus:
     #   GPIO.setup(pin,GPIO.OUT)
def setup2():   
    #print ('Program is starting...')
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    for pin in motorPins2:
        GPIO.setup(pin,GPIO.OUT)
#def setup3():   
    #print ('Program is starting...')
    #GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    #for pin in motorPins3:
        #GPIO.setup(pin,GPIO.OUT)
#def setup4():   
    #print ('Program is starting...')
    #GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    #for pin in motorPins4:
        #GPIO.setup(pin,GPIO.OUT)
#def setup5():   
    #print ('Program is starting...')
    #GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    #for pin in motorPins5:
        #GPIO.setup(pin,GPIO.OUT)
#def setup6():   
    #print ('Program is starting...')
    #GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    #for pin in motorPins6:
        #GPIO.setup(pin,GPIO.OUT)
#def setup7():   
    #print ('Program is starting...')
    #GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    #for pin in motorPins7:
        #GPIO.setup(pin,GPIO.OUT)


#alimentazione in sequenza delle bobine del motore. 
# def moveOnePeriodFocus(direction,ms):
#     for j in range(0,4,1):      #cycle for power supply order [range(numero start, numero stop, incremento)]
#         for i in range(0,4,1):  #assign to each pin, a total of 4 pins
#             if (direction == 1):#power supply order clockwise
#                 GPIO.output(motorPinsFocus[i],((CCWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
#             else :              #power supply order anticlockwise
#                 GPIO.output(motorPinsFocus[i],((CWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
#         if(ms<3):       #the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
#             ms = 3
#         time.sleep(ms*0.001)
        
        
def moveOnePeriod2(direction,ms):
    for j in range(0,4,1):      #cycle for power supply order [range(numero start, numero stop, incremento)]
        for i in range(0,4,1):  #assign to each pin, a total of 4 pins
            if (direction == 1):#power supply order clockwise
                GPIO.output(motorPins2[i],((CCWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
            else :              #power supply order anticlockwise
                GPIO.output(motorPins2[i],((CWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
        if(ms<3):       #the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
            ms = 3
        time.sleep(ms*0.001)
        

# def moveOnePeriod3(direction,ms):
#     for j in range(0,4,1):      #cycle for power supply order [range(numero start, numero stop, incremento)]
#         for i in range(0,4,1):  #assign to each pin, a total of 4 pins
#             if (direction == 1):#power supply order clockwise
#                 GPIO.output(motorPins3[i],((CCWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
#             else :              #power supply order anticlockwise
#                 GPIO.output(motorPins3[i],((CWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
#         if(ms<3):       #the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
#             ms = 3
#         time.sleep(ms*0.001)
        

# def moveOnePeriod4(direction,ms):
#     for j in range(0,4,1):      #cycle for power supply order [range(numero start, numero stop, incremento)]
#         for i in range(0,4,1):  #assign to each pin, a total of 4 pins
#             if (direction == 1):#power supply order clockwise
#                 GPIO.output(motorPins4[i],((CCWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
#             else :              #power supply order anticlockwise
#                 GPIO.output(motorPins4[i],((CWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
#         if(ms<3):       #the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
#             ms = 3
#         time.sleep(ms*0.001)
        

# def moveOnePeriod5(direction,ms):
#     for j in range(0,4,1):      #cycle for power supply order [range(numero start, numero stop, incremento)]
#         for i in range(0,4,1):  #assign to each pin, a total of 4 pins
#             if (direction == 1):#power supply order clockwise
#                 GPIO.output(motorPins5[i],((CCWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
#             else :              #power supply order anticlockwise
#                 GPIO.output(motorPins5[i],((CWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
#         if(ms<3):       #the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
#             ms = 3
#         time.sleep(ms*0.001)

# def moveOnePeriod6(direction,ms):
#     for j in range(0,4,1):      #cycle for power supply order [range(numero start, numero stop, incremento)]
#         for i in range(0,4,1):  #assign to each pin, a total of 4 pins
#             if (direction == 1):#power supply order clockwise
#                 GPIO.output(motorPins6[i],((CCWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
#             else :              #power supply order anticlockwise
#                 GPIO.output(motorPins6[i],((CWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
#         if(ms<3):       #the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
#             ms = 3
#         time.sleep(ms*0.001)


# def moveOnePeriod7(direction,ms):
#     for j in range(0,4,1):      #cycle for power supply order [range(numero start, numero stop, incremento)]
#         for i in range(0,4,1):  #assign to each pin, a total of 4 pins
#             if (direction == 1):#power supply order clockwise
#                 GPIO.output(motorPins7[i],((CCWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
#             else :              #power supply order anticlockwise
#                 GPIO.output(motorPins7[i],((CWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
#         if(ms<3):       #the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
#             ms = 3
#         time.sleep(ms*0.001)



# #azionamento del motore
# def moveStepFocus(direction, ms, steps):
#     for i in range(steps):
#         moveOnePeriodFocus(direction, ms)
        
def moveStep2(direction, ms, steps):
    for i in range(steps):
        moveOnePeriod2(direction, ms)

# def moveStep3(direction, ms, steps):
#     for i in range(steps):
#         moveOnePeriod3(direction, ms)

# def moveStep4(direction, ms, steps):
#     for i in range(steps):
#         moveOnePeriod4(direction, ms)

# def moveStep5(direction, ms, steps):
#     for i in range(steps):
#         moveOnePeriod5(direction, ms)

# def moveStep6(direction, ms, steps):
#     for i in range(steps):
#         moveOnePeriod6(direction, ms)

# def moveStep7(direction, ms, steps):
#     for i in range(steps):
#         moveOnePeriod7(direction, ms)



def motorStop():
    for i in range(0,4,1):
        GPIO.output(motorPins2[i],GPIO.LOW)


def destroy():
    GPIO.cleanup()  #release GPIOs used chennels
    