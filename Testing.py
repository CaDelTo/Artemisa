import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def getServiceLinks(zoneName, targetTopic, targetService, linkType=None):
    """
    Retrieves service links from Colombia en Mapas platform
    
    Args:
        zoneName (str): Name of the geographic zone/department
        targetTopic (str): Desired map topic/category
        targetService (str): Specific service to retrieve links from
        linkType (str, optional): Filter for specific link type (e.g., 'wms')
    
    Returns:
        list: Filtered service URLs
    """
    # Browser setup
    chromeOptions = Options()
    chromeOptions.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chromeOptions
    )

    try:
        # Initialize session
        driver.get("https://www.colombiaenmapas.gov.co/#")

        # Handle initial dialogs
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "checkTerminos"))).click()
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.close[onclick='cancelTutorial(); return false;']"))).click()

        # Zone selection logic
        zoneSelector = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchFiltro")))
        
        # Find zone by name
        zoneOptions = zoneSelector.find_elements(By.TAG_NAME, "option")
        zoneCode = None
        
        for option in zoneOptions:
            if option.text.strip().lower() == zoneName.strip().lower():
                zoneCode = option.get_attribute("value")
                break

        if not zoneCode:
            raise ValueError(f"Zone '{zoneName}' not found in available options")
        
        driver.execute_script(f"""
            arguments[0].value = '{zoneCode}';
            arguments[0].dispatchEvent(new Event('change'))
        """, zoneSelector)

        # Wait for content load
        time.sleep(1)

        # Topic selection
        topicXpath = f"""
            //div[contains(@class, 'tematica') 
            and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 
            '{targetTopic.lower()}')]
        """
        topicElement = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, topicXpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", topicElement)
        topicElement.click()

        # Service selection
        serviceXpath = f"""
            //div[contains(@class, 'media-resultados2')]//*
            [contains(translate(normalize-space(.), 
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 
            'abcdefghijklmnopqrstuvwxyz'), 
            '{targetService.lower()}')]
        """
        serviceElement = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, serviceXpath)))
        
        driver.execute_script("""
            arguments[0].scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        """, serviceElement)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", serviceElement)

        # Link extraction and filtering
        linkContainer = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul#enlacesContainer")))
        
        allLinks = linkContainer.find_elements(By.CSS_SELECTOR, "a[href]")
        filteredLinks = []
        
        for link in allLinks:
            url = link.get_attribute("href")
            linkText = link.text.lower()
            
            if linkType:
                if linkType.lower() in url.lower() or linkType.lower() in linkText:
                    filteredLinks.append(url)
            else:
                filteredLinks.append(url)
        
        return filteredLinks

    finally:
        time.sleep(2)
        driver.quit()

# Configuration (modify these values)
selectedZone = "Antioquia"
selectedTopic = "geodesia"
selectedService = "Red Pasiva GNSS"
requestedLinkType = "wms"

# Execution example
try:
    serviceLinks = getServiceLinks(
        zoneName=selectedZone,
        targetTopic=selectedTopic,
        targetService=selectedService,
        linkType=requestedLinkType
    )

    print(f"\n{len(serviceLinks)} {requestedLinkType.upper()} links found:")
    for index, link in enumerate(serviceLinks, 1):
        print(f"{index}. {link}")

except ValueError as error:
    print(f"\nConfiguration error: {str(error)}")
except Exception as error:
    print(f"\nRuntime error: {str(error)}")