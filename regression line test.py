import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

a = [[5, 10], [1, 9], [2, 8], [3, 8], [9, 11], [0, 5], [3, 7], [255, 255]]
c = np.array(a)
coord = c[np.lexsort(np.transpose(c)[::-1])]
x = np.transpose(coord)[0] # divide il vettore di coordinate per ottenere il vettore delle x
y = np.transpose(coord)[1] # divide il vettore di coordinate per ottenere il vettore delle y

## Filtraggio dei punti outliers che non appartengono alla linea serie di boccole allineate
# Creazione della fascia di filtraggio
lim_inf = np.median(y) - 2 * np.std(y)  # il parametro può variare (1 filtro stretto - 3 filtro largo)
lim_sup = np.median(y) + 2 * np.std(y) 

filtred = []
for x, y in coord:
    
    if (y > lim_inf) and (y < lim_sup): 
        filtred.append([x, y])

filtred_x = np.transpose(filtred)[0] # divide il vettore di coordinate per ottenere il vettore delle x
filtred_y = np.transpose(filtred)[1] # divide il vettore di coordinate per ottenere il vettore delle y
res = stats.linregress(filtred_x, filtred_y)

# N.B.: y = m*x + q    (m = slope, q = intercept)
p1 = (0, round(res.slope*0 + res.intercept))
p2 = (800, round(res.slope*800 + res.intercept))
#cv2.line(img,(p1[0], p1[1]) , (p2[0], p2[1]),(0, 255, 0) ,3)  # linea regressione