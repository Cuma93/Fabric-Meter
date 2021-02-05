################################################################################################
####################################  IMPORTAZIONE LIBRERIE  ###################################
################################################################################################

# Librerie generiche
import os #..................................................navigazione cartelle
import yaml  #...............................................caricamento files di configurazione
import RPi.GPIO as GPIO  #...................................abilitazione GPIO Raspberry
from StepperLib import * #...................................attuazione del mini motore step 
import cv2  #............................................... grafica e computer vision
import numpy as np  #........................................operazioni su array
import time #................................................delays

# Librerie GUI
import tkinter as tk #.......................................GUI (principale)
from tkinter.constants import HORIZONTAL, SOLID #............estensione per widget GUI
from tkinter.ttk import Progressbar #........................barre avanzamento
from tkinter import font as tkFont #.........................fonts per GUI

################################################################################################
#########################################  FUNZIONI  ###########################################
################################################################################################

# Funzione per la pulizia del frame GUI
def clear(object):
    slaves = object.grid_slaves()
    for x in slaves:
        x.destroy()

################################################################################################
#####################################  FUNZIONI FISICHE  #######################################
################################################################################################

# Esegue le seguenti operazioni:
# - salva in memoria globale i parametri n boccole e forza di tiro
# - controlla la GPIO. Se è piena la svuota. Se è vuota la carica
# - restituisce un True
def setting():
	global set_holes, set_force
	set_holes = holes_number.get()
	set_force = forza_tiraggio.get()
	clear(buttons_frame)
	tk.Button(buttons_frame, text="START", command=start, padx=98).grid(row=0, column=0)
	print(set_holes, set_force)


################################################################################################
##########################################  MAIN  ##############################################
################################################################################################

# Esegue le seguenti operazioni:
# - esegue caratterizzazione e restituisce: max_points, min_dist e True
# - esegue allineamento e restituisce: True
# - esegue conteggio e aggancia
# - esegue tiraggio restituisce: parametro
# - sgancio e rimozione
def start():
    clear(objects_frame)
    clear(buttons_frame)
    tk.Label(message_frame, text="IN ESECUZIONE...").grid(row=0, column=0)  # messaggio
    progress_bar = Progressbar(objects_frame, orient="horizontal", mode="determinate", maximum=100, value=0)
    progress_bar.grid(row=0, column=1)
    objects_frame.update()
    progress_bar['value'] = 0
    objects_frame.update()

    for i in range(0, 100, 1):
        progress_bar['value'] = i
        objects_frame.update_idletasks() 
        time.sleep(0.01)

    clear(message_frame)
    tk.Label(message_frame, text="MISURAZIONE TERMINATA" + "\n" + "SONO €10").grid(row=0, column=0) # messaggio

################################################################################################
###########################################  GUI  ##############################################
################################################################################################

# Setup dell'interfaccia
root = tk.Tk()  
root.title("Menu system")
root.geometry("800x1500+1100+0")
holes_number = tk.IntVar()
forza_tiraggio = tk.DoubleVar()
 
# Creazione dei frames (caselle apposte sul root)
objects_frame = tk.Frame(root)
objects_frame.grid(row=0, column=0)
buttons_frame = tk.Frame(root)
buttons_frame.grid(row=1, column=0)
message_frame = tk.Frame(root)
message_frame.grid(row=2, column=0)

# Pulsanti nella schermata iniziale
tk.Scale(objects_frame, label="NUMERO ASOLE", from_=0, to=200, bg="white", activebackground="green", troughcolor="white", width=50, length=300, relief=SOLID, tickinterval=50, orient=HORIZONTAL, variable=holes_number).grid(row=0, column=0) # slider
tk.Scale(objects_frame, label="FORZA TENSIONAMENTO (kg)", from_=0, to=200, bg="white", activebackground="green", troughcolor="white", width=50, length=300, relief=SOLID, tickinterval=50, orient=HORIZONTAL, variable=forza_tiraggio).grid(row=1, column=0) # slider
tk.Button(objects_frame, text="CONFERMA PARAMETRI", command=setting, padx=98).grid(row=2, column=0) # pulsante conferma
 
tk.mainloop()
