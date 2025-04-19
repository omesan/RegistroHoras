from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from datetime import datetime
import calendar
import time


from dotenv import load_dotenv
import os



# RUTA donde tengas el chromedriver
CHROME_DRIVER_PATH  = "C:\\webDrivers\\chromedriver-win64\\chromedriver.exe"

# Credenciales
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




#it Registro de Horas
wait = WebDriverWait(driver, 10)
menu_opcionInicio = wait.until(EC.element_to_be_clickable((By.ID, "moduleMenuOption-0")))
menu_opcionInicio.click()

wait = WebDriverWait(driver, 10)
menu_opcionImputacion = wait.until(EC.element_to_be_clickable((By.ID, "menuForm:tabView0:j_idt65")))
menu_opcionImputacion.click()

#espera cargue de pagina
time.sleep(5)



hoy = datetime.today()
anio_actual = hoy.year
mes_actual = hoy.month


def obtener_primer_y_ultimo_dia_habil(anio, mes):
    # Obtener número de días del mes
    _, dias_en_mes = calendar.monthrange(anio, mes)

    primer_habil = None
    ultimo_habil = None

    for dia in range(1, dias_en_mes + 1):
        fecha = datetime(anio, mes, dia)
        if fecha.weekday() < 5:  # Lunes (0) a Viernes (4)
            if not primer_habil:
                primer_habil = fecha
            ultimo_habil = fecha

    return primer_habil, ultimo_habil

primer, ultimo = obtener_primer_y_ultimo_dia_habil(anio_actual, mes_actual)


hora="8,75"


# Días que queremos dejar seleccionados
dias_permitidos = ["Lunes", "Martes", "Miércoles", "Jueves"]

for i in range(2):
    
    if i==1:
        hora="7"
        dias_permitidos = ["Viernes"]
        
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


    # Registro fechas
    campo_fecha_ini = wait.until(EC.element_to_be_clickable((By.ID, "taskWorkedTabView:taskWorkedForm:date_input")))
    campo_fecha_ini.clear()
    campo_fecha_ini.send_keys( f"{primer.day}/{primer.strftime('%m')}/{primer.strftime('%y')}") 

    campo_fecha_fin = wait.until(EC.element_to_be_clickable((By.ID, "taskWorkedTabView:taskWorkedForm:dateEnd_input")))
    campo_fecha_fin.clear()
    campo_fecha_fin.send_keys( f"{ultimo.day}/{ultimo.strftime('%m')}/{ultimo.strftime('%y')}") 


    campo_horas = wait.until(EC.element_to_be_clickable((By.ID, "taskWorkedTabView:taskWorkedForm:hours_input")))
    campo_horas.clear()
    campo_horas.send_keys(hora)

    # Paso 1: Clic en el dropdown para abrir el menú de días
    dropdown_label = wait.until(EC.element_to_be_clickable((By.ID, "taskWorkedTabView:taskWorkedForm:daysOfWeek")))
    dropdown_label.click()


    # Paso 2: Esperar a que el panel de días esté visible
    wait.until(EC.visibility_of_element_located((By.ID, "taskWorkedTabView:taskWorkedForm:daysOfWeek_panel")))

    

    # Forzar clic con JavaScript
    for i in range(0, 7):  # 0 a 6 → lunes a domingo
        label = driver.find_element(By.XPATH, f"//label[@for='taskWorkedTabView:taskWorkedForm:daysOfWeek:{i}']")
        texto_dia = label.text.strip()

        # Si el día no está permitido, desmarcar (forzar clic)
        if texto_dia not in dias_permitidos:
            driver.execute_script("arguments[0].click();", label)

    # Ahora asegurarnos de que lunes a jueves estén marcados (por si no lo estaban)
    for indice, dia in enumerate(dias_permitidos):
              
        if dia=="Viernes":
            label = driver.find_element(By.XPATH, f"//label[@for='taskWorkedTabView:taskWorkedForm:daysOfWeek:{4}']")
            driver.execute_script("arguments[0].click();", label)
        else:
            label = driver.find_element(By.XPATH, f"//label[@for='taskWorkedTabView:taskWorkedForm:daysOfWeek:{indice}']")
            driver.execute_script("arguments[0].click();", label)

    # guardar
    boton_guardar = wait.until(EC.element_to_be_clickable((By.ID, "taskWorkedTabView:taskWorkedForm:save")))
    boton_guardar.click()
    del boton_guardar
    driver.refresh()
    wait.until(EC.element_to_be_clickable((By.ID, "taskWorkedTabView:taskWorkedFormList:taskWorkedTable:add")))



