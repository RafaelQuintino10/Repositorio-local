from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

# Configurações de opções do Chrome
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--start-maximized")

# Configurações para mascarar o modo headless
chrome_options.add_argument("--headless=new")  # Use "new" instead of the older "--headless"
chrome_options.add_argument("--proxy-server='direct://'")  # Ignora qualquer proxy
chrome_options.add_argument("--proxy-bypass-list=*")  # Bypassa todos os proxys

# Modificar o user-agent
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Configuração de capacidades
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"  # Opção para carregar páginas rapidamente

# Iniciar o driver com as configurações
driver = webdriver.Chrome(service=Service('caminho/para/chromedriver'), options=chrome_options, desired_capabilities=caps)

# Evitar detecção de Selenium
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Testar a execução
driver.get("https://www.opex360.com")

time.sleep(5)
print(driver.title)
driver.quit()