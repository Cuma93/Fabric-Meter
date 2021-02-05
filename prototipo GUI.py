# Programma personalizzato con una pagina e progress bar
import time
import tkinter as tk
from tkinter.constants import HORIZONTAL, SOLID
from tkinter.ttk import Progressbar
 
# setup
root = tk.Tk()
root.title("Menu system")
root.geometry("800x1500+1100+0")
 
# create frames
objects_frame = tk.Frame(root)
objects_frame.grid(row=0, column=0)
buttons_frame = tk.Frame(root)
buttons_frame.grid(row=1, column=0)
message_frame = tk.Frame(root)
message_frame.grid(row=2, column=0)

holes_number = tk.DoubleVar()
forza_tiraggio = tk.DoubleVar()
tk.Scale(objects_frame, label="NUMERO ASOLE", from_=0, to=200, bg="white", activebackground="green", troughcolor="white", width=50, length=300, relief=SOLID, tickinterval=50, orient=HORIZONTAL, variable=holes_number).grid(row=0, column=0)
tk.Scale(objects_frame, label="FORZA TENSIONAMENTO (kg)", from_=0, to=200, bg="white", activebackground="green", troughcolor="white", width=50, length=300, relief=SOLID, tickinterval=50, orient=HORIZONTAL, variable=forza_tiraggio).grid(row=1, column=0)

# clear screen function
def clear(object):
    slaves = object.grid_slaves()
    for x in slaves:
        x.destroy()

# different items on different menus
def setting():
    clear(buttons_frame)
    tk.Button(buttons_frame, text="START", command=start, padx=98).grid(row=0, column=0)
    print(holes_number.get())
    print(forza_tiraggio.get())

    # se la gpio è piena, svuotala
    # se è vuota, riempila 
    # salvare i parametri n boccole e forza di tiro
    # restituire True

def start():
    clear(objects_frame)
    clear(buttons_frame)
    tk.Label(message_frame, text="IN ESECUZIONE...").grid(row=0, column=0)
    progress_bar = Progressbar(objects_frame, orient="horizontal", mode="determinate", maximum=100, value=0)
    progress_bar.grid(row=0, column=1)

    # Procedere con il campionamento fino ad ottenere la dist minima di controllo tra i fori e numero di fori per riga.
    # Restituire un True dalla funzione campionamento
    # Se è True, far partire l'allineamento

    for i in range(0, 100, 1):
        progress_bar['value'] = i
        objects_frame.update_idletasks() 
        time.sleep(0.01)

    clear(message_frame)
    tk.Label(message_frame, text="MISURAZIONE TERMINATA" + "\n" + "SONO €10").grid(row=0, column=0)
    # inserire il campionamento e restituire un True

# Pulsanti persistenti
tk.Button(objects_frame, text="CONFERMA PARAMETRI", command=setting, padx=98).grid(row=2, column=0)
 
tk.mainloop()