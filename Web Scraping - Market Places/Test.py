import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Função para fazer scraping da Americanas usando Selenium
def scrape_americanas_selenium(search_term, filter_term):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_driver_path = '/caminho/para/o/seu/chromedriver'  # Substitua pelo caminho do seu chromedriver
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
    
    try:
        # Abrir a página de busca da Americanas
        driver.get(f'https://www.americanas.com.br/busca/{search_term}')
        
        # Esperar alguns segundos para a página carregar completamente
        time.sleep(5)
        
        # Simular ação de filtrar (exemplo: clicar em um botão de filtro)
        # Aqui você precisaria implementar a lógica para interagir com a página usando Selenium
        
        # Exemplo de extração de dados
        produtos = driver.find_elements(By.XPATH, '//div[@class="product-grid-item"]')
        
        data = []
        
        for index, produto in enumerate(produtos):
            # Exemplo de extração de dados como título, preço e link
            titulo = produto.find_element(By.XPATH, './/span[@class="product-name"]').text.strip()
            preço = produto.find_element(By.XPATH, './/span[@class="product-price"]').text.strip()
            link = produto.find_element(By.XPATH, './/a[@class="product-link"]')['href']
            
            # Exemplo de extração de inclui_frete e valor_do_frete
            try:
                inclui_frete_element = produto.find_element(By.XPATH, './/span[@class="product-shipping"]')
                inclui_frete = inclui_frete_element.text.strip() if inclui_frete_element else 'Não especificado'
        
                valor_frete_element = produto.find_element(By.XPATH, './/span[@class="product-shipping-price"]')
                valor_do_frete = valor_frete_element.text.strip() if valor_frete_element else 'Não especificado'
            except:
                inclui_frete = 'Não especificado'
                valor_do_frete = 'Não especificado'
            
            # Exemplo de extração de vendedor
            try:
                vendedor_element = produto.find_element(By.XPATH, './/span[@class="seller-name"]')
                vendedor = vendedor_element.text.strip() if vendedor_element else 'Não especificado'
            except:
                vendedor = 'Não especificado'
            
            # Exemplo de verificação se é patrocinado
            try:
                patrocinado_element = produto.find_element(By.XPATH, './/div[@class="sponsored-tag"]')
                patrocinado = 's' if patrocinado_element else 'n'
            except:
                patrocinado = 'n'
            
            # Exemplo de extração de avaliação e número de avaliações
            try:
                avaliacao_element = produto.find_element(By.XPATH, './/span[@class="product-rating-stars"]')
                avaliacao = avaliacao_element.get_attribute('aria-label').strip() if avaliacao_element else 'Não especificado'
        
                num_avaliacoes_element = produto.find_element(By.XPATH, './/span[@class="product-rating-count"]')
                num_avaliacoes = num_avaliacoes_element.text.strip() if num_avaliacoes_element else 'Não especificado'
            except:
                avaliacao = 'Não especificado'
                num_avaliacoes = 'Não especificado'
            
            # Construir um dicionário com os dados do produto
            produto_data = {
                'marketplace': 'Americanas',
                'termo_pesquisado': search_term,
                'termo_filtro': filter_term,
                'dia_da_busca': datetime.now().strftime('%Y-%m-%d'),
                'hora_da_busca': datetime.now().strftime('%H:%M:%S'),
                'preço': preço,
                'inclui_frete': inclui_frete,
                'valor_do_frete': valor_do_frete,
                'vendedor': vendedor,
                'ordem': index + 1,
                'patrocinado': patrocinado,
                'avaliação': avaliacao,
                'num_avaliações': num_avaliacoes,
                'link': link
            }
            data.append(produto_data)
        
        return pd.DataFrame(data)
    
    finally:
        driver.quit()

# Receber entrada do usuário para termo de pesquisa e termo de filtro
def get_user_input():
    search_term = input("Digite o termo de pesquisa: ").strip().replace(' ', '+')
    filter_term = input("Digite o termo de filtro: ").strip().replace(' ', '+')
    return search_term, filter_term

# Obter entrada do usuário
search_term, filter_term = get_user_input()

# Scraping da Americanas com os termos fornecidos pelo usuário usando Selenium
df = scrape_americanas_selenium(search_term, filter_term)

# Salvar em um arquivo CSV
df.to_csv('resultado.csv', index=False)

print(f"Dados salvos em 'resultado.csv' para o termo de pesquisa '{search_term}' com filtro '{filter_term}'.")
