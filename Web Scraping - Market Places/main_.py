import gettext
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.parse import urljoin

# 1) A busca deverá ser feita utilizando UM termo de pesquisa (Ex: luva de goleiro adidas) e deverá ter UM termo de filtro para filtrar os resultados (ex: filtrar os resultados que tenham ao menos as palavras "luvas" e "adidas")

# 2) O resultado deverá ser apenas um arquivo CSV para o produto pesquisado, com as seguintes colunas: marketplace (site onde foi feita a busca), termo pesquisado, termo de filtro (filtros que foram aplicados), dia da busca, hora da busca, preço, inclui_frete (s/n), valor_do_frete (se possivel colocar no momento do scrap um cep de SP capital), vendedor (pode ser o proprio marketplace ou um terceiro), ordem (a posicao que apareceu no resultado), patrocinado (s/n), avaliacao, num_avaliacoes, link.

# 3) Idealmente configurar o scrapping usando servico tipo https://www.proxy4free.com/ para evitarmos qq problema de bloqueio de ip, etc.

# Eu fecho com vc nesses valores, mas com os seguintes detalhes. Como ainda nao trabalhamos antes e seu perfil nao tem avaliacao aqui, fazemos um projeto inicial com 2 marketplaces (mercadolivre e americanas) com valor proporcional (R$320), eles estando ok a gente abre um projeto para os demais.



escolha_do_usuario = input('Qual produto deseja buscar no Mercado Livre?  ')
url = f"https://lista.mercadolivre.com.br/{escolha_do_usuario}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}
site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
qtd_itens = soup.find('span', class_="ui-search-search-result__quantity-results").get_text().strip()
print(qtd_itens)
dic_produtos = {'Modelo':[], 'Preço':[], 'Link':[]}
n = 1

for pagina in range(1,2):
    urlpag = f'https://lista.mercadolivre.com.br/{escolha_do_usuario}'
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.find_all('div', class_="ui-search-result__wrapper")
    for produto in produtos:
        marca = produto.find('h2', class_=re.compile('item__title')).get_text().strip()
        preco = produto.find('span', class_=re.compile('search-price')).get_text().strip()
        link = produto.find('a', class_=re.compile('search-link')).get('href', '')
        if link:
            link_completo = urljoin(url,link)
        else:
            link_completo = ''
        print(n,'.',marca,' // ', preco,' // ', link_completo)
        n+=1

        dic_produtos['Modelo'].append(marca)
        dic_produtos['Preço'].append(preco)
        dic_produtos['Link'].append(link_completo)
        
tabela = pd.DataFrame(dic_produtos)
print(tabela)
tabela.to_csv('Resultados_da_pesquisa.csv')
tabela.to_excel('Resultados_da_pesquisa.xlsx')