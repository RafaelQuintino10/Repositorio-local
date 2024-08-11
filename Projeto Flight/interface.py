
from tkinter import END, Listbox, messagebox, filedialog
import customtkinter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
import threading
# Configuração do driver
options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=300x300')

# Função para executar a busca no site da LATAM e exibir resultados na Listbox
def latam(origem, destino, dia_ida, mes_ida, dia_volta, mes_volta):
    n = 1
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.latamairlines.com/br/pt/oferta-voos?origin={origem}&inbound=2024-{mes_volta}-{dia_volta}T12%3A00%3A00.000Z&outbound=2024-{mes_ida}-{dia_ida}T12%3A00%3A00.000Z&destination={destino}&adt=1&chd=0&inf=0&trip=RT&cabin=Economy&redemption=false&sort=RECOMMENDED")
    sleep(3)
    try:
        cookie_button = driver.find_element(By.ID, "cookies-politics-button")
        cookie_button.click()
        sleep(15)
    except:
        pass

    # Limpar a Listbox antes de inserir novos resultados
    grafico.delete(0, END)

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

        # Adicionar resultado na Listbox
        resultado = f'{n}. Preço: {preco} // Horário de partida: {horario_partida} // Aeroporto origem: {aeroporto_origem} // Horário de chegada: {horario_chegada} // Aeroporto de destino: {aeroporto_destino}// Paradas: {paradas} '
        grafico.insert(END, resultado)
        grafico.see(END)
        n += 1

    arquivo = filedialog.asksaveasfilename(defaultextension=' .xlsx', filetypes=[('Planiha Excel', '*xlsx')])
    tabela = pd.DataFrame(dict_passagens)
    tabela.to_excel(arquivo, index=False)
    print(tabela)
    driver.quit()

def executar_scraping():
    # Ler os valores dos campos de entrada
    origem = origem_input.get().strip().upper()
    destino = destino_input.get().strip().upper()
    dia_ida = dia_partida_input.get().strip()
    mes_ida = mes_partida_input.get().strip()
    dia_volta = dia_volta_input.get().strip()
    mes_volta = mes_volta_input.get().strip()

    if not origem or not destino or not dia_ida or not mes_ida or not dia_volta or not mes_volta:
        messagebox.showerror("Erro!", "Todos os campos devem ser preenchidos!")
    else:
        # Chamar a função latam com os valores lidos
        latam(origem, destino, dia_ida, mes_ida, dia_volta, mes_volta)
    # Chamar a função latam com os valores lidos
    # latam(origem, destino, dia_ida, mes_ida, dia_volta, mes_volta)

def clique():
    threading.Thread(target=executar_scraping).start()

janela = customtkinter.CTk()
janela.geometry('800x600')
janela.title('Flight')
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')
#  Configuração de pesos das linhas e colunas para expansão
janela.grid_rowconfigure(5, weight=1)
janela.grid_rowconfigure(6, weight=0)
janela.grid_columnconfigure(0, weight=1)
janela.grid_columnconfigure(1, weight=1)
janela.grid_columnconfigure(2, weight=1)
janela.grid_columnconfigure(3, weight=1)
janela.grid_columnconfigure(4, weight=1)

texto = customtkinter.CTkLabel(janela, text='Passagens aéreas',font=('Helvetica', 24, 'bold'), text_color='#E0FFFF')
texto.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

# Linha 1
origem_label = customtkinter.CTkLabel(janela, text='Origem:',font=('Helvetica', 14, 'bold'), text_color='#E0FFFF')
origem_label.grid(row=1, column=0,padx=10, pady=10, sticky='e')
origem_input = customtkinter.CTkEntry(janela, placeholder_text='Cidade ou aeroporto (Ex: FOR)')
origem_input.grid(row=1, column=1,padx=10, pady=10, sticky='we')

destino_label = customtkinter.CTkLabel(janela, text='Destino:',font=('Helvetica', 14, 'bold'), text_color='#E0FFFF')
destino_label.grid(row=1, column=2, padx=10, pady=10, sticky='e')
destino_input = customtkinter.CTkEntry(janela, placeholder_text='Cidade ou aeroporto (Ex: SAO)')
destino_input.grid(row=1, column=3, padx=10, pady=10, sticky='we')

# Linha 2
dia_partida_label = customtkinter.CTkLabel(janela, text='Dia de partida:',font=('Helvetica', 14, 'bold'), text_color='#E0FFFF')
dia_partida_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
dia_partida_input = customtkinter.CTkEntry(janela, placeholder_text='Digite o dia de partida (Ex: 08)')
dia_partida_input.grid(row=2, column=1, padx=10, pady=10, sticky='we')

mes_partida_label = customtkinter.CTkLabel(janela, text='Mês de partida:',font=('Helvetica', 14, 'bold'), text_color='#E0FFFF')
mes_partida_label.grid(row=2, column=2, padx=10, pady=10, sticky='e')
mes_partida_input = customtkinter.CTkEntry(janela, placeholder_text='Digite o mês de partida (Ex: 09)')
mes_partida_input.grid(row=2, column=3, padx=10, pady=10, sticky='we')

dia_volta_label = customtkinter.CTkLabel(janela, text='Dia da volta:',font=('Helvetica', 14, 'bold'), text_color='#E0FFFF')
dia_volta_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
dia_volta_input = customtkinter.CTkEntry(janela, placeholder_text='Digite o dia da volta (Ex: 08)')
dia_volta_input.grid(row=3, column=1, padx=10, pady=10, sticky='we')

mes_volta_label = customtkinter.CTkLabel(janela, text='Mês da volta:',font=('Helvetica', 14, 'bold'), text_color='#E0FFFF')
mes_volta_label.grid(row=3, column=2, padx=10, pady=10, sticky='e')
mes_volta_input = customtkinter.CTkEntry(janela, placeholder_text='Digite o mês da volta (Ex: 09)')
mes_volta_input.grid(row=3, column=3, padx=10, pady=10, sticky='we')

botao = customtkinter.CTkButton(janela, text='Varrer dados', font=('Helvetica', 14, 'bold'),  fg_color='#1E90FF', command=clique)
botao.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

# Configuração do Listbox para expansão horizontal e vertical
grafico = Listbox(janela, bg='grey', fg='white', font=('Helvetica', 24, 'bold'))
grafico.grid(row=5, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

nome_empresa = customtkinter.CTkLabel(janela, text='Desenvolvido por Front Dev Studio@', font=('Helvetica', 20, 'bold'))
nome_empresa.grid(row=6,column=0, columnspan=5, padx=10, pady=10)


janela.mainloop()
