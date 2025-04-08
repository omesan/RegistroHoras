from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import os


from datetime import datetime
import calendar
import time

load_dotenv()


# RUTA donde tengas el chromedriver
CHROME_DRIVER_PATH  = "C:\\webDrivers\\chromedriver-win64\\chromedriver.exe"

# Credenciales
USUARIO = os.getenv("USUARIO")
CONTRASENA = os.getenv("CONTRASENA")

# Inicializar el navegador
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)
driver.get("https://smart4.myteam2go.com/smart4?c=MTQ1")

# 👉 Maximizar la ventana
driver.maximize_window()

# --- Login ---
driver.find_element(By.ID, "j_username").send_keys(USUARIO)
driver.find_element(By.ID, "j_password").send_keys(CONTRASENA)
login_button = driver.find_element(By.NAME, "login")
ActionChains(driver).move_to_element(login_button).perform()
login_button.click()

#seleccionar opcion Menu

wait = WebDriverWait(driver, 10)
menu = wait.until(EC.element_to_be_clickable((By.ID, "openBurgerMenu")))
menu.click()


# ir Registro de Horas
wait = WebDriverWait(driver, 10)
menu_opcionInicio = wait.until(EC.element_to_be_clickable((By.ID, "moduleMenuOption-0")))
menu_opcionInicio.click()

wait = WebDriverWait(driver, 10)
menu_opcionImputacion = wait.until(EC.element_to_be_clickable((By.ID, "menuForm:tabView0:j_idt65")))
menu_opcionImputacion.click()

#espera cargue de pagina
time.sleep(5)

 #Añadir Nuevo Registro de horas
Añadir_button = driver.find_element(By.ID, "taskWorkedTabView:taskWorkedFormList:taskWorkedTable:add")
Añadir_button.click()
wait = WebDriverWait(driver, 10)

# Paso 1: Clic en el dropdown (el label visible)
dropdown_label = wait.until(EC.element_to_be_clickable((By.ID, "taskWorkedTabView:taskWorkedForm:task_label")))
dropdown_label.click()

# Paso 2: Esperar a que la lista se despliegue y seleccionar la opción
opcion = wait.until(EC.element_to_be_clickable((
    By.XPATH,
    "//li[contains(@id, 'taskWorkedTabView:taskWorkedForm:task_') and contains(text(), 'Horas Laborales')]"
)))
opcion.click()


hoy = datetime.today()

#test de viernes
#hoy=datetime.strptime("01/04/2025", "%d/%m/%Y").date()

primer=hoy
ultimo=hoy

# Registro fechas desde hasta
campo_fecha_ini = wait.until(EC.element_to_be_clickable((By.ID, "taskWorkedTabView:taskWorkedForm:date_input")))
campo_fecha_ini.clear()
campo_fecha_ini.send_keys( f"{primer.day}/{primer.strftime('%m')}/{primer.strftime('%y')}") 

campo_fecha_fin = wait.until(EC.element_to_be_clickable((By.ID, "taskWorkedTabView:taskWorkedForm:dateEnd_input")))
campo_fecha_fin.clear()
campo_fecha_fin.send_keys( f"{ultimo.day}/{ultimo.strftime('%m')}/{ultimo.strftime('%y')}") 

#horas trabajadas
campo_horas = wait.until(EC.element_to_be_clickable((By.ID, "taskWorkedTabView:taskWorkedForm:hours_input")))
campo_horas.clear()
if hoy.weekday() == 4:
    campo_horas.send_keys("7")
else:
    campo_horas.send_keys("8,75")  # o el valor que necesites

# guardar
boton_guardar = wait.until(EC.element_to_be_clickable((By.ID, "taskWorkedTabView:taskWorkedForm:save")))
boton_guardar.click()
