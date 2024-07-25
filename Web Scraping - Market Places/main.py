from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
import time
from datetime import datetime


# 1) A busca deverá ser feita utilizando UM termo de pesquisa (Ex: luva de goleiro adidas) e deverá ter UM termo de filtro para filtrar os resultados (ex: filtrar os resultados que tenham ao menos as palavras "luvas" e "adidas")

# 2) O resultado deverá ser apenas um arquivo CSV para o produto pesquisado, com as seguintes colunas: marketplace (site onde foi feita a busca), termo pesquisado, termo de filtro (filtros que foram aplicados), dia da busca, hora da busca, preço, inclui_frete (s/n), valor_do_frete (se possivel colocar no momento do scrap um cep de SP capital), vendedor (pode ser o proprio marketplace ou um terceiro), ordem (a posicao que apareceu no resultado), patrocinado (s/n), avaliacao, num_avaliacoes, link.

# 3) Idealmente configurar o scrapping usando servico tipo https://www.proxy4free.com/ para evitarmos qq problema de bloqueio de ip, etc.

# Eu fecho com vc nesses valores, mas com os seguintes detalhes. Como ainda nao trabalhamos antes e seu perfil nao tem avaliacao aqui, fazemos um projeto inicial com 2 marketplaces (mercadolivre e americanas) com valor proporcional (R$320), eles estando ok a gente abre um projeto para os demais



# driver = webdriver.Chrome()
chrome_config = Options()
chrome_config.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_config)
url = 'https://www.americanas.com.br/busca/pc-gamer?page=1&limit=24&offset=48'
driver.get(url)

WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '//h3[contains(@class,"product-name")]')))

titulos = driver.find_elements(By.XPATH, '//h3[contains(@class,"product-name")]')
n = 1
for titulo in titulos:
    print(n,'.',titulo.text)
    n+=1

driver.quit()
