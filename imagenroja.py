import cv2 as cv
img = cv.imread('C:\\Users\\eliga\\OneDrive\\Pictures\\figura.png', 1)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
ubbr = (0,60,60)
ubar = (10,255,255) #umbral alto y bajo de color en formato HSV
ubb1r = (170,60,60) #segunda parte del umbral para el color rojo
uba1r = (180,255,255)
ubba = (100,60,60)
ubaa = (140,255,255) #umbral alto y bajo de color en formato HSV
ubb1a = (140,60,60) #segunda parte del umbral para el color rojo
uba1a = (170,255,255)
ubbv = (40,60,60)
ubav = (80,255,255) #umbral alto y bajo de color en formato HSV
ubb1v = (80,60,60) #segunda parte del umbral para el
uba1v = (100,255,255)
ubbam = (20,60,60)
ubaam = (40,255,255) #umbral alto y bajo de color en formato HSV
mask1 = cv.inRange(hsv, ubbr, ubar)    
mask2 = cv.inRange(hsv, ubb1r, uba1r)
maskr = mask1 + mask2
mask3 = cv.inRange(hsv, ubba, ubaa)
mask4 = cv.inRange(hsv, ubb1a, uba1a)
maska = mask3 + mask4
mask5 = cv.inRange(hsv, ubbv, ubav)
mask6 = cv.inRange(hsv, ubb1v, uba1v)
maskv = mask5 + mask6
mask7 = cv.inRange(hsv, ubbam, ubaam)
maskam = mask7
resultado1 = cv.bitwise_and(img, img, mask=maskr) 
resultado2 = cv.bitwise_and(img, img, mask=maska)
resultado3 = cv.bitwise_and(img, img, mask=maskv)
resultado4 = cv.bitwise_and(img, img, mask=maskam)
cv.imshow('img', img)
cv.imshow('mask', maskr)
cv.namedWindow('resultado Rojo', cv.WINDOW_NORMAL)
cv.imshow('resultado Rojo', resultado1)
cv.namedWindow('resultado Azul', cv.WINDOW_NORMAL)
cv.imshow('resultado Azul', resultado2)
cv.namedWindow('resultado Verde', cv.WINDOW_NORMAL)
cv.imshow('resultado Verde', resultado3)
cv.namedWindow('resultado Amarillo', cv.WINDOW_NORMAL)
cv.imshow('resultado Amarillo', resultado4)
cv.waitKey(0)
cv.destroyAllWindows()
