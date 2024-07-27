from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from urllib.parse import urljoin
from datetime import datetime

# 1) A busca deverá ser feita utilizando UM termo de pesquisa (Ex: luva de goleiro adidas) e deverá ter UM termo de filtro para filtrar os resultados (ex: filtrar os resultados que tenham ao menos as palavras "luvas" e "adidas")

# 2) O resultado deverá ser apenas um arquivo CSV para o produto pesquisado, com as seguintes colunas: marketplace (site onde foi feita a busca), termo pesquisado, termo de filtro (filtros que foram aplicados), dia da busca, hora da busca, preço, inclui_frete (s/n), valor_do_frete (se possivel colocar no momento do scrap um cep de SP capital), vendedor (pode ser o proprio marketplace ou um terceiro), ordem (a posicao que apareceu no resultado), patrocinado (s/n), avaliacao, num_avaliacoes, link.

# 3) Idealmente configurar o scrapping usando servico tipo https://www.proxy4free.com/ para evitarmos qq problema de bloqueio de ip, etc.

# Eu fecho com vc nesses valores, mas com os seguintes detalhes. Como ainda nao trabalhamos antes e seu perfil nao tem avaliacao aqui, fazemos um projeto inicial com 2 marketplaces (mercadolivre e americanas) com valor proporcional (R$320), eles estando ok a gente abre um projeto para os demais.

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(options=chrome_options)

# Função principal
def scrape_mercadolivre(produto):
    url = f"https://lista.mercadolivre.com.br/{produto}"
    driver.get(url)

    # Obtém a quantidade de resultados
    qtd_itens = driver.find_element(By.XPATH, '//span[contains(@class, "ui-search-search-result__quantity-results")]').text.strip()
    print(qtd_itens)

    dic_produtos = {'Modelo': [], 'Preço': [], 'Link': [], 'Marketplace': [], 'Termo Pesquisado': [], 'Termo de Filtro': [], 'Dia da Busca': [], 'Hora da Busca': [], 'Inclui Frete': [], 'Valor do Frete': [], 'Vendedor': [], 'Ordem': [], 'Patrocinado': [], 'Avaliação': [], 'Num Avaliações': []}
    n = 1

    produtos = driver.find_elements(By.XPATH, '//div[@class="ui-search-result__wrapper"]')

    for produto in produtos:
        # Encontra os produtos, preços e links
        marca = produto.find_element(By.XPATH, './/h2[contains(@class, "item__title")]').text.strip()
        preco = produto.find_element(By.XPATH, './/span[contains(@class, "search-price")]').text.strip()
        link = produto.find_element(By.XPATH, './/a[contains(@class, "search-link")]').get_attribute('href')
        link_completo = urljoin(url, link)
        dic_produtos['Modelo'].append(marca)
        # Adiciona informações acima ao dicionário
        dic_produtos['Preço'].append(preco)
        dic_produtos['Link'].append(link_completo)
        
        # Faz uma validação dos dados(N.avaliaçõs, frete, valor do frete, patrocínio...). 
        # Se encontrados, são adicionados ao dicionário!
        try:
            avaliacoes = produto.find_element(By.XPATH, './/span[contains(@class, "rating-number")]').text.strip()
            num_avaliacoes = produto.find_element(By.XPATH, './/span[contains(@class, "reviews__amount")]').text.strip()
            dic_produtos['Avaliação'].append(avaliacoes)  
            dic_produtos['Num Avaliações'].append(num_avaliacoes) 
            # frete = produto.find_element(By.XPATH, './/span[contains(@class, "ui-pb-highlight")]').text.strip()
            # patrocinado = produto.find_element(By.XPATH, './/span[contains(@class, "reviews__amount")]').text.strip()
            # dic_produtos['Frete'].append(frete) 
        except:
            dic_produtos['Avaliação'].append('Não possui avaliações') 
            dic_produtos['Num Avaliações'].append('Não possui num.avaliações')  

            
        print(f"{n}. {marca} // {preco} // {link_completo} // {avaliacoes} // {num_avaliacoes}")

        
        
        dic_produtos['Marketplace'].append('Mercado Livre')
        dic_produtos['Termo Pesquisado'].append(escolha_do_usuario)
        dic_produtos['Termo de Filtro'].append('luvas, adidas')  # Exemplo de termo de filtro
        dic_produtos['Dia da Busca'].append(datetime.now().strftime("%d-%m-%Y"))
        dic_produtos['Hora da Busca'].append(datetime.now().strftime("%H:%M:%S"))
         # Simulação de valor do frete
        dic_produtos['Vendedor'].append('')  # Simulação de vendedor
        dic_produtos['Ordem'].append(n)
        dic_produtos['Patrocinado'].append('N')  # Simulação de patrocinado
        
        n += 1

    # Cria DataFrame e salva em CSV e em excel
    tabela = pd.DataFrame(dic_produtos)
    print(tabela)
    tabela.to_csv('Resultados_da_pesquisa_selenium.csv', index=False)
    tabela.to_excel('Resultados_da_pesquisa_selenium.xlsx', index=False)

# Entrada do usuário
escolha_do_usuario = input('Qual produto deseja buscar no Mercado Livre? ')
scrape_mercadolivre(escolha_do_usuario)

# Fecha o WebDriver
driver.quit()
