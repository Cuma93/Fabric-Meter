import os
import time
import RPi.GPIO as GPIO
import yaml
from StepperLib import *

GPIO.setmode(GPIO.BOARD)   # Assegna ai pin la numerazione convenzionale. Usare "GPIO.setmode(GPIO.BCM)" per la numerazione hardware.

# Assegnazione pin motori
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
proxy_distensori = 22
proxy_focus = 13
proxy_videocamera = 15
laser = 16


# Setup GPIO input/output
setup2()
GPIO.setup(dir_distensori, GPIO.OUT, initial=0)
GPIO.setup(pull_distensori, GPIO.OUT, initial=0)
GPIO.setup(dir_tensionatore, GPIO.OUT, initial=0)
GPIO.setup(pull_tensionatore, GPIO.OUT, initial=0)
GPIO.setup(dir_allineamento, GPIO.OUT, initial=0)
GPIO.setup(pull_allineamento, GPIO.OUT, initial=0)
GPIO.setup(dir_videocamera, GPIO.OUT, initial=0)
GPIO.setup(pull_videocamera, GPIO.OUT, initial=0)


GPIO.setup(bobina_mobile, GPIO.OUT)
GPIO.setup(bobina_fissa, GPIO.OUT)
GPIO.setup(bobina_distensione, GPIO.OUT)

GPIO.setup(proxy_tensionatore, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(proxy_allineamento, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(proxy_distensori, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(proxy_focus, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(proxy_videocamera, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(laser, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("La GPIO è stata liberata")

GPIO.cleanup()