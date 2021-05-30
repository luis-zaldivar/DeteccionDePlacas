import cv2#libreria para deteccion de bordes
import pytesseract#libreria para el reconocimiento optico de caracteres
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'#ruta donde esta pytesseract

##################################################################################
#                                                                                #
#               segmento de codigo para encontrar los contornos de las placas    #
#                                                                                #
##################################################################################

imagen = cv2.imread('Funcionales/c1.jpg')# leemos la imagen con la que trabajaremos
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)  # aplicamos escala de grises
gris = cv2.blur(gris, (3, 3))  # aplicamos filtro a grises
canny = cv2.Canny(gris, 150, 200)  # aplicamos canny
canny = cv2.dilate(canny, None, iterations=1)  # buscamos los bordes
contornos, _ = cv2.findContours(
    canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # Encontrar los contornos

##################################################################################
#                                                                                #
#           segmento de codigo para sacar el texto de las plcas                  #
#                                                                                #
##################################################################################

for contorno in contornos:  # ciclo para los contornos
    area = cv2.contourArea(contorno)  # obtenemos el area de figura
    x, y, w, h = cv2.boundingRect(contorno)  # calculamos el total de lados
    epsilon = 0.09*cv2.arcLength(contorno, True)
    numeroLados = cv2.approxPolyDP(contorno, epsilon, True)
    # buscamos las figuras de 4 lados y con area de 1500
    if len(numeroLados) == 4 and area >= 1500:
        placa = gris[y:y+h, x:x+w]  # sacamos las placas
        # sacamos el texto de las placas
        texto = pytesseract.image_to_string(placa, config='--psm 11')
        print(texto)  # mostramos el texto en consola
        if len(texto) > 6:  # filtrar por largo de texto encontrado
            cv2.imshow('PLACA', placa)  # Mostrar la imagen de la placa
            # mostrar el rectangulo donde estan las plcas
            cv2.rectangle(imagen, (x, y), (x+w, y+h), (0, 255, 0), 3)
            # mostramos el texto de las placas
            newI = cv2.resize(imagen, (1200, 900))  # redimencionamos la imagen
            #cv2.imshow('deteccion',newI)#mostramos la deteccion del rectangulo de las placas
            cv2.putText(imagen, texto, (x-20, y-10),
                        1, 4.2, (0, 255, 0), 3)

##################################################################################
#                                                                                #
#                         Mostramos el resultado                                 #
#                                                                                #
##################################################################################

newI = cv2.resize(imagen, (1200, 900))#redimencionamos la imagen
cv2.imshow('Image', newI)#mostramos la imagen
cv2.waitKey(0)#esperamos a presionar el teclado
