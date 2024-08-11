from telnetlib import EC
from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import chromedriver_autoinstaller
import time
from datetime import datetime
import pandas as pd

# chromedriver_autoinstaller.install()

options = Options()
def converter_tempo(day, month, year):
    # Converte o dia, mês e ano para timestamp em milissegundos
    date_str = f"{day}/{month}/{year}"
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    return int(date_obj.timestamp() * 1000)

def smiles(origem, destino, dia_ida, mes_ida, dia_volta, mes_volta):
    n=1
    driver = Driver(uc=True)
    # Obtém o ano corrente
    ano_atual = datetime.now().year
    # Converte as datas para timestamp
    timestamp_ida = converter_tempo(dia_ida, mes_ida, ano_atual)
    timestamp_volta = converter_tempo(dia_volta, mes_volta, ano_atual)
    # Acessa a URL
    driver.get(f"https://www.smiles.com.br/mfe/emissao-passagem?tripType=1&originAirport={origem}&destinationAirport={destino}&departureDate={timestamp_ida}&returnDate={timestamp_volta}&adults=1&children=0&infants=0&searchType=g3&segments=1&isElegible=false&originCity=&originCountry=&destinCity=&destinCountry=&originAirportIsAny=false&destinationAirportIsAny=true&isFlexibleDateChecked=false&cabin=ECONOMIC&fromSearchMilesBalance=&novo-resultado-voos=true")

    time.sleep(5)
    cookie_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    cookie_button.click()
    time.sleep(15)
    # more_button = driver.find_element(By.CSS_SELECTOR, "button.button.button-pill.undefined.button-more")
    # more_button.click()
    # time.sleep(3)

    dict_passagens = {'Ordem':[],'Preço':[], 'Origem':[], 'Aeroporto/Origem':[], 'Horário de Partida':[], 'Destino':[], 'Aeroporto/Destino':[], 'Horários de Chegada':[], 'Paradas': []}

    passagens = driver.find_elements(By.XPATH, '//div[@class="header-content"]')
    for passagem in passagens:

        try:
            horarios = passagem.find_element(By.XPATH, './/div[@class="info"]').text.strip()
            paradas = passagem.find_element(By.XPATH, './/p[@class="scale-duration__type-flight"]').text.strip()
            preco = passagem.find_element(By.XPATH, './/div[@class="price"]').text.strip()


            horario_partida = horarios.split()[4]
            aeroporto_origem = horarios.split()[3]
            horario_chegada = horarios.split()[6]
            aeroporto_destino = horarios.split()[5]

        except NoSuchElementException:
            horarios = "Não foi possível identificar os horários"
            paradas = "Não foi possível identificar os paradas"
            preco = 'Não foi possível identificar o preço'
            horario_partida = 'Não foi possível identificar o horário de partida!'
            aeroporto_origem = 'Não foi possível identificar o aeroporto de origem!'
            horario_chegada = 'Não foi possível identificar o horário de chegada!'
            aeroporto_destino = 'Não foi possível identificar o aeroporto de destino!'



        dict_passagens['Origem'].append(origem)
        dict_passagens['Preço'].append(preco)
        dict_passagens['Paradas'].append(paradas)
        dict_passagens['Aeroporto/Origem'].append(aeroporto_origem)
        dict_passagens['Horário de Partida'].append(horario_partida)
        dict_passagens['Destino'].append(destino)
        dict_passagens['Horários de Chegada'].append(horario_chegada)
        dict_passagens['Aeroporto/Destino'].append(aeroporto_destino)
        dict_passagens['Ordem'].append(n)

        print(f'{n}. Preço: {preco} // Horário de partida: {horario_partida} // Aeroporto origem: {aeroporto_origem} // Horário de chegada: {horario_chegada} // Aeroporto de destino: {aeroporto_destino}Paradas: {paradas} ')
        
        n+=1
    tabela = pd.DataFrame(dict_passagens)
    print(tabela)
    tabela.to_excel('resultados_smiles.xlsx', index=False)

    driver.quit()



# Entradas do usuário
def origem_f():
    while True:
        origem = str(input("Digite o código do aeroporto de origem (ex: FOR): ")).strip().upper()
        if not origem:
            print('Erro! Tente novamente!')
        else:
            return origem

def dia_ida_f():
    while True:
        dia_ida = (input('Digite o dia da ida (dd): ')).strip()
        if not dia_ida:
            print('Erro! Tente novamente!')
        else:
            return dia_ida

def mes_ida_f():
    while True:
        mes_ida = (input('Digite o mês da ida (mm): ')).strip()
        if not mes_ida:
            print('Erro! Tente novamente!')
        else:
            return mes_ida

def destino_f():
    while True:
        destino = str(input('"Digite o código do aeroporto de destino (ex: SAO): ')).strip().upper()
        if not destino:
            print('Erro! Tente novamente!')
        else:
            return destino

def dia_volta_f():
    while True:
        dia_volta = (input('Digite o dia da volta (dd): ')).strip()
        if not dia_volta:
            print('Erro! Tente novamente!')
        else:
            return dia_volta

def mes_volta_f():
    while True:
        mes_volta = (input('Digite o mês da volta (mm): ')).strip()
        if not mes_volta:
            print('Erro! Tente novamente!')
        else:
            return mes_volta

origem = origem_f()
destino = destino_f()
dia_ida = dia_ida_f()
mes_ida = mes_ida_f()
dia_volta = dia_volta_f()
mes_volta = mes_volta_f()

smiles(origem, destino, dia_ida, mes_ida, dia_volta, mes_volta)