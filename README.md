# Fabric-Meter
## Programma principale: main_4.py 
### Sequenza ciclo
Importazione librerie
Setting
1.  assegnazione pins;
2.	armamento quattro bobine distensione;
3.	reset motori sulle guide;
4.	reset del motore focus;

Campionamento
1.	Salvataggio di 30 immagini diverse lungo la corsa della videocamera;
2.	elaborazione immagini campionamento;
3.	Output: numero fori per riga, distanza minima statistica tra due fori contigui;

Armamento e assestamento della bobina fissa

Allineamento con conteggio
1.	Prende una porzione di frame a sinistra sulla mezzeria;
2.	Applica il filtraggio migliore; 
3.	Allinea sempre il secondo foro partendo da destra portandolo sulla mezzeria;
4.	Quando il secondo foro è allineato, la videocamera avanza di una quantità tale che il secondo foro del frame diventi il primo foro nel frame successivo; 
5.	Allinea fino alla fine della corsa;

Armamento e assestamento della bobina mobile

### Cosa mancava da implementare

1. Correzione degli errori video: punto doppio e punto mancante.
2. Miglioramento del detecting sulla regione di interesse.
3. Individuazione dell’ultimo frame per il posizionamento preciso in corrispondenza della bobina fissa.

