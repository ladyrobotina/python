from cv2 import cv2
# modulo de python
import numpy as np

valorGauss=1 #variable crear el modelado de imagenes
valorKernel=7 #hay que usar valores impares
#variable para cargar la imagen
original=cv2.imread('monedassoles.jpg')
#pasar a escalas grises
gris=cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
#es un suavizado para desenfoque para eliminar ruidos
gauss=cv2.GaussianBlur(gris, (valorGauss,valorGauss), 0) #para el modelado gausiano se necesita una matriz
canny=cv2.Canny(gauss, 60,100)
#contornos de afuera, se trabaja con matrices
kernel=np.ones((valorKernel,valorKernel),np.uint8)
cierre=cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)

#devuelven dos valores contornos y jerarquía
contornos, jerarquía=cv2.findContours(cierre.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print("monedas encontradas: {}".format(len(contornos)))

#dibuja el contorno de linea 19
cv2.drawContours(original, contornos, -1, (0,0,255),2)

#Mostrar resultados
#cv2.imshow("Grises",gris)
#cv2.imshow("gauss",gauss)
#cv2.imshow("canny",canny)
#cv2.imshow("cierre",cierre)

#mostrar las imagenes
cv2.imshow("Resultado", original)
#para que no se cierre la imagen y quede hasta cerrar
cv2.waitKey(0)