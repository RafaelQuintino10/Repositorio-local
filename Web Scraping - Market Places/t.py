from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Chrome webdriver
driver = webdriver.Chrome()

# Open the desired URL
url = 'https://www.americanas.com.br/busca/pc-gamer?page=1&limit=24&offset=48'
driver.get(url)

# Wait until all product titles are present on the page
WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '//h3[contains(@class,"product-name")]')))

# Find all product titles using XPath
titulos = driver.find_elements(By.XPATH, '//h3[contains(@class,"product-name")]')

# Print each product title
for titulo in titulos:
    print(titulo.text)

# Close the webdriver
driver.quit()
