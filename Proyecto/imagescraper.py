from selenium import webdriver
from selenium.webdriver.chrome.service import Service

PATH = "C:\\Users\\eliga\\OneDrive - Instituto Tecnológico de Morelia\\tec\\trabajos\\IA\\Proyecto\\chromedriver.exe"

service = Service(executable_path=PATH)
wd = webdriver.Chrome(service=service)


