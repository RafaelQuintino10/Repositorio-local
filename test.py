import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Função para obter frete inserindo o CEP
def obter_frete(link, cep):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    driver.get(link)
    try:
        cep_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input.ui-pdp-buybox__quantity__input'))
        )
        cep_input.clear()
        cep_input.send_keys(cep)
        cep_input.send_keys(Keys.RETURN)
        
        time.sleep(5)  # Aguarda o carregamento do frete
        
        frete = driver.find_element(By.CSS_SELECTOR, 'span.ui-pdp-price__second-line__label').text
    except Exception as e:
        frete = 'Não disponível'
    driver.quit()
    return frete

escolha_do_usuario = input('Qual produto deseja buscar no Mercado Livre?  ')
cep = input('Insira o CEP para cálculo do frete: ')
url = f"https://lista.mercadolivre.com.br/{escolha_do_usuario}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}
site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
qtd_itens = soup.find('span', class_="ui-search-search-result__quantity-results").get_text().strip()
print(qtd_itens)
dic_produtos = {'Modelo':[], 'Preço':[], 'Link':[], 'Frete':[]}
n = 1

for pagina in range(1,2):
    urlpag = f'https://lista.mercadolivre.com.br/{escolha_do_usuario}_Desde_{(pagina-1)*50+1}'
    site = requests.get(urlpag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.find_all('div', class_="ui-search-result__wrapper")
    for produto in produtos:
        marca = produto.find('h2', class_=re.compile('item__title')).get_text().strip()
        preco = produto.find('span', class_=re.compile('search-price')).get_text().strip()
        link = produto.find('a', class_=re.compile('ui-search-link')).get('href', '')
        if link:
            link_completo = urljoin(url, link)
        else:
            link_completo = ''
        print(n, '.', marca, ' // ', preco, ' // ', link_completo)
        
        frete = obter_frete(link_completo, cep)  # Obtém o frete do produto
        print('Frete: ', frete)
        n += 1

        dic_produtos['Modelo'].append(marca)
        dic_produtos['Preço'].append(preco)
        dic_produtos['Link'].append(link_completo)
        dic_produtos['Frete'].append(frete)

tabela = pd.DataFrame(dic_produtos)
print(tabela)
tabela.to_csv('Resultados_da_pesquisa.csv')
tabela.to_excel('Resultados_da_pesquisa.xlsx')