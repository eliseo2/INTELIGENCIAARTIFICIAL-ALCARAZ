import cv2 as cv 
import numpy as np 
import os
from tqdm import tqdm 
import time 

dataSet = 'C:\\Users\\eliga\\OneDrive\\Pictures\\likcos\\recorte\\Sebas'
faces = os.listdir(dataSet)
print(faces)

labels = []
facesData = []
label = 0 


for face in faces:
    facePath = dataSet + '\\' + face
    
    
    faceNamesList = os.listdir(facePath)

    for face in faces:
        facePath = dataSet + '\\' + face
        for faceName in os.listdir(facePath):
            labels.append(label)
            facesData.append(cv.imread(facePath + '\\' + faceName, 0))
        label = label + 1


print("Entrenando modelo EigenFace...")
faceRecognizer = cv.face.EigenFaceRecognizer_create()

start_time = time.time() 


faceRecognizer.train(facesData, np.array(labels))

end_time = time.time() 
total_time = end_time - start_time
faceRecognizer.write('EigenFace.xml')
print("Modelo guardado como 'EigenFace.xml'")