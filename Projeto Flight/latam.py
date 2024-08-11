from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

# Configuração do driver
options = Options()
# options.add_argument('--headless')

# Inicializa o driver


# Acessa a página desejada
def latam(origem, destino, dia_ida, mes_ida, dia_volta, mes_volta):
    n=1
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.latamairlines.com/br/pt/oferta-voos?origin={origem}&inbound=2024-{mes_volta}-{dia_volta}T12%3A00%3A00.000Z&outbound=2024-{mes_ida}-{dia_ida}T12%3A00%3A00.000Z&destination={destino}&adt=1&chd=0&inf=0&trip=RT&cabin=Economy&redemption=false&sort=RECOMMENDED")
    sleep(3)
    cookie_button = driver.find_element(By.ID, "cookies-politics-button")
    cookie_button.click()
    sleep(15)

    dict_passagens = {'Ordem':[],'Preço':[], 'Origem':[], 'Aeroporto/Origem':[], 'Horário de Partida':[], 'Destino':[], 'Aeroporto/Destino':[], 'Horários de Chegada':[], 'Paradas': []}

    passagens = driver.find_elements(By.XPATH, '//li[@class="bodyFlightsstyle__ListItemAvailableFlights-sc__sc-1g00tx2-5 ciAabv"]')
    for passagem in passagens:

        try:
            horarios = passagem.find_element(By.XPATH, './/div[@class="flightInfostyle__WrapperFlightInfo-sc__sc-169zitd-2 deppNM"]').text.strip()
            paradas = passagem.find_element(By.XPATH, './/div[@class="cardFlightstyle__ContainerFooterCard-sc__sc-1fa5kbc-16 gbVmHM"]').text.strip()
            preco = passagem.find_element(By.XPATH, './/div[@class="displayCurrencystyle__DisplayCurrencyWrapper-sc__sc-hel5vp-0 bedHUU"]').text.strip()
            horario_partida = horarios.split()[0]
            aeroporto_origem = horarios.split()[1]
            horario_chegada = horarios.split()[7]
            aeroporto_destino = horarios.split()[8]
        except:
            horarios = "Não foi possível identificar os horários"
            paradas = "Não foi possível identificar os paradas"
            preco = 'Não foi possível identificar o preço'
            horario_partida = 'Não foi possível identificar o horário de partida!'
            aeroporto_origem = 'Não foi possível identificar o aeroporto de origem!'
            horario_chegada = 'Não foi possível identificar o horário de chegada!'
            aeroporto_destino = 'Não foi possível identificar o aeroporto de destino!'



        dict_passagens['Origem'].append(origem)
        dict_passagens['Paradas'].append(paradas)
        dict_passagens['Preço'].append(preco)
        dict_passagens['Aeroporto/Origem'].append(aeroporto_origem)
        dict_passagens['Horário de Partida'].append(horario_partida)
        dict_passagens['Destino'].append(destino)
        dict_passagens['Horários de Chegada'].append(horario_chegada)
        dict_passagens['Aeroporto/Destino'].append(aeroporto_destino)
        dict_passagens['Ordem'].append(n)

        print(f'{n}. Preço: {preco} // Horário de partida: {horario_partida} // Aeroporto origem: {aeroporto_origem} // Horário de chegada: {horario_chegada} // Aeroporto de destino: {aeroporto_destino}// Paradas: {paradas} ')
        n+=1
    tabela = pd.DataFrame(dict_passagens)
    print(tabela)
    tabela.to_excel('resultados_latam.xlsx', index=False)
    driver.quit()


        
def origem_f():
    while True:
        origem = str(input('Digite a origem:  ')).strip().upper()
        if not origem:
            print('Erro! Tente novamente!')
        else:
            return origem

def dia_ida_f():
    while True:
        dia_ida = (input('Dia de partida:  ')).strip()
        if not dia_ida:
            print('Erro! Tente novamente!')
        else:
            return dia_ida

def mes_ida_f():
    while True:
        mes_ida = (input('Mês de partida:  ')).strip()
        if not mes_ida:   
            print('Erro! Tente novamente!')
        else:
            return mes_ida

def destino_f():
    while True:
        destino = str(input('Digite o destino:  ')).strip().upper()
        if not destino:
            print('Erro! Tente novamente!')
        else:
            return destino

def dia_volta_f():
    while True:    
        dia_volta = (input('Dia da volta:  ')).strip()
        if not dia_volta: 
            print('Erro! Tente novamente!')
        else:
            return dia_volta

def mes_volta_f():
    while True:
        mes_volta = (input('Mês da volta:  ')).strip()
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

latam(origem, destino, dia_ida, mes_ida, dia_volta, mes_volta)