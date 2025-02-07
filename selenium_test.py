import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


# Configurar selenium para usar el driver de Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Definir URL de la página web
url = "https://www.colombiaenmapas.gov.co/#"
driver.get(url)


# Aceptar los términos y condiciones y cerrar el tutorial
# Esperar hasta que el elemento con el id "checkTerminos" esté presente y hacer clic en él, luego esperar hasta que el botón de cerrar el tutorial esté presente y hacer clic en él
# <input type="checkbox" id="checkTerminos">
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkTerminos"))).click()
# <a href="#" class="close" onclick="cancelTutorial(); return false;" aria-label="Cerrar"><span aria-hidden="true">×</span></a>
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.close[onclick='cancelTutorial(); return false;']"))).click()


# Esperar hasta que el select con el id "searchFiltro" esté presente y obtener todas las opciones del select (Seleccionar Zona)
# <select class="form-control select2-hidden-accessible" id="searchFiltro" style="width: 100%;font-size: 14px;" data-select2-id="searchFiltro" tabindex="-1" aria-hidden="true">
select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchFiltro")))
options = select_element.find_elements(By.TAG_NAME, "option")
for option in options:
    if option.text.strip() == "Antioquia":
        option.click()
        print(f"Selected zone: {option.text}")
        break


time.sleep(1)
# <div class="media media-resultados tematica" data-tematica="36" data-tematica-label="poblacion"><
tematicas = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.media.media-resultados.tematica")))
# Select a random tematica and click it

tematica = None
for t in tematicas:
    if "geodesia" in t.text.lower():
        tematica = t
        break
if tematica is None:
    raise Exception("No tematica found with text 'geodasia'")
print(f"Selected tematica: {tematica.text}")

#Darle click a la tematica
media_body = tematica.find_element(By.CLASS_NAME, "media-body")
driver.execute_script("arguments[0].click();", media_body)

time.sleep(1)
elemento_buscar = "Red Pasiva GNSS"  # Specify the element name you want to find
elementos = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.media.media-resultados2")))

elemento_encontrado = None
for elemento in elementos:
    titulo = elemento.find_element(By.CLASS_NAME, "panel-resultados-titulo")
    print(f"Found element: {titulo.text}")
    if elemento_buscar.lower() in titulo.text.lower():
        elemento_encontrado = elemento
        break

if elemento_encontrado:
    driver.execute_script("arguments[0].click();", elemento_encontrado)
    print(f"Clicked on: {elemento_buscar}")
else:
    print(f"Element '{elemento_buscar}' not found")

servicios = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul#enlacesContainer")))
servicios_list = servicios.find_elements(By.CSS_SELECTOR, "li")
for item in servicios_list:
    links = item.find_elements(By.TAG_NAME, "a")
    for link in links:
        print(link.get_attribute("href"))
