from cv2 import cv2
import numpy as np #matrices
def ordenarpuntos(puntos): # def es para definir funciones, esta funcion pide puntos
    #unir y enlazar matrices todos los puntos se unen y se convierten en un solo objeto
    # al final el tolist lo convierte en una lista
    n_puntos=np.concatenate([puntos[0],puntos[1],puntos[2],puntos[3]]).tolist()
    #coordenadas x e y 
    # ordenamos con el sorted
    # funcion key=lambda asume el tipo de orden que le damos a la matriz
    # n_puntos: n_puntos[1] es el orden que le damos a la matriz
    # se le pone 1 porque se resta 1-1 = 0 que es el primer elemento
    y_order=sorted(n_puntos,key=lambda n_puntos:n_puntos[1])
    # esta es la coordenada
    x1_order=y_order[:2]
    # aca ordenamos al x1
    x1_order=sorted(x1_order,key=lambda x1_order:x1_order[0])
    x2_order=y_order[2:4]
    x2_order=sorted(x2_order,key=lambda x2_order:x2_order[0])
    # toda funcion tiene que retornar una valor
    # retornamos los valores de la matriz ordenados
    return [x1_order[0],x1_order[1],x2_order[0],x2_order[1]]
    # alineamos las imagenes
def alineamiento(imagen,ancho,alto):
    imagen_alineada=None
    # le pasamos grises a la imagen
    grises=cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    # devolvemos dos umbrales minimos y maximos
    tipoumbral,umbral=cv2.threshold(grises, 150,255, cv2.THRESH_BINARY)
    # mostramos el umbral
    cv2.imshow("Umbral", umbral)
    # contornos que devuelven dos valores, contorno y jerarquia
    contorno=cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    # ordenar los contornos son sorted
    # reverse ordena los puntos de menor a mayor, son para los eje x
    contorno=sorted(contorno,key=cv2.contourArea,reverse=True)[:1]
    # recorremos los cotornor
    for c in contorno:
        # la variable c esta recorriendo todos los contornos
        # epsilon ayuda a encontrar las areas
        # arcLenght sirve para sacar las areas
        epsilon=0.01*cv2.arcLength(c, True)
        # aca piden las curvas que va a analizar para que las curvas no tengan tando ruido
        approximacion=cv2.approxPolyDP(c, epsilon, True)
        # contamos objetos que tenemos en la lista
        # los 4 puntos forman un circulo
        if len(approximacion)==4:
            puntos=ordenarpuntos(approximacion)
            # convertimos los puntos en alto y ancho
            puntos1=np.float32(puntos)
            puntos2=np.float32([[0,0],[ancho,0],[0,alto],[ancho,alto]])
            # metodo de perspectiva
            # se mantiene fijo M en caso que la camara rote
            M = cv2.getPerspectiveTransform(puntos1, puntos2)
            # a la imagen alineada le pasamos la informacion
            imagen_alineada=cv2.warpPerspective(imagen, M, (ancho,alto))
    return imagen_alineada
capturavideo= cv2.VideoCapture(0) #abrir la camara el cero es para buscar camara que esta en el cel con droiCam

while True: #si encontro la camara, entonces realiza lo siguiente:
    tipocamara,camara=capturavideo.read() #capturar lo que muestra la camara en video
    if tipocamara==False:
        break
    #definimos una imagen A6 medida de papel
    imagen_A6=alineamiento(camara,ancho=480,alto=640)
    if imagen_A6 is not None:
        # le pasamos una lista vacia
        puntos=[]
        #le pasamos la imagen gris
        imagen_gris=cv2.cvtColor(imagen_A6,cv2.COLOR_BGR2GRAY) #pasar la imagen a gris
        # modelado gausiano con la matriz 5x5 para eliminar ruidos
        blur=cv2.GaussianBlur(imagen_gris,(5,5),1)
        # le aplicamos un umbral valor minimo 0, maximo 255
        # a la hoja de papel la convertimos en negro y al objeto color claro
        _,umbral2=cv2.threshold(blur,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
        # mostramos el umbral
        cv2.imshow("Umbral",umbral2)
        # obtenemos el contorno
        contorno2=cv2.findContours(umbral2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        # dibujamos el contorno
        cv2.drawContours(imagen_A6, contorno2, -1, (255,0,0),2)
        # variables para sumar monedas
        suma1=0.0
        suma2=0.0
        for c_2 in contorno2:
            # segun las areas vamos a saber que monedas estamos recorriendo
            area=cv2.contourArea(c_2)
            # etiqueta de la moneda
            Momentos = cv2.moments(c_2)
            # preguntamos por la matriz
            if(Momentos["m00"]==0):
                # el centro del objeto es m00 es estatico
                # añadimos el 1.0 si esta estatico
                # sirven para añadir etiquetas
                Momentos["m00"]=1.0
                #agregamos las coordenadas, aca los momentos no son estaticos
            x=int(Momentos["m10"]/Momentos["m00"])
            y=int(Momentos["m01"]/Momentos["m00"])

            if area<9300 and area>8000: #moneda de 20 centimos
                #le damos una fuente para ingresarle un texto
                font=cv2.FONT_HERSHEY_SIMPLEX
                #el texto es S/. 0.20
                cv2.putText(imagen_A6, "S/. 0.20",(x,y) , font, 0.75, (0,255,0),2)
                suma1=suma1+0.2
            
            if area<7800 and area>6500:
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(imagen_A6, "S/. 0.10",(x,y) , font, 0.75, (0,255,0),2)
                suma2=suma2+0.1
        total=suma1+suma2
        print("Sumatoria total en Centimos:",round(total,2))
        cv2.imshow("Imagen A6", imagen_A6)
        cv2.imshow("camara", camara) #mostrar la camara
    if cv2.waitKey(1) == ord('s'): #detener la camara cuando presionamos S
        break
capturavideo.release() #detenemos el video
cv2.destroyAllWindows() #destruimos las ventanas







    



 


