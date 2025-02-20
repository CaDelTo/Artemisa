import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


#TODO ARCGIS SOLO DICE SERVICIO, CORTAR HASTA MAPSERVER


def handleTermsConditions(driver):
    """Handles initial legal agreements and tutorial popups"""
    try:
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "checkTerminos"))).click()
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.close[onclick='cancelTutorial(); return false;']"))).click()
    except Exception as e:
        raise RuntimeError("Failed to accept terms and conditions") from e

def getServiceLinks(zoneName, targetTopic, targetService, linkType=None):
    """
    Retrieves geographic service links from Colombia en Mapas platform
    (Official IGAC mapping service: https://www.colombiaenmapas.gov.co)
    
    Args:
        zoneName (str): Name of the department/geographic zone (case-insensitive)
        targetTopic (str): Map category/topic (e.g., 'Geodesia', 'Transporte')
        targetService (str): Specific service layer name (e.g., 'Red Pasiva GNSS')
        linkType (str, optional): Service type filter (e.g., 'wms', 'wfs')
    
    Returns:
        list: Filtered list of service URLs
        
    Raises:
        ValueError: For missing elements or invalid parameters
        RuntimeError: For browser-related failures
    
    Example:
        >>> links = getServiceLinks(
                zoneName="Antioquia",
                targetTopic="Geodesia",
                targetService="Red Pasiva GNSS",
                linkType="wms"
            )
        >>> for link in links:
                print(link)
    """
    # Browser setup (Don't touch this, keep this configuration)
    chromeOptions = Options()
    chromeOptions.add_argument("--headless=new")
    chromeOptions.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chromeOptions
    )

    try:
        driver.get("https://www.colombiaenmapas.gov.co/#")
        
        # Handle legal agreements
        handleTermsConditions(driver)

        # Zone selection with error context
        time.sleep(1)
        try:
            print("Selecting zone...")
            zoneSelector = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "searchFiltro")))
            
            zoneOptions = zoneSelector.find_elements(By.TAG_NAME, "option")
            zoneCode = None
            
            for option in zoneOptions:
                if option.text.strip().lower() == zoneName.strip().lower():
                    zoneCode = option.get_attribute("value")
                    break

            if not zoneCode:
                available_zones = [opt.text.strip() for opt in zoneOptions]
                raise ValueError(
                    f"Zone '{zoneName}' not found. Available options: {', '.join(available_zones)}"
                )
            
            driver.execute_script(f"""
                arguments[0].value = '{zoneCode}';
                arguments[0].dispatchEvent(new Event('change'))
            """, zoneSelector)
            
            # Wait for content load
            time.sleep(1)

        except Exception as e:
            raise ValueError(f"Zone selection failed: {str(e)}") from e

        # Topic selection with error context
        try:
            print("Selecting topic...")
            topicXpath = f"""
                //div[contains(@class, 'tematica') 
                and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 
                '{targetTopic.lower()}')]
            """
            topicElement = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, topicXpath)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", topicElement)
            topicElement.click()
        except Exception as e:
            raise ValueError(f"Topic '{targetTopic}' not found") from e

        # Service selection with error context
        try:
            print("Selecting service...")
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
        except Exception as e:
            raise ValueError(f"Service '{targetService}' not found") from e

        # Link processing with error context
        try:
            print("Extracting links...")
            linkContainer = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul#enlacesContainer")))
            
            allLinks = linkContainer.find_elements(By.CSS_SELECTOR, "a[href]")
            
            if not allLinks:
                raise ValueError("No links found")
            
            filteredLinks = []
            for link in allLinks:
                url = link.get_attribute("href")
                linkText = link.text.lower()
                if not linkType:
                    filteredLinks.append(url)
                    continue

                link_type_lower = linkType.strip().lower()
                
                # Handle special cases
                if link_type_lower == "arcgis" and "servicio" in linkText:
                    filteredLinks.append(url)
                elif link_type_lower in ["wms", "wfs"] and f"Servicio ({linkType.upper()})" in linkText:
                    filteredLinks.append(url)
                # Generic case - search in both URL and link text
                elif link_type_lower in url.lower() or link_type_lower in linkText:
                    filteredLinks.append(url)
            
            if linkType and not filteredLinks:
                raise ValueError(f"No '{linkType}' links found")

            processed_links = []
            for url in filteredLinks:
                if "MapServer" in url:
                    index = url.find("MapServer")
                    truncated = url[:index + len("MapServer")]
                    processed_links.append(truncated)
                elif "FeatureServer" in url:
                    index = url.find("FeatureServer")
                    truncated = url[:index + len("FeatureServer")]
                    processed_links.append(truncated)
                else:
                    processed_links.append(url)
            
            return processed_links

        except Exception as e:
            raise RuntimeError("Link extraction failed") from e

    finally:
        driver.quit()

# Parametros
selectedZone = "Colombia"
selectedTopic = "geodesia"
selectedService = "Red Pasiva GNSS"
requestedLinkType = " wms"

try:
    serviceLinks = getServiceLinks(
        zoneName=selectedZone,
        targetTopic=selectedTopic,
        targetService=selectedService,
        linkType=requestedLinkType
    )

    for link in serviceLinks:
        print(link)

except ValueError as error:
    print(f"\nCONFIGURATION ERROR: {error}")
    if error.__cause__:
        print(f"Technical details: {error.__cause__}")
except RuntimeError as error:
    print(f"\nOPERATIONAL ERROR: {error}")
    if error.__cause__:
        print(f"Technical details: {error.__cause__}")
except Exception as error:
    print(f"\nUNEXPECTED ERROR: {type(error).__name__} - {error}")