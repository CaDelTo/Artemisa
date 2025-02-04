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


# Esperar hasta que el elemento con el id "checkTerminos" esté presente y hacer clic en él, luego esperar hasta que el botón de cerrar el tutorial esté presente y hacer clic en él
# <input type="checkbox" id="checkTerminos">
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkTerminos"))).click()
# <a href="#" class="close" onclick="cancelTutorial(); return false;" aria-label="Cerrar"><span aria-hidden="true">×</span></a>
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.close[onclick='cancelTutorial(); return false;']"))).click()

# Esperar hasta que el select con el id "searchFiltro" esté presente y obtener todas las opciones del select
# <select class="form-control select2-hidden-accessible" id="searchFiltro" style="width: 100%;font-size: 14px;" data-select2-id="searchFiltro" tabindex="-1" aria-hidden="true">
select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchFiltro")))

# Para testeo pongo una aleatoria
options = select_element.find_elements(By.TAG_NAME, "option")
option = random.choice(options)
option.click()
print(option.text)

# <div class="media media-resultados tematica" data-tematica="36" data-tematica-label="poblacion"><
tematicas = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.media.media-resultados.tematica")))
# Select a random tematica and click it
tematica = None
while tematica is None:
    tematica = random.choice(tematicas)
    if not tematica.text.strip():  # Check if text is empty or just whitespace
        tematica = None
print(f"Selected tematica: {tematica.text}")

# Wait for the media-body element within the selected tematica and click it
media_body = WebDriverWait(tematica, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "media-body")))
media_bodies = tematica.find_elements(By.CLASS_NAME, "media-body")
# Select a random media-body and click it
#TODO: Hacer que pueda pasar el nombre de la tematica para seleccionarla
media_body = random.choice(media_bodies)
driver.execute_script("arguments[0].click();", media_body)

time.sleep(30)

#TODO: Entrar a todos los elementos de la tematica y sacar la info
# media media-resultados2 es el class de los elementos dentro de la tematica