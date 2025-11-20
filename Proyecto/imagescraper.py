from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from PIL import Image
import requests
import io
import time
import os
PATH = "C:\\Users\\eliga\\OneDrive\\Documentos\\GitHub\\INTELIGENCIAARTIFICIAL-ALCARAZ\\Proyecto\\chromedriver.exe"
def descargar_imagenes_google(query, cantidad):
   
    service = Service(PATH)
    driver = webdriver.Chrome(service=service)
   
    driver.get(f"https://www.google.com/search?q={query}&tbm=isch")
    time.sleep(2)
   
    urls = set()
   
    for scroll in range(10):
        scroll += 1
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1)
       
        imagenes = driver.find_elements(By.TAG_NAME, "img")
       
        for img in imagenes:
            try:
                src = img.get_attribute("src")
                if src and src.startswith("http") and len(src) > 50:
                    urls.add(src)
                    if len(urls) >= cantidad:
                        break
            except:
                pass
       
        if len(urls) >= cantidad:
            break
   
    driver.quit()
   
    descargadas = 0
   
    for i, url in enumerate(urls):
        try:
            img_data = requests.get(url, timeout=10).content
            img = Image.open(io.BytesIO(img_data)).convert("RGB")
            img.save(f"Proyecto/gatos/gato{i}.jpg", "JPEG")
            descargadas += 1
           
        except:
            print(f"ERROR AL DESCARGAR IMAGEN {i+1}")
descargar_imagenes_google("cats full body", 20)