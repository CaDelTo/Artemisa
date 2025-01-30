from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Configurar Selenium en modo headless (sin interfaz gráfica)
options = Options()
options.add_argument("--headless")  # Ejecutar en segundo plano
options.add_argument("--disable-gpu")  # Evitar errores con la GPU
options.add_argument("--disable-software-rasterizer")  # Evita uso de software GPU
options.add_argument("--no-sandbox")  # Evita problemas en entornos Linux
options.add_argument("--disable-dev-shm-usage")  # Evita errores de memoria compartida

# Configurar Selenium con Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Abrir la página
url = "https://www.colombiaenmapas.gov.co/#"
driver.get(url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "panel-resultados-titulo2")))

# Extraer elementos por clase
elementos = driver.find_elements(By.CLASS_NAME, "panel-resultados-titulo2")

for elemento in elementos:
    print(elemento)
driver.quit()
