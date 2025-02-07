import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuración inicial mejorada
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Maximizar ventana desde el inicio
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Navegación a la página
    driver.get("https://www.colombiaenmapas.gov.co/#")

    # Manejo de términos y tutorial
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "checkTerminos"))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.close[onclick='cancelTutorial(); return false;']"))).click()

    # Selección de departamento optimizada
    select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchFiltro")))
    driver.execute_script("arguments[0].value = '05'; arguments[0].dispatchEvent(new Event('change'))", select)

    # Espera para carga de temáticas
    time.sleep(1)  # Espera corta necesaria para carga dinámica

    # Búsqueda directa de temática con XPath
    tematica = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class, 'tematica') and contains(translate(., 'GEODESIA', 'geodesia'), 'geodesia')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tematica)
    tematica.click()

    # Búsqueda directa de la capa específica
    # Versión corregida y mejorada para hacer clic en "Red Pasiva GNSS"
    capa = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'media-resultados2')]//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'red pasiva gnss')]")
        )
    )

    # Hacer scroll y click con JavaScript para mayor confiabilidad
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", capa)
    time.sleep(0.5)  # Pequeña espera para el scroll
    driver.execute_script("arguments[0].click();", capa)

    # Extracción de enlaces optimizada
    servicios = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul#enlacesContainer")))
    enlaces = servicios.find_elements(By.CSS_SELECTOR, "a[href]")
    
    print("\nEnlaces encontrados:")
    for enlace in enlaces:
        print(enlace.get_attribute("href"))

finally:
    # Cierre seguro del navegador
    time.sleep(2)  # Espera opcional para visualización final
    driver.quit()